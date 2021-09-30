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
parser.add_argument("--json_indexations_stagiaires")

args = parser.parse_args()

# CACHES
cache_personnes = Cache(args.cache_personnes)
cache_lieux = Cache(args.cache_lieux)
cache_congregations = Cache(args.cache_congregations)
cache_mots_clefs = Cache(args.cache_mots_clefs)

# Création de la liste de dictionnaires qui constituera le body de la requête
indexations_stagiaires = []

# Fichiers TXT contenant les indexations
for file in glob.glob(args.txt + '**/*.txt', recursive=True):
	with open(file, "r") as f:
		lines = f.readlines()

		id_article = ntpath.basename(file)[0:-4]

		dict = {"id": id_article}

		for line in lines:
			line = line.split("=")

			# Création d'une liste par thésaurus recueillant tous les uuid indexés
			personnes = []
			congregations = []
			lieux = []
			mots_clefs = []

			if line[0] == "personnes":
				id = line[1].strip().replace("\n", "")
				try:
					# Récupération de l'uuid
					uuid = cache_personnes.get_uuid(["personnes", id, "uuid"])
					personnes.append(uuid)
				except:
					print(line[1], ": introuvable dans le cache des personnes")

			if line[0] == "congrégations":
				id = line[1].strip().replace("\n", "")
				try:
					# Récupération de l'uuid
					uuid = cache_congregations.get_uuid(["congrégations", id, "uuid"])
					congregations.append(uuid)
				except:
					print(line[1], ": introuvable dans le cache des congrégations")

			if line[0] == "lieux":
				id = line[1].strip().replace("\n", "")
				try:
					# Récupération de l'uuid
					uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"])
					lieux.append(uuid)
				except:
					print(line[1], ": introuvable dans le cache des lieux")

			if line[0] == "mots clés":
				id = line[1].strip().replace("\n", "")
				try:
					# Récupération de l'uuid
					uuid = cache_mots_clefs.get_uuid(["mots-clefs", id, "uuid"])
					mots_clefs.append(uuid)
				except:
					print(line[1], ": introuvable dans le cache des mots-clefs")


		# Création du body de la requête json
		dict["personnes"] = [{
			"personnes_id": personne,
			"sources_articles_id": id_article
		} for personne in personnes if len(personnes) >= 1]

		dict["congregations"] = [{
			"congregations_id": congregation,
			"sources_articles_id": id_article
		} for congregation in congregations if len(congregations) >= 1]

		dict["lieux"] = [{
				"lieux_id": lieu,
				"sources_articles_id": id_article
			} for lieu in lieux if len(lieux) >= 1]

		dict["mots_clefs"] = [{
				"mots_clefs_id": mots_clef,
				"sources_articles_id": id_article
			} for mots_clef in mots_clefs if len(mots_clefs) >= 1]

		indexations_stagiaires.append(dict)


			# TODO Comment indexer les oeuvres citées sans référentiel

			# TODO Pas de référentiel des institutions (il doit être entièrement remanié dans Directus)


#########################################################################################
## CREATION DES FICHIERS JSON
#########################################################################################

with open(args.json_indexations_stagiaires, 'w', encoding="utf-8") as file:
	json.dump(indexations_stagiaires, file, ensure_ascii=False)

print("\nECRITURE DES FICHIERS JSON TERMINEE\n")

#########################################################################################
## ENVOI DES DONNEES
#########################################################################################

# print("\nENVOI DES INDEXATIONS DE STAGIAIRES DANS DIRECTUS\n")
send_indexations(args.json_indexations_stagiaires)
