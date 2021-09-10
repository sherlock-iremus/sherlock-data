import os, sys
import requests
import yaml
import argparse
from openpyxl import load_workbook
from pprint import pprint

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

# Fonction d'envoi des données de chaque feuille de "taxonomies.xlsx" dans une collection Directus
def post_taxonomy(sheet, collection):
	rows = get_xlsx_sheet_rows_as_dicts(taxonomies[sheet])
	for row in rows:
		if row["name"] != None:
			# Création d'un dictionnaire par ligne de feuille Excel
			dict = {"id": row["uuid"], "nom": row["name"]}

			# Insertion du dictionnaire dans la collection Directus
			r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=dict)
			print(r)


# Insertion des données dans Directus
# for sheet in taxonomies_sheets:
	# if sheet == "spécialité":
	# 	print("SPECIALITES")
	# 	post_taxonomy(sheet, "specialites")
	# 	print("\n" * 2)
	# if sheet == "Période":
	# 	print("PERIODES")
	# 	post_taxonomy(sheet, "periodes")
	# 	print("\n" * 2)
	# if sheet == "École":
	# 	print("ECOLES")
	# 	post_taxonomy(sheet, "ecoles")
	# 	print("\n" * 2)
	# if sheet == "Domaine":
	# 	print("DOMAINES")
	# 	post_taxonomy(sheet, "domaines")
	# 	print("\n" * 2)
	# if sheet == "Lieu de conservation":
	# 	print("LIEU DE CONSERVATION")
	# 	post_taxonomy(sheet, "lieux_de_conservation")
	# 	print("\n" * 2)
	# if sheet == "Thème":
	# 	print("THEMES")
	# 	post_taxonomy(sheet, "themes")
	# 	print("\n" * 2)
	# if sheet == "Instrument de musique":
	# 	print("INSTRUMENTS DE MUSIQUE")
	# 	post_taxonomy(sheet, "instruments_de_musique")
	# 	print("\n" * 2)
	# if sheet == "Chant":
	# 	print("CHANTS")
	# 	post_taxonomy(sheet, "chants")
	# 	print("\n" * 2)
	# if sheet == "Support":
	# 	print("SUPPORTS")
	# 	post_taxonomy(sheet, "supports")
	# 	print("\n" * 2)
	# if sheet == "Type oeuvre":
	# 	print("TYPES D'OEUVRES")
	# 	post_taxonomy(sheet, "types_doeuvres")
	# 	print("\n" * 2)
	# if sheet == "Rôles":
	# 	print("ROLES")
	# 	post_taxonomy(sheet, "roles")
	# 	print("\n" * 2)
	# if sheet == "Notation musicale":
	# 	print("NOTATION MUSICALE")
	# 	post_taxonomy(sheet, "notation_musicale")
	# 	print("\n" * 2)


################################################################################################
## DATA
################################################################################################

# Lecture du fichier Excel
data = load_workbook(args.data)
data_sheets = data.sheetnames

for row in data["1_auteurs"].values:
	dict = {"id": row["uuid"],
	        "nom":


	}

	# Insertion du dictionnaire dans la collection Directus
	r = requests.post(secret["url"] + '/items/auteurs_editeurs?limit=-1&access_token=' + access_token, json=dict)
	print(r)


# Insertion des données de "euterpe_data.xlsx" dans Directus
# AUTEURS-EDITEURS
