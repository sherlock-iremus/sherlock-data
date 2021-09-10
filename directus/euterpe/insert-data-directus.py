import os, sys
import requests
import yaml
import argparse
from openpyxl import load_workbook
from pprint import pprint
import time

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
# print(sys.path)
from helpers_python import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--data")
parser.add_argument("--taxonomies")
args = parser.parse_args()

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()


################################################################################################
## TAXONOMIES
################################################################################################

# Lecture du fichier Excel
taxonomies = load_workbook(args.taxonomies)
taxonomies_sheets = taxonomies.sheetnames

# Dictionnaire de correspondance identifiant_euterpe-UUID
id_uuid = {}

# Fonction d'envoi des données de chaque feuille de "taxonomies.xlsx" dans une collection Directus
def post_taxonomy(sheet, collection):
	rows = get_xlsx_sheet_rows_as_dicts(taxonomies[sheet])
	for row in rows:
		if row["name"] != None:
			# Création d'un dictionnaire par ligne de feuille Excel
			dict = {"id": row["uuid"], "nom": row["name"]}

			# Ajout de la correspondance identifiant_euterpe-UUID dans le dictionnaire
			id_uuid[row["id"]] = row["uuid"]

			# Insertion du dictionnaire dans la collection Directus
			# r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=dict)
			# print(r)


# Insertion des données dans Directus
for sheet in taxonomies_sheets:
	if sheet == "spécialité":
		print("SPECIALITES")
		post_taxonomy(sheet, "specialites")
		print("\n" * 2)
	if sheet == "Période":
		print("PERIODES")
		post_taxonomy(sheet, "periodes")
		print("\n" * 2)
	if sheet == "École":
		print("ECOLES")
		post_taxonomy(sheet, "ecoles")
		print("\n" * 2)
	if sheet == "Domaine":
		print("DOMAINES")
		post_taxonomy(sheet, "domaines")
		print("\n" * 2)
	if sheet == "Lieu de conservation":
		print("LIEU DE CONSERVATION")
		post_taxonomy(sheet, "lieux_de_conservation")
		print("\n" * 2)
	if sheet == "Thème":
		print("THEMES")
		post_taxonomy(sheet, "themes")
		print("\n" * 2)
	if sheet == "Instrument de musique":
		print("INSTRUMENTS DE MUSIQUE")
		post_taxonomy(sheet, "instruments_de_musique")
		print("\n" * 2)
	if sheet == "Chant":
		print("CHANTS")
		post_taxonomy(sheet, "chants")
		print("\n" * 2)
	if sheet == "Support":
		print("SUPPORTS")
		post_taxonomy(sheet, "supports")
		print("\n" * 2)
	if sheet == "Type oeuvre":
		print("TYPES D'OEUVRES")
		post_taxonomy(sheet, "types_doeuvres")
		print("\n" * 2)
	if sheet == "Rôles":
		print("ROLES")
		post_taxonomy(sheet, "roles")
		print("\n" * 2)
	if sheet == "Notation musicale":
		print("NOTATION MUSICALE")
		post_taxonomy(sheet, "notation_musicale")
		print("\n" * 2)

# pprint(id_uuid)

################################################################################################
## DATA
################################################################################################

# Lecture du fichier Excel
data = load_workbook(args.data)
data_sheets = data.sheetnames

# Fonction de recherche de l'UUID d'un concept à partir de son identifiant Euterpe,
# en utilisant le dictionnaire "id_uuid" créé précédemment
def get_uuid(column_name, uuid_list):
	if len(row[column_name]) == 1:
		uuid = id_uuid[row[column_name]]
		uuid_list.append(uuid)
	else:
		ids = row[column_name].split("🍄")
		for id in ids:
			uuid = id_uuid[id.strip()]
			uuid_list.append(uuid)


# AUTEURS-EDITEURS

rows = get_xlsx_sheet_rows_as_dicts(data["1_auteurs"])

# Récupération et suppression des données dans Directus
# r = requests.get(secret["url"] + '/items/auteurs_editeurs?limit=-1&access_token=' + access_token)
# print("Récupération des données:", r)
# ids = [item["id"] for item in r.json()["data"]]
#
# for i in range(0, len(ids), 10):
# 	ids_slice = [ids[j] for j in range(i, i+10) if j < len(ids)]
# 	print(i)
# 	r = requests.delete(secret["url"] + '/items/personnes?limit=-1&access_token=' + access_token, json=ids_slice)
# 	print(r)


for row in rows:

	periodes = []
	specialites = []
	ecoles = []

	# Recherche de l'UUID des "siècles" à partir de leur identifiant euterpe
	if row["siècle"] != None:
		get_uuid("siècle", periodes)

	# Recherche de l'UUID des "spécialités" à partir de leur identifiant euterpe
	if row["spécialité"] != None:
		get_uuid("spécialité", specialites)

	# Recherche de l'UUID des "écoles" à partir de leur identifiant euterpe
	if row["école"] != None:
		get_uuid("école", ecoles)

	# Ajout de la correspondance identifiant_euterpe-UUID des auteurs dans le dictionnaire
	id_uuid[row["id"]] = row["uuid"]

	dict = {
				"id": row["uuid"],
			    "nom": row["nom"],
			    "alias": row["alias"],
				"lieu_de_deces": row["lieu de décès"],
				"periode": [{
							"periodes_id": periode,
							"auteurs_editeurs_id": row["uuid"],
							"collection": "periode"
						} for periode in periodes],
				"specialite": [{
					"specialites_id": specialite,
					"auteurs_editeurs_id": row["uuid"],
					"collection": "specialite"
				} for specialite in specialites],
				"ecole": [{
					"ecoles_id": ecole,
					"auteurs_editeurs_id": row["uuid"],
					"collection": "ecole"
				} for ecole in ecoles],

				"date_de_deces": row["date de décès"],
				"lieu_de_naissance": row["lieu de naissance"],
				"date_de_naissance": row["date de naissance"],
				"commentaire": row["commentaire"],
				"lieu_dactivite": row["lieu d'activité"],
				"date_dactivite": row["date d'activité"]
	        }

	# print(dict)

	r = requests.post(secret["url"] + '/items/auteurs_editeurs?limit=-1&access_token=' + access_token, json=dict)
	print(r)


