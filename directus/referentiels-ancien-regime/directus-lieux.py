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
from delete_and_send_data import delete, send_data

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--cache_lieux")
parser.add_argument("--skos")
parser.add_argument("--json_lieux")
parser.add_argument("--json_indexations")
args = parser.parse_args()

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

# RECUPERATION DES DONNEES SKOS
for opentheso_lieu_uri, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):

	# Dictionnaire des concepts et de leurs informations
	dict_infos_lieu = {}

	id = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.identifier))[0].value

	# UUID
	try:
		uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"])
		dict_infos_lieu["id"] = uuid
	except:
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

	data_lieux.append(dict_infos_lieu)

	# Coordonnées
	geolat = list(input_graph.objects(opentheso_lieu_uri, u("http://www.w3.org/2003/01/geo/wgs84_pos#lat")))
	geolong = list(input_graph.objects(opentheso_lieu_uri, u("http://www.w3.org/2003/01/geo/wgs84_pos#lat")))
	if len(geolat) >= 1 and len(geolong) >= 1:
		dict_infos_lieu["latitude"] = str(geolat[0].value)
		dict_infos_lieu["longitude"] = str(geolong[0].value)

	# Période historique
	periode = list(input_graph.objects(opentheso_lieu_uri, DCTERMS.description))[0].value[:4]
	if periode == "1336":
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
			dict_infos_lieu["fusion"] = [f for f in fusion_list]
	else:
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
			dict_infos_lieu["etat_actuel"] = [{
				"etat_actuel_id": e,
				"lieux_id": uuid,
				"collection": "lieux"
			} for e in etat_actuel_list]


	# Parent
	# parents = list(input_graph.objects(opentheso_lieu_uri, SKOS.broader))
	# if len(parents) >= 1:
	# 	parents_list = []
	# 	for parent in parents:
	# 		parent = parent.split("idc=")[1].split("&")[0]
	# 		if parent == "1336" or parent == "275949":
	# 			pass
	# 		else:
	# 			try:
	# 				# On va chercher l'UUID du parent s'il existe
	# 				parent_uuid = cache_lieux.get_uuid(["lieux", parent, "E93", "uuid"])
	# 				parents_list.append(parent_uuid)
	# 			except:
	# 				# On crée l'UUID du parent s'il n'existe pas
	# 				parent_uuid = cache_lieux.get_uuid(["lieux", parent, "E93", "uuid"], True)
	# 				parents_list.append(parent_uuid)
	# 	dict_infos_lieu["parent"] = [{
	# 				"parent_id": p,
	# 				"lieux_id": uuid,
	# 				"collection": "lieux"
	# 			} for p in parents_list]


#########################################################################################
## INDEXATIONS
#########################################################################################

data_indexations = []

for k, v in dict_indexations.items():
	dict_infos_index = {
		"id": k,
		"indices": [{
			"item": i,
			"sources_articles_id": k,
			"collection": "lieux"
		} for i in v]
	}

	data_indexations.append(dict_infos_index)

#########################################################################################
## CREATION DES FICHIERS JSON
#########################################################################################

with open(args.json_lieux, 'w', encoding="utf-8") as file:
	json.dump(data_lieux, file, ensure_ascii=False)

with open(args.json_indexations, 'w', encoding="utf-8") as file:
	json.dump(data_indexations, file, ensure_ascii=False)

#########################################################################################
## ENVOI DES DONNEES
#########################################################################################

# LIEUX
delete("lieux")

with open(args.json_lieux) as json_file:
	data_lieux = json.load(json_file)
	send_data(data_lieux, "lieux", 1, 5300, 5338)

# # INDEXATIONS
#
# # Récupération des données de la collection
# print("""
#
# ##########################################################################################
#
# COLLECTION 'SOURCES ARTICLES'
#
# Récupération des données:""")
# r = requests.get(secret["url"] + '/items/sources_articles?limit=-1&access_token=' + access_token)
# print(r)
#
# ids = [item["id"] for item in r.json()["data"]]
#
# # Ajout de données à la collection (patch)
# with open(args.json_index) as json_file:
# 	sources_articles = json.load(json_file)
#
# 	for sa in sources_articles:
# 		r = requests.get(secret["url"] + '/items/sources_articles/'+sa["id"]+'?access_token=' + access_token)
# 		if r.status_code == 200:
# 			r = requests.patch(secret["url"] + '/items/sources_articles/' + sa["id"] + '?access_token=' + access_token, json=sa)
# 		else:
# 			r = requests.post(secret["url"] + '/items/sources_articles?access_token=' + access_token, json=sa)
# 		print(r.json())