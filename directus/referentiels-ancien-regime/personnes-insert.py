import json
import subprocess
from subprocess import call
from rdflib import Graph, Literal, RDF, RDFS, SKOS, DCTERMS
from rdflib.plugins import sparql
import argparse
from sherlockcachemanagement import Cache
from pprint import pprint
import time
import sys
from delete_and_send_data import delete, send_data, send_indexations

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--cache_personnes")
parser.add_argument("--skos")
parser.add_argument("--json_personnes")
parser.add_argument("--json_indexations")
args = parser.parse_args()

# Caches
cache_personnes = Cache(args.cache_personnes)

# Initialisation du graphe
input_graph = Graph()
input_graph.load(args.skos)

# Dictionnaire de l'indexation des sources par le référentiel des personnes
dict_indexations = {}

#########################################################################################
## PERSONNES
#########################################################################################

data_personnes = []

# RECUPERATION DES DONNEES SKOS
print("RECUPERATION DES DONNEES SKOS\n")

for opentheso_personne_uri, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):

	# Dictionnaire des concepts et de leurs informations
	dict_infos_personne = {}

	id = list(input_graph.objects(opentheso_personne_uri, DCTERMS.identifier))[0].value

	# uuid
	try:
		uuid = cache_personnes.get_uuid(["personnes", id, "uuid"])
		dict_infos_personne["id"] = uuid
	except:
		uuid = cache_personnes.get_uuid(["personnes", id, "uuid"], True)
		dict_infos_personne["id"] = uuid

	# prefLabel
	label = list(input_graph.objects(opentheso_personne_uri, SKOS.prefLabel))[0].value
	dict_infos_personne["label"] = label

	# définition
	definitions = list(input_graph.objects(opentheso_personne_uri, SKOS.definition))
	if len(definitions) >= 1:
		dict_infos_personne["definition"] = definitions[0].value
	else:
		pass

	# notes/indexation
	for p in [SKOS.editorialNote, SKOS.historyNote, SKOS.note, SKOS.scopeNote]:
		notes_opentheso = list(input_graph.objects(opentheso_personne_uri, p))
		if len(notes_opentheso) >= 1:
			note = notes_opentheso[0].value

			# balises dans les notes à supprimer
			balises_a_supprimer = ["&amp;nbsp;", "<p class= ql-align-justify >", "<br>",
			"</span>", "</p>", "<span style= color: black; >", "<span style= color: rgb(102, 102, 102); >",
			"<span style= color: rgb(0, 0, 0); >", "<span style= color: rgb(80, 80, 80); >",
			"<span style= color: rgb(191, 191, 191); >", "<p>"]
			for balise in balises_a_supprimer:
				if balise in note:
					note = note.replace(balise, "")

			# Insertion d'un lien URL à la place des références aux articles Obvil
			#TODO Revoir la route de l'URL
			if "cf. MG-" in note:
				note = note.replace("cf. ", "cf. http://data-iremus.huma-num.fr/")

			# récupération des indexations_to_ttl
			elif "##" in note:
				indexations = note.split("##")
				for indexation in indexations:
					if "MG" in indexation:
						indexation = indexation.replace("\r", "").strip()

						if indexation not in dict_indexations:
							dict_indexations[indexation] = []
						dict_indexations[indexation].append(uuid)

			elif "IReMus :" in note or "IReMus:" in note:
				dict_infos_personne["ref_iremus"] = note

			elif "Hortus :" in note or "Hortus:" in note:
				dict_infos_personne["ref_hortus"] = note

			else:
				dict_infos_personne["note_historique"] = note

		else:
			pass

	# récupération des Altlabels
	altlabels = list(input_graph.objects(opentheso_personne_uri, SKOS.altLabel))
	if len(altlabels) >= 1:
		n = 1
		clé = "alt_label_" + str(n)
		for altlabel in altlabels:
			while clé in dict_infos_personne.keys():
				n += 1
				clé = "alt_label_"+str(n)
			dict_infos_personne[clé] = altlabel

	data_personnes.append(dict_infos_personne)


	# exactMatch
	exactMatches = list(input_graph.objects(opentheso_personne_uri, SKOS.exactMatch))
	if len(exactMatches) >= 1:
		for exactMatch in exactMatches:
			if "catalogue.bnf" in exactMatch:
				dict_infos_personne["catalogue_bnf_alignement"] = f"<a href='{exactMatch}'>{exactMatch}</a>"
			if "viaf" in exactMatch:
				dict_infos_personne["viaf_alignement"] = f"<a href='{exactMatch}'>{exactMatch}</a>"
			if "versailles" in exactMatch:
				dict_infos_personne["versailles_alignement"] = f"<a href='{exactMatch}'>{exactMatch}</a>"
			if "isni" in exactMatch:
				dict_infos_personne["isni_alignement"] = f"<a href='{exactMatch}'>{exactMatch}</a>"
			if "data.bnf" in exactMatch:
				dict_infos_personne["data_bnf_alignement"] = f"<a href='{exactMatch}'>{exactMatch}</a>"


#########################################################################################
## INDEXATIONS
#########################################################################################

data_indexations = []

for k, v in dict_indexations.items():
	dict_infos_index = {
		"id": k,
		"personnes": [{
			"personnes_id": i,
			"sources_articles_id": k
		} for i in v]
	}

	data_indexations.append(dict_infos_index)

#########################################################################################
## CREATION DES FICHIERS JSON
#########################################################################################

# print("\nECRITURE DES FICHIERS JSON\n")

# with open(args.json_personnes, 'w', encoding="utf-8") as file:
# 	json.dump(data_personnes, file, ensure_ascii=False)
#
# with open(args.json_indexations, 'w', encoding="utf-8") as file:
# 	json.dump(data_indexations, file, ensure_ascii=False)

#########################################################################################
## ENVOI DES DONNEES
#########################################################################################

#PERSONNES
# print("\nSUPPRESSION DES ITEMS DE LA COLLECTION 'PERSONNES'\n")
# delete("personnes")

# print("\nENVOI DES NOUVEAUX ITEMS DANS LA COLLECTION 'PERSONNES'\n")
# with open(args.json_personnes) as json_file:
# 	data_personnes = json.load(json_file)
# 	send_data(data_personnes, "personnes", 1, 5200, 5449)

print("\nENVOI DES INDEXATIONS DANS LA COLLECTION 'SOURCES_ARTICLES'\n")
# INDEXATIONS
send_indexations(args.json_indexations)