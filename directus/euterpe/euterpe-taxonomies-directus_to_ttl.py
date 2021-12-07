from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import requests
import os
import sys
import yaml
import json
from sherlockcachemanagement import Cache
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# Cache
cache = Cache(args.cache)

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

############################################################################################
## INITIALISATION DU GRAPHE ET NAMESPACES
############################################################################################

output_graph = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
sdt_ns = Namespace("http://data-iremus.huma-num.fr/datatypes/")
sherlock_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

output_graph.bind("crm", crm_ns)
output_graph.bind("dcterms", DCTERMS)
output_graph.bind("skos", SKOS)
output_graph.bind("sdt", sdt_ns)
output_graph.bind("she_ns", sherlock_ns)

a = RDF.type

def crm(x):
	return URIRef(crm_ns[x])

def she(x):
	return URIRef(iremus_ns[x])

def she_ns(x):
	return URIRef(sherlock_ns[x])

def t(s, p, o):
	output_graph.add((s, p, o))


############################################################################################
## RECUPERATION DES DONNEES DANS DIRECTUS
############################################################################################

# Taxonomies
query = """
query{
  chants(limit: -1) {
    id
    nom
  }
  domaines(limit: -1) {
    id
    nom
  }
  roles(limit: -1) {
    id
    nom
  }
  ecoles(limit: -1) {
    id
    nom
  }
  instruments_de_musique(limit: -1) {
    id
    nom
    parent {
      id
    }
  }
  lieux_de_conservation(limit: -1) {
    id
    nom
  }
  notations_musicales(limit: -1) {
    id
    nom
  }
  periodes(limit: -1) {
    id
    nom
  }
  specialites(limit: -1) {
    id
    nom
  }
  supports(limit: -1) {
    id
    nom
  }
  themes(limit: -1) {
    id
    nom
    parent {
      id
    }
  }
  types_oeuvres(limit: -1) {
    id
    nom
  }
}
"""

r = requests.post(secret["url"] + '/graphql' + '?access_token=' + access_token, json={'query': query})
print(r.status_code)
result = json.loads(r.text)

############################################################################################
## CREATION DES TRIPLETS
############################################################################################

for taxonomie in result["data"]:
	nom = taxonomie.replace("_", " ").capitalize()

	E32_uri = she(
		cache.get_uuid(["taxonomies", nom], True))
	t(E32_uri, a, crm("E32_Authority_Document"))
	t(E32_uri, crm("P1_is_identified_by"), l(nom))

	for concept in result["data"][taxonomie]:
		t(she(concept["id"]), a, crm("E55_Type"))
		t(E32_uri, crm("P71_lists"), she(concept["id"]))
		t(she(concept["id"]), crm("P1_is_identified_by"), Literal(concept["nom"]))

		if taxonomie == "themes" or taxonomie == "instruments_de_musique":
			try:
				if concept["parent"] is None:
					t(E32_uri, she_ns("sheP_a_pour_entité_de_plus_haut_niveau"), she(concept["id"]))
				else:
					t(she(concept["id"]), crm("P127_has_broader_term"), she(concept["parent"]["id"]))
			except:
				print("Erreur :", concept)

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

serialization = output_graph.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "wb") as f:
	f.write(serialization)

cache.bye()