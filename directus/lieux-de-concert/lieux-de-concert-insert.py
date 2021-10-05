import os, sys
import requests
import yaml
import argparse
from openpyxl import load_workbook
from pprint import pprint
import time
import re
from pprint import pprint
from geopy.geocoders import Nominatim

# Helpers
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--excel_data")
args = parser.parse_args()

# YAML Secret
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Reading the Excel file
excel_data = load_workbook(args.excel_data)
excel_data_sheets = excel_data.sheetnames

# Data
data = []

# Adding both sheets of the excel file in the "data" list of dictionaries.
for s in excel_data_sheets:
    rows = get_xlsx_sheet_rows_as_dicts(excel_data[s])
    for row in rows:
        dict = {
            "arrondissement": row["Arrondissement"],
            "nom_de_la_salle": row["Nom de la salle"],
            "raison_sociale_de_letablissement" : row["Raison sociale de l'établissement"],
            "type_de_lieu" : row["Type de lieu"],
            "adresse" : row["Adresse"],
            "date_de_construction" : row["Date de construction"],
            "date_de_premiere_activite_de_concert" : row["Date de première activité de concert"],
            "date_de_derniere_inauguration" : row["Date de dernière inauguration"],
            "exploitant" : row["Exploitant"],
            "statut_juridique" : row["Statut juridique"],
            "proprietaire" : row["Propriétaire"],
            "reseau" : row["Réseau"],
            "jazz_et_blues" : row["Jazz et blues"],
            "pop_et_rock" : row["Pop et Rock"],
            "rnb_rap_soul" : row["RnB, Rap, Soul"]
            "musique_electronique" : row["Musique électronique",
            "musique_du_monde" : row["Musique du monde"],
            "chanson_et_variete" : row["Chanson et variété"],
            "gospel" : row["Gospel"],
            "musique_chorale" : row["Musique chorale"],
            "theatre_musical" : row["Théâtre musical"],
            "musique_symphonique" : row["Musique symphonique"],
            "musique_de_chambre" : row["Musique de chambre"],
            "opera" : row["Opéra"],
            "recital" : row["Récital"]
            "cine_concerts" : row["Ciné - concerts"],
            "autres" : row["Autres(préciser quoi dans la colonne)"],
            "jauge assise" : row["Jauge assise"],
            "jauge_debout" : row["Jauge debout"],
            "salle_privatisable" : row["La salle est-elle privatisable?"],
            "modes_de_production" : row["Modes_de_production"],
            "actions_culturelles" : row["Actions culturelles(ateliers, formations, conférences, cours, etc.)"],
            "espace_de_sociabilite_en_libre_acces" : row["Espace de sociabilité en libre accès(hall, cours, terrasse...)"],
            "espace_de_restauration_payant" : row["Espace de restauration(payant)"],
            "presence_dun_centre_de_ressources_" :
            Espace
            de
            restauration(payant)
            Présence
            d
            'un centre de ressources (bibliothèque, médiathèque, etc.)	Présence d'
            espaces
            privatisables
            Accès
            PMR
            Subventionné
            Notice
            Dimensions
            plateau
            Dimensions
            salle
            Commentaires
            Contact
            site
            internet

        }
        # Parisian places
        if "Département" not in row:
            dict["departement"] = 75
            dict["commune"] = "Paris"
        else:
            dict["departement"] = row["Département"]
            dict["commune"] = row["Commune"]

        data.append(dict)

pprint(data)