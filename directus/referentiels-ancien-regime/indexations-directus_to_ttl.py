import json
from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import argparse
from pprint import pprint
from sherlockcachemanagement import Cache
import requests
import os
import sys
import yaml

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")
args = parser.parse_args()

# Cache
cache = Cache(args.cache)
cache_tei = Cache(args.cache_tei)

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login", json={"email": secret["email"], "password": secret["password"]})
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
output_graph.bind("she", sherlock_ns)

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

query = """
query {
  sources_articles(limit: -1) {
    id
    personnes{personnes_id{id}}
    }
  }"""

r = requests.post(secret["url"] + '/graphql' + '?access_token=' + access_token, json={'query': query})
print(r.status_code)
result = json.loads(r.text)

############################################################################################
## CREATION DES TRIPLETS
############################################################################################

for indexation in result["data"]["sources_articles"]:
	id_livraison = indexation["id"][3:].split("_")
	id_livraison = id_livraison[0]
	id_article = indexation["id"][3:]

	# Récupération de l'uuid de l'article dans le cache du corpus
	try:
		F2_article_uri = she(cache_tei.get_uuid(
			["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
	except:
		print("l'article ou la livraison", id_article, "(" + id_livraison + ") est introuvable dans les sources TEI")

	for personne in indexation["personnes"]:
		uuid_personne = personne["personnes_id"]["id"]
		E13_indexation_uri = she(cache.get_uuid(["indexations", id_article, "personnes", uuid_personne, "E13 Attribute Assignement"], True))
		t(E13_indexation_uri, a, crm("E13_Attribute_Assignement"))
		t(E13_indexation_uri, crm("P14_carried_out_by"),
		  she("684b4c1a-be76-474c-810e-0f5984b47921"))
		t(E13_indexation_uri, crm("P140_assigned_attribute_to"), F2_article_uri)
		t(E13_indexation_uri, crm("P141_assigned"), she(uuid_personne))
		t(E13_indexation_uri, crm("P177_assigned_property_type"), crm("P67_refers_to"))

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

serialization = output_graph.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "wb") as f:
	f.write(serialization)

cache.bye()
