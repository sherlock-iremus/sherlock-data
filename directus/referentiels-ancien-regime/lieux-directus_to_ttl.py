from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import argparse
from pprint import pprint
from sherlockcachemanagement import Cache
import requests
import os
import sys
import yaml
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


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
r = requests.post(secret["url"] + "/auth/login", json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url=secret["url"] + '/graphql' + '?access_token=' + access_token)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

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
## DONNEES STATIQUES
############################################################################################

E32_lieux_uri = u(iremus_ns["947a38f0-34ac-4c54-aeb7-69c5f29e77c0"])
t(E32_lieux_uri, a, crm("E32_Authority_Document"))
t(E32_lieux_uri, crm("P1_is_identified_by"), l("Lieux"))

E52_GrandSiecle_uri = she(cache.get_uuid(["lieux", "E52 Grand Siècle"], True))
t(E52_GrandSiecle_uri, a, crm("E52_Time-Span"))
t(E52_GrandSiecle_uri, crm("P1_is_identified_by"), l("Grand Siècle"))

E52_MondeContemp_uri = she(cache.get_uuid(["lieux", "E52 Monde contemporain"], True))
t(E52_MondeContemp_uri, a, crm("E52_Time-Span"))
t(E52_MondeContemp_uri, crm("P1_is_identified_by"), l("Monde Contemporain"))

############################################################################################
## RECUPERATION DES DONNEES DANS DIRECTUS
############################################################################################

print("RECUPERATION DES DONNEES DE DIRECTUS")

query = gql("""
query ($page_size: Int) {
	lieux(limit: 500, offset: $page_size) {
		id
		label
		parent {
		parent_id {
			id
		}
		}
		periode_historique
		note_historique
		alt_label_1
		alt_label_2
		etat_actuel {
			etat_actuel_id {
			id
			label
		}
		}
		fusion {
		fusion_id {
			id
			label
		}
		}
		cassini_alignement
		cassini_voir_aussi
		geonames_alignement
		geonames_voir_aussi
		coordonnees_geographiques
  }
}
""")

page_size = 0

while True:

	response = client.execute(query, variable_values= {"page_size": page_size} )

	#--------------------------------------------------------------------------------------
	# CREATION DES TRIPLETS
	#--------------------------------------------------------------------------------------
	
	for lieu in response["lieux"]:
	
		if lieu["label"] == "Grand Siècle" or lieu["label"] == "Monde contemporain":
			continue

		E93_uri = she(lieu["id"])
		t(E93_uri, a, crm("E93_Presence"))
		t(E32_lieux_uri, crm("P71_lists"), E93_uri)

		# PrefLabel
		E41_uri = she(cache.get_uuid(["lieux", E93_uri, "E41"], True))
		t(E93_uri, crm("P1_is_identified_by"), E41_uri)
		t(E41_uri, a, crm("E41_Appellation"))
		t(E41_uri, RDFS.label, l(lieu["label"]))
		t(E41_uri, crm("P2_has_type"), she("3cf0c743-ee9b-4dfc-8133-7dd383a1b6be"))

		# AltLabels
		n = 1
		clé = "alt_label_" + str(n)
		while clé in lieu.keys():
			altlabel = lieu[clé]
			if altlabel != None:
				E41_alt_uri = she(cache.get_uuid(["lieux", E93_uri, "E41 alt", altlabel], True))
				t(E41_alt_uri, a, crm("E41_Appellation"))
				t(E41_alt_uri, RDFS.label, l(altlabel))
				t(E93_uri, crm("P1_is_identified_by"), E41_alt_uri)
				t(E41_alt_uri, crm("P2_has_type"), she("70589b95-4156-431e-a58a-818af6dc795a"))
			n += 1
			clé = "alt_label_" + str(n)

		# Période historique
		if lieu["periode_historique"] == "grand_siecle":
			E13_E52_GS_uri = she(cache.get_uuid(["lieux", E93_uri, "E52 Grand Siècle", "E13"], True))
			t(E13_E52_GS_uri, a, crm("E13_Attribute_Assignement"))
			t(E13_E52_GS_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(E13_E52_GS_uri, crm("P140_assigned_attribute_to"), E93_uri)
			t(E13_E52_GS_uri, crm("P141_assigned"), E52_GrandSiecle_uri)
			t(E13_E52_GS_uri, crm("P177_assigned_property_type"), crm("P4_has_time-span"))
		else:
			E13_E52_MC_uri = she(cache.get_uuid(["lieux", E93_uri, "E52 Monde Contemporain", "E13"], True))
			t(E13_E52_MC_uri, a, crm("E13_Attribute_Assignement"))
			t(E13_E52_MC_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(E13_E52_MC_uri, crm("P140_assigned_attribute_to"), E93_uri)
			t(E13_E52_MC_uri, crm("P141_assigned"), E52_MondeContemp_uri)
			t(E13_E52_MC_uri, crm("P177_assigned_property_type"), crm("P4_has_time-span"))
		
		# Note historique
		if lieu["note_historique"] != None:
			E13_note_uri = she(cache.get_uuid(["lieux", E93_uri, "note historique", "E13"], True))
			t(E13_note_uri, a, crm("E13_Attribute_Assignement"))
			t(E13_note_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(E13_note_uri, crm("P140_assigned_attribute_to"), E93_uri)
			t(E13_note_uri, crm("P141_assigned"), l(lieu["note_historique"]))
			t(E13_note_uri, crm("P177_assigned_property_type"), crm("P3_has_note"))

		# Alignements
		def alignement(champ, predicat):
			if lieu[champ] != None:
				try:
					url_alignement = lieu[champ].split("'>")[1]
					url_alignement = url_alignement.replace("</a>", "").replace("</p>", "")
					t(E93_uri, predicat, u(url_alignement))
				except:
					try:
						url_alignement = lieu[champ].split('">')[1]
						url_alignement = url_alignement.replace("</a>", "").replace("</p>", "")
						t(E93_uri, predicat, u(url_alignement))
					except:
						print(lieu[champ])

		alignement("cassini_alignement", SKOS.exactMatch)
		alignement("geonames_alignement", SKOS.exactMatch)
		alignement("cassini_voir_aussi", SKOS.closeMatch)
		alignement("geonames_voir_aussi", SKOS.closeMatch)

		# Parents
		if lieu["parent"] != None:
			for parent in lieu["parent"]:
				E13_parent_uri = she(cache.get_uuid(["lieux", E93_uri, "parent", "E13"], True))
				t(E13_parent_uri, a, crm("E13_Attribute_Assignement"))
				t(E13_parent_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(E13_parent_uri, crm("P140_assigned_attribute_to"), E93_uri)
				t(E13_parent_uri, crm("P141_assigned"), she(parent["parent_id"]["id"]))
				t(E13_parent_uri, crm("P177_assigned_property_type"), crm("P10_falls_within"))

		# Etats actuels (E4_Period)
		def link_to_E4(uri):
			E13_E4_uri = she(cache.get_uuid(["lieux", uri, "E4", "E13"], True))
			t(E13_E4_uri, a, crm("E13_Attribute_Assignement"))
			t(E13_E4_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(E13_E4_uri, crm("P140_assigned_attribute_to"), uri)
			t(E13_E4_uri, crm("P141_assigned"), E4_uri)
			t(E13_E4_uri, crm("P177_assigned_property_type"), crm("P166_was_a_presence_of"))

		if lieu["etat_actuel"] != None:
			for etat_actuel in lieu["etat_actuel"]:
				E4_label = etat_actuel["etat_actuel_id"]["label"] + " / " + lieu["label"]
				E4_uri = she(cache.get_uuid(["lieux", E93_uri, "E4", "uuid"], True))
				t(E4_uri, a, crm("E4_Period"))
				t(E4_uri, crm("is_identified_by"), l(E4_label))

				link_to_E4(E93_uri)
				link_to_E4(she(etat_actuel["etat_actuel_id"]["id"]))

		# Fusions
		if lieu["fusion"] != None:
			pass

		# Coordonnées géographiques
		if lieu["coordonnees_geographiques"] != None:
			coordonnees = lieu["coordonnees_geographiques"]["coordinates"]
			coordonnees = str(coordonnees)[1:-1]
				
			E53_uri = she(cache.get_uuid(["lieux", E93_uri, "E53", "uuid"], True))
			t(E53_uri, a, crm("E53_Place"))
			t(E53_uri, crm("P168_place_is_defined_by"), l(coordonnees))

			E13_E53_uri = she(cache.get_uuid(["lieux", E93_uri, "E53", "E13"], True))
			t(E13_E53_uri, a, crm("E13_Attribute_Assignement"))
			t(E13_E53_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(E13_E53_uri, crm("P140_assigned_attribute_to"), E93_uri)
			t(E13_E53_uri, crm("P141_assigned"), E53_uri)
			t(E13_E53_uri, crm("P177_assigned_property_type"), crm("P161_has_spatial_projection"))


	print(page_size, "lieux traités")
	page_size += 500

	if not response["lieux"]:
		break


############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

print("\nECRITURE DU FICHIER TTL")

serialization = output_graph.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "wb") as f:
	f.write(serialization)

cache.bye()