import argparse
import glob
from pathlib import Path
import ntpath
from pprint import pprint
from sherlockcachemanagement import Cache
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join('directus/referentiels-ancien-regime/', '')))
from delete_and_send_data import delete, send_data, send_indexations

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--txt")
parser.add_argument("--cache_personnes")
parser.add_argument("--cache_lieux")
parser.add_argument("--cache_mots_clefs")
parser.add_argument("--cache_stagiaires")
parser.add_argument("--cache_congregations")
parser.add_argument("--json_indexations_personnes")
parser.add_argument("--json_indexations_lieux")
parser.add_argument("--json_indexations_institutions")
parser.add_argument("--json_indexations_congregations")
parser.add_argument("--json_indexations_mots_clefs")

args = parser.parse_args()

# CACHES
cache_personnes = Cache(args.cache_personnes)
cache_lieux = Cache(args.cache_lieux)
cache_congregations = Cache(args.cache_congregations)
cache_mots_clefs = Cache(args.cache_mots_clefs)

indexations_personnes = []
indexations_lieux = []
indexations_oeuvres = []
indexations_mots_clefs = []
indexations_congregations = []
indexations_institutions = []

##############################################################################################
# CREATION DU DICTIONNAIRE
# (la fonction crée un dictionnaire pour chaque article et ses indexations
# puis réunit tous les articles et leurs indexations dans un second dictionnaire)
##############################################################################################

def make_json(cache, referentiel, article, indexations):
	id = line[1].strip().replace("\n", "")
	try:
		uuid = cache.get_uuid([referentiel, id, "uuid"])
		item = {
			"item": uuid,
			"sources_articles_id": id_article,
			"collection": referentiel
		}

		article["indices"].append(item)
		indexations.append(article)

	except:
		print(line[1], ": introuvable dans le cache des", referentiel)


# Fichiers TXT contenant les indexations

for file in glob.glob(args.txt + '**/*.txt', recursive=True):
	with open(file, "r") as f:
		lines = f.readlines()

		id_article = ntpath.basename(file)[0:-4]

		# Création d'un dictionnaire par article et par référentiel, contenant l'id de l'article et ses indexations

		article_personnes = {"id": id_article, "indices": []}
		article_lieux = {"id": id_article, "indices": []}
		article_congregations = {"id": id_article, "indices": []}
		article_mots_clefs = {"id": id_article, "indices": []}

		for line in lines:
			line = line.split("=")

			# Exécution de la fonction make_json() pour chaque référentiel
			# à l'exception du ref. des lieux, dont le cache est différent

			if line[0] == "personnes":
				make_json(cache_personnes, "personnes", article_personnes, indexations_personnes)


			if line[0] == "congrégations":
				make_json(cache_congregations, "congrégations", article_congregations, indexations_congregations)


			if line[0] == "mots clés":
				make_json(cache_mots_clefs, "mots-clefs", article_mots_clefs, indexations_mots_clefs)


			if line[0] == "lieux":
				id = line[1].strip().replace("\n", "")
				try:
					uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"])
					item = {
						"item": uuid,
						"sources_articles_id": id_article,
						"collection": "lieux"
					}

					article_lieux["indices"].append(item)
					indexations_lieux.append(article_lieux)

				except:
					print(line[1], ": introuvable dans le cache des lieux")


			# TODO Pas de référentiel des oeuvres citées

			# TODO Pas de référentiel des institutions (il doit être entièrement remanié dans Directus)


#########################################################################################
## CREATION DES FICHIERS JSON
#########################################################################################

with open(args.json_indexations_personnes, 'w', encoding="utf-8") as file:
	json.dump(indexations_personnes, file, ensure_ascii=False)

with open(args.json_indexations_lieux, 'w', encoding="utf-8") as file:
	json.dump(indexations_lieux, file, ensure_ascii=False)

with open(args.json_indexations_congregations, 'w', encoding="utf-8") as file:
	json.dump(indexations_congregations, file, ensure_ascii=False)

with open(args.json_indexations_mots_clefs, 'w', encoding="utf-8") as file:
	json.dump(indexations_mots_clefs, file, ensure_ascii=False)

print("\nECRITURE DES FICHIERS JSON TERMINEE\n")

#########################################################################################
## ENVOI DES DONNEES
#########################################################################################

# send_indexations(json_indexations_personnes)
# send_indexations(json_indexations_lieux)
# send_indexations(json_indexations_congregations)
# send_indexations(json_indexations_mots_clefs)
