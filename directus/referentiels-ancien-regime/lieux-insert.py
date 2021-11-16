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

#########################################################################################
## LIEUX
#########################################################################################

data_lieux = []
data_lieux_relations = []

# RECUPERATION DES DONNEES SKOS
for opentheso_lieu_uri, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):

	# Dictionnaire contenant les informations simples d'un lieu
	dict_infos_lieu = {}
	# Dictionnaire contenant les informations relationnelles d'un lieu
	dict_relations_lieu = {}

	id = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.identifier))[0].value

	# UUID
	try:
		uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"])
		dict_infos_lieu["id"] = uuid
		dict_relations_lieu["id"] = uuid

	except:
		uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"], True)
		dict_infos_lieu["id"] = uuid
		dict_relations_lieu["id"] = uuid

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
	geolong = list(input_graph.objects(opentheso_lieu_uri, u("http://www.w3.org/2003/01/geo/wgs84_pos#lat")))
	if len(geolat) >= 1 and len(geolong) >= 1:
		dict_infos_lieu["latitude"] = str(geolat[0].value)
		dict_infos_lieu["longitude"] = str(geolong[0].value)

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
		dict_infos_lieu["periode_historique"] = "Grand Siècle"
		# Etat actuel du lieu (lien entre Ancien Régime et Monde contemporain)
		etat_actuel = list(input_graph.objects(opentheso_lieu_uri, SKOS.related))
		if len(etat_actuel) >= 1:
			etat_actuel_list = []
			for e in etat_actuel:
				e = e.split("idc=")[1].split("&")[0]
				try:
					etat_actuel_uuid = cache_lieux.get_uuid(["lieux", e, "E93", "uuid"])
					etat_actuel_list.append(etat_actuel_uuid)
				except:
					etat_actuel_uuid = cache_lieux.get_uuid(["lieux", e, "E93", "uuid"], True)
					etat_actuel_list.append(etat_actuel_uuid)
			dict_relations_lieu["etat_actuel"] = [{
				"etat_actuel_id": e,
				"lieu_id": uuid
			} for e in etat_actuel_list]
	else:
		dict_infos_lieu["periode_historique"] = "Monde Contemporain"
		# Evenement de fusion du lieu en un autre (seulement pour Monde Contemporain)
		fusion = list(input_graph.objects(opentheso_lieu_uri, SKOS.related))
		if len(fusion) >= 1:
			fusion_list = []
			for f in fusion:
				f = f.split("idc=")[1].split("&")[0]
				try:
					fusion_uuid = cache_lieux.get_uuid(["lieux", f, "E93", "uuid"])
				except:
					fusion_uuid = cache_lieux.get_uuid(["lieux", f, "E93", "uuid"], True)
				fusion_list.append(fusion_uuid)
			dict_relations_lieu["fusion"] = [{
				"fusion_id": f,
				"lieux_id": uuid
			} for f in fusion_list]


	# Parent
	parents = list(input_graph.objects(opentheso_lieu_uri, SKOS.broader))
	if len(parents) >= 1:
		parents_list = []
		for parent in parents:
			parent = parent.split("idc=")[1].split("&")[0]
			if parent == "1336" or parent == "275949":
				pass
			else:
				try:
					# On va chercher l'UUID du parent s'il existe
					parent_uuid = cache_lieux.get_uuid(["lieux", parent, "E93", "uuid"])
					parents_list.append(parent_uuid)
				except:
					# On crée l'UUID du parent s'il n'existe pas
					parent_uuid = cache_lieux.get_uuid(["lieux", parent, "E93", "uuid"], True)
					parents_list.append(parent_uuid)
		dict_relations_lieu["parent"] = [{
					"parent_id": p,
					"lieux_id": uuid
				} for p in parents_list]

	data_lieux.append(dict_infos_lieu)
	data_lieux_relations.append(dict_relations_lieu)

#########################################################################################
## INDEXATIONS
#########################################################################################
#
data_indexations = []

for k, v in dict_indexations.items():
	dict_infos_index = {
		"id": k,
		"lieux": [{
			"lieux_id": i,
			"sources_articles_id": k
		} for i in v]
	}

	data_indexations.append(dict_infos_index)

#########################################################################################
## CREATION DES FICHIERS JSON
#########################################################################################
#
# with open(args.json_lieux, 'w', encoding="utf-8") as file:
# 	json.dump(data_lieux, file, ensure_ascii=False)
#
# with open(args.json_lieux_relations, 'w', encoding="utf-8") as file:
# 	json.dump(data_lieux_relations, file, ensure_ascii=False)
#
# with open(args.json_indexations, 'w', encoding="utf-8") as file:
# 	json.dump(data_indexations, file, ensure_ascii=False)
#
# print("\nECRITURE DES FICHIERS JSON TERMINEE\n")

#########################################################################################
## ENVOI DES DONNEES
#########################################################################################

# LIEUX
# delete("lieux")
#
with open(args.json_lieux) as json_file:
	data_lieux = json.load(json_file)
	# send_data(data_lieux, "lieux", 100, 5300, 5338)

#Patch des relations entre un lieu et un/plusieurs autres
# with open(args.json_lieux_relations) as json_file:
# 	data_lieux_relations = json.load(json_file)
# 	print("\nENVOI DES DONNEES RELATIONNELLES\n")
# 	print(len(data_lieux_relations), "données à envoyer")
# 	n = 0
# 	# Limite à 1800 requêtes d'affilée pour ne pas planter Directus
# 	for item in data_lieux_relations[n:1800]:
# 		print(n)
# 		try:
# 			r = requests.patch(secret["url"] + '/items/lieux/' + item["id"] + '?access_token=' + access_token, json=item)
# 			print(r)
# 		except Exception as e:
# 			print(e)
# 			print(r.json())
# 		n += 1
# 		time.sleep(0.7)

# INDEXATIONS
# send_indexations(args.json_indexations)