import json
import subprocess
from subprocess import call
from rdflib import Graph, Literal, RDF, RDFS, SKOS, DCTERMS, URIRef as u
from rdflib.plugins import sparql
import argparse
from sherlockcachemanagement import Cache
from pprint import pprint
import time
import sys
import os
import requests
import yaml
from delete_and_send_data import delete, send_data, send_indexations

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--cache_lieux")
parser.add_argument("--skos")
parser.add_argument("--json_lieux")
parser.add_argument("--json_lieux_relations")
parser.add_argument("--json_indexations")
args = parser.parse_args()

# Secret YAML pour les requêtes Directus
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login", json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Caches
cache_lieux = Cache(args.cache_lieux)

# Initialisation du graphe
input_graph = Graph()
input_graph.load(args.skos)

# Dictionnaire de l'indexation des sources par le référentiel des lieux
dict_indexations = {}

# Dictionnaire de correspondance lieu-période
lieu_periode = {}

#########################################################################################
## LIEUX
#########################################################################################

data_lieux = []
data_lieux_relations = []

# RECUPERATION DES DONNEES SKOS
for opentheso_lieu_uri, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):

	# Dictionnaire contenant les informations simples d'un lieu
	dict_infos_lieu = {}

	id = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.identifier))[0].value

	# UUID
	uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"], True)
	dict_infos_lieu["id"] = uuid

	# PrefLabel
	label = list(input_graph.objects(opentheso_lieu_uri, SKOS.prefLabel))[0].value
	dict_infos_lieu["label"] = label

	# Définition
	definitions = list(input_graph.objects(opentheso_lieu_uri, SKOS.definition))
	if len(definitions) >= 1:
		dict_infos_lieu["definition"] = definitions[0].value
	else:
		pass

	# Notes/indexation
	for p in [SKOS.editorialNote, SKOS.historyNote, SKOS.note, SKOS.scopeNote]:
		notes_opentheso = list(input_graph.objects(opentheso_lieu_uri, p))
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
				dict_infos_lieu["ref_iremus"] = note

			elif "Hortus :" in note or "Hortus:" in note:
				dict_infos_lieu["ref_hortus"] = note

			else:
				dict_infos_lieu["note_historique"] = note

		else:
			pass


	# Altlabels
	altlabels = list(input_graph.objects(opentheso_lieu_uri, SKOS.altLabel))
	if len(altlabels) >= 1:
		n = 1
		clé = "alt_label_" + str(n)
		for altlabel in altlabels:
			while clé in dict_infos_lieu.keys():
				n += 1
				clé = "alt_label_"+str(n)
			dict_infos_lieu[clé] = altlabel.value


	# Coordonnées
	geolat = list(input_graph.objects(opentheso_lieu_uri, u("http://www.w3.org/2003/01/geo/wgs84_pos#lat")))
	geolong = list(input_graph.objects(opentheso_lieu_uri, u("http://www.w3.org/2003/01/geo/wgs84_pos#long")))
	if len(geolat) >= 1 and len(geolong) >= 1:
		dict_infos_lieu["coordonnees_geographiques"] = {"coordinates": [str(geolong[0].value), str(geolat[0].value)], "type": "Point"}

	# ExactMatch
	exactMatches = list(input_graph.objects(opentheso_lieu_uri, SKOS.exactMatch))
	if len(exactMatches) >= 1:
		for exactMatch in exactMatches:
			if "geonames" in exactMatch:
				dict_infos_lieu["geonames_alignement"] = "<a href='" + exactMatch + "'> Identifiant Geonames</a>"
			else:
				dict_infos_lieu["cassini_alignement"] = "<a href='" + exactMatch + "'> Identifiant Cassini</a>"
		# CloseMatch
	closeMatches = list(input_graph.objects(opentheso_lieu_uri, SKOS.closeMatch))
	if len(closeMatches) >= 1:
		for closeMatch in closeMatches:
			if "geonames" in closeMatch:
				dict_infos_lieu["geonames_voir_aussi"] = "<a href='" + closeMatch + "'> Identifiant Geonames</a>"
			else:
				dict_infos_lieu["cassini_voir_aussi"] = "<a href='" + closeMatch + "'> Identifiant Cassini</a>"

	# Période historique
	periode = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.description))[0].value[:4]
	if periode == "1336":
		lieu_periode[id] = "Grand Siècle"
		dict_infos_lieu["periode_historique"] = "grand_siecle"
	else:
		lieu_periode[id] = "Monde Contemporain"
		dict_infos_lieu["periode_historique"] = "monde_contemporain"

	data_lieux.append(dict_infos_lieu)


# Relations (parents, fusion, état actuel) (requêtes PATCH)
for opentheso_lieu_uri, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):

	id = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.identifier))[0].value
	uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"], True)

	# Dictionnaire contenant les informations relationnelles d'un lieu
	dict_relations_lieu = {}
	dict_relations_lieu["id"] = uuid

	# Parents
	parents = list(input_graph.objects(opentheso_lieu_uri, SKOS.broader))
	if len(parents) >= 1:
		parents_list = []
		for parent in parents:
			parent = parent.split("idc=")[1].split("&")[0]
			parent_uuid = cache_lieux.get_uuid(["lieux", parent, "E93", "uuid"], True)
			parents_list.append(parent_uuid)

		dict_relations_lieu["parents"] = [{
					"parent_id": p,
					"lieu_id": uuid
				} for p in parents_list]

	# Lien à un autre lieu (SKOS.related)
	periode = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.description))[0].value
	
	# S'il s'agit d'un lieu du Monde Contemporain...
	if "275949#" in periode:
		related_places = list(input_graph.objects(opentheso_lieu_uri, SKOS.related))
		if len(related_places) >= 1:
			fusions_list = []
			etats_anterieurs_list = []

			for place in related_places:
				place_id = place.split("idc=")[1].split("&")[0]
				if lieu_periode[place_id] == "Monde Contemporain":
					# Il s'agit d'une fusion
					fusion_uuid = cache_lieux.get_uuid(["lieux", place_id, "E93", "uuid"], True)
					fusions_list.append(fusion_uuid)
				else:
					# Le lien lieu du Monde Contempo/lieu du Grand Siècle est répété dans les deux sens
					# et traité dans la boucle suivante
					pass
			
			dict_relations_lieu["fusions"] = [{
					"fusion_id": f,
					"lieu_id": uuid
				} for f in fusions_list]

	# S'il s'agit d'un lieu du Grand Siècle
	if "1336#" in periode:
		etats_actuels = list(input_graph.objects(opentheso_lieu_uri, SKOS.related))
		if len(etats_actuels) >= 1:
			etats_actuels_list = []
			for e in etats_actuels:
				e = e.split("idc=")[1].split("&")[0]
				etat_actuel_uuid = cache_lieux.get_uuid(["lieux", e, "E93", "uuid"], True)
				etats_actuels_list.append(etat_actuel_uuid)
			dict_relations_lieu["etats_actuels"] = [{
				"etat_actuel_id": etat_actuel,
				"lieu_id": uuid
			} for etat_actuel in etats_actuels_list]

	data_lieux_relations.append(dict_relations_lieu)

cache_lieux.bye()

#########################################################################################
## INDEXATIONS
#########################################################################################
#
data_indexations = []

for k, v in dict_indexations.items():
	dict_infos_index = {
		"id": k,
		"lieux": [{
			"lieu_id": i,
			"source_article_id": k
		} for i in v]
	}

	data_indexations.append(dict_infos_index)

#########################################################################################
## CREATION DES FICHIERS JSON
#########################################################################################

#with open(args.json_lieux, 'w', encoding="utf-8") as file:
#	json.dump(data_lieux, file, ensure_ascii=False)
#
#with open(args.json_lieux_relations, 'w', encoding="utf-8") as file:
#	json.dump(data_lieux_relations, file, ensure_ascii=False)

#with open(args.json_indexations, 'w', encoding="utf-8") as file:
#	json.dump(data_indexations, file, ensure_ascii=False)
#
#print("\nECRITURE DES FICHIERS JSON TERMINEE\n")

#########################################################################################
## ENVOI DES DONNEES
#########################################################################################

# LIEUX
#print("\nSUPPRESSION DES ITEMS DE LA COLLECTION")
#delete("lieux_etats_actuels")
#delete("lieux_fusions")
#delete("lieux_parents")
#delete("sources_articles_lieux")
#delete("lieux")

#with open(args.json_lieux) as json_file:
#	data_lieux = json.load(json_file)
#	send_data(data_lieux, "lieux", 1, 0, 0)

#Patch des relations entre un lieu et un/plusieurs autres
with open(args.json_lieux_relations) as json_file:
	data_lieux_relations = json.load(json_file)
	print("\nENVOI DES DONNEES RELATIONNELLES\n")
	print(len(data_lieux_relations), "données à envoyer")
	n = 483
	for item in data_lieux_relations[n:]:
		print(n)
		try:
			r = requests.patch(secret["url"] + '/items/lieux/' + item["id"] + '?access_token=' + access_token, json=item)
			print(r)
		except Exception as e:
			print(e)
			print(r.json())
		n += 1
#
## INDEXATIONS
#send_indexations(args.json_indexations)