from rdflib import Graph, Literal
from rdflib.plugins import sparql
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_ttl")
parser.add_argument("--input_txt")
args = parser.parse_args()

############################################################################################
# RECHERCHE DES CONGREGATIONS DONT L'ALIGNEMENT AU REFERENTIEL DES LIEUX N'A PAS FONCTIONNE
############################################################################################

input_graph = Graph()
input_graph.load(args.input_ttl, format="turtle")

file = open(args.input_txt, "r", encoding="utf-8")

list = file.readlines()
for id in list:
	concept_id = Literal(id.rstrip())

	q = sparql.prepareQuery("""
		SELECT ?concept_id
		WHERE {
		?concept <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?identifier .
		?identifier <http://www.w3.org/2000/01/rdf-schema#label> ?concept_id .
		FILTER NOT EXISTS {
		?concept <http://data-iremus.huma-num.fr/ns/sherlock#geohistorical_situation> ?lieu .
		}
		}
		""")

	for row in input_graph.query(q, initBindings={'concept_id': concept_id}):
		print("Alignement raté (lieu introuvable dans le cache) :",  row[0])

