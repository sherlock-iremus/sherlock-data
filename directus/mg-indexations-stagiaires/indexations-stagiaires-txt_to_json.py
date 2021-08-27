import argparse
import glob
from pathlib import Path
import ntpath
from pprint import pprint
from sherlockcachemanagement import Cache
import json

parser = argparse.ArgumentParser()
parser.add_argument("--txt")
parser.add_argument("--cache_personnes")
parser.add_argument("--cache_lieux")
parser.add_argument("--cache_mots_clés")
parser.add_argument("--cache_stagiaires")
parser.add_argument("--cache_institutions")
parser.add_argument("--cache_congrégations")
parser.add_argument("--json_indexations_personnes")
args = parser.parse_args()

# CACHES
cache_personnes = Cache(args.cache_personnes)

indexation = []

# Fichiers txt contenant les indexations
for file in glob.glob(args.txt + '**/*.txt', recursive=True):
	with open(file, "r") as f:
		lines = f.readlines()

		# Identifiant de l'article
		id_article = ntpath.basename(file)[3:-4]
		indexation_article = ({"id": id_article, "indices":[]})

		for line in lines:
			line = line.split("=")

			# Identifiant des personnes indexées
			if line[0] == "personnes":
				id = line[1].strip().replace("\n","")
				try:
					uuid = cache_personnes.get_uuid(["personnes", id, "uuid"])
					item = {
						"item": uuid,
						"sources_articles_id": id_article,
						"collection": "personnes"
					}

					indexation_article["indices"].append(item)
					indexation.append(indexation_article)

				except:
					print(line[1], ": introuvable dans le cache des personnes")

			with open(args.json_indexations_personnes, 'w', encoding="utf-8") as file:
				json.dump(indexation, file, ensure_ascii=False)

# pprint(indexation)

