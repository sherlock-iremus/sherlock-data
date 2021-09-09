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
parser.add_argument("--oeuvres")
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

# Lecture des fichiers excel
oeuvres = load_workbook(args.oeuvres)
taxonomies = load_workbook(args.taxonomies)

taxonomie_sheets = taxonomies.sheetnames

# Fonction d'envoi des données d'une feuille Excel dans une collection Directus
def send_data(sheet, collection):
	rows = get_xlsx_sheet_rows_as_dicts(taxonomies[sheet])
	for row in rows:
		if row["name"] != None:
			# Création d'un dictionnaire par ligne de feuille Excel
			dict = {"id": row["uuid"], "nom": row["name"]}

			# Insertion du dictionnaire dans la collection Directus
			r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=dict)
			print(r)


# Insertion des données de chaque taxonomie dans Directus
for sheet in taxonomie_sheets:
	if sheet == "spécialité":
		send_data(sheet, "specialites")

