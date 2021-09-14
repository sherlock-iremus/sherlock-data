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
## FONCTIONS
################################################################################################

# Suppression d'une collection Directus
def delete(collection):
	# Création d'une liste des identifiants des données à supprimer grâce à une requête GET
	r = requests.get(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token)
	print("Récupération des données:", r)
	ids = [item["id"] for item in r.json()["data"]]

	# Suppression des données par parquets de 100
	for i in range(0, len(ids), 100):
		ids_slice = [ids[j] for j in range(i, i + 100) if j < len(ids)]
		print(i)
		try:
			r = requests.delete(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=ids_slice)
			print("Suppression des données par paquets de 100 :", r)
		except Exception as e:
			print(e)
		n = i

	#Suppression des données restantes (non envoyées car elles n'atteignent pas la centaine de données)
	for i in range(n, len(ids), 1):
		print(i)
		try:
			r = requests.delete(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=ids[i])
			print("Suppression des données restantes :", r)
		except Exception as e:
			print(e)


# Création d'une collection Directus à partir du fichier "taxonomies.xlsx"
def send_taxonomy(sheet, collection):
	rows = get_xlsx_sheet_rows_as_dicts(taxonomies[sheet])
	for row in rows:
		if row["name"] != None:
			# Création d'un dictionnaire par ligne de feuille Excel
			dict = {"id": row["uuid"], "nom": row["name"]}

			# Ajout de la correspondance identifiant_euterpe-UUID au dictionnaire "id_uuid"
			id_uuid[str(row["id"])] = row["uuid"]

			# Insertion du dictionnaire dans la collection Directus
			# r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=dict)
			# print(r)


# Création d'une collection Directus à partir du fichier "euterpe_data.xlsx"
def send_data(collection, range_min, range_max):
	print("Données à insérer:", len(data_to_send))

	# Envoi des données par paquets de 100
	for i in range(0, len(data_to_send), 100):
		# print(data_concepts)
		data_slice = [data_to_send[j] for j in range(i, i + 100) if j < len(data_to_send)]
		print(i)
		try:
			r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=data_slice)
			r.raise_for_status()
		except Exception as e:
			print(e)
			# pprint(data_slice)
		print(r)
		# time.sleep(0.5)

	# Envoi des données restantes (non envoyées car elles n'atteignent pas la centaine de données)
	for i in range(range_min, range_max):
		print(i)
		try:
			r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=data_to_send[i])
			r.raise_for_status()
		except Exception as e:
			print(e)
			# pprint(data_to_send[i])
		print(r)


# Fonction de recherche de l'UUID d'un concept à partir de son identifiant Euterpe,
# en utilisant le dictionnaire "id_uuid"
def get_uuid_list(column_name, uuid_list):
	row[column_name] = str(row[column_name])
	if "🍄" in row[column_name]:
		ids = row[column_name].split("🍄")
		for id in ids:
			try:
				uuid = id_uuid[id.strip()]
				uuid_list.append(uuid)
			except:
				print(column_name, ":", id, "- id non trouvé")
	else:
		try:
			uuid = id_uuid[row[column_name]]
			uuid_list.append(uuid)
		except:
			print(column_name, ":", row[column_name], "- id non trouvé")


################################################################################################
## TAXONOMIES
################################################################################################

# Lecture du fichier Excel
taxonomies = load_workbook(args.taxonomies)
taxonomies_sheets = taxonomies.sheetnames

# Dictionnaire de correspondance identifiant_euterpe-UUID
id_uuid = {}

# Insertion des données dans Directus
for sheet in taxonomies_sheets:
	if sheet == "spécialité":
		print("SPECIALITES")
		send_taxonomy(sheet, "specialites")
		print("\n" * 2)
	if sheet == "Période":
		print("PERIODES")
		send_taxonomy(sheet, "periodes")
		print("\n" * 2)
	if sheet == "École":
		print("ECOLES")
		send_taxonomy(sheet, "ecoles")
		print("\n" * 2)
	if sheet == "Domaine":
		print("DOMAINES")
		send_taxonomy(sheet, "domaines")
		print("\n" * 2)
	if sheet == "Lieu de conservation":
		print("LIEU DE CONSERVATION")
		send_taxonomy(sheet, "lieux_de_conservation")
		print("\n" * 2)
	if sheet == "Thème":
		print("THEMES")
		send_taxonomy(sheet, "themes")
		print("\n" * 2)
	if sheet == "Instrument de musique":
		print("INSTRUMENTS DE MUSIQUE")
		send_taxonomy(sheet, "instruments_de_musique")
		print("\n" * 2)
	if sheet == "Chant":
		print("CHANTS")
		send_taxonomy(sheet, "chants")
		print("\n" * 2)
	if sheet == "Support":
		print("SUPPORTS")
		send_taxonomy(sheet, "supports")
		print("\n" * 2)
	if sheet == "Type oeuvre":
		print("TYPES D'OEUVRES")
		send_taxonomy(sheet, "types_doeuvres")
		print("\n" * 2)
	if sheet == "Rôles":
		print("ROLES")
		send_taxonomy(sheet, "roles")
		print("\n" * 2)
	if sheet == "Notation musicale":
		print("NOTATION MUSICALE")
		send_taxonomy(sheet, "notation_musicale")
		print("\n" * 2)


################################################################################################
## DATA
################################################################################################

# Lecture du fichier Excel
data = load_workbook(args.data)
data_sheets = data.sheetnames


# 1. AUTEURS (collection "auteurs_oeuvres" dans Directus)
#----------------------------------------------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(data["1_auteurs"])

# Suppression de la collection Directus
# delete("auteurs_oeuvres")

for row in rows:

	periodes = []
	specialites = []
	ecoles = []

	# Recherche de l'UUID des "siècles" à partir de leur identifiant euterpe
	if row["siècle"] != None:
		get_uuid_list("siècle", periodes)

	# Recherche de l'UUID des "spécialités" à partir de leur identifiant euterpe
	if row["spécialité"] != None:
		get_uuid_list("spécialité", specialites)

	# Recherche de l'UUID des "écoles" à partir de leur identifiant euterpe
	if row["école"] != None:
		get_uuid_list("école", ecoles)

	# Ajout de la correspondance identifiant_euterpe-UUID des auteurs dans le dictionnaire
	id_uuid[str(row["id"])] = row["uuid"]

	dict = {
		"id": row["uuid"],
		"nom": row["nom"],
		"alias": row["alias"],
		"lieu_de_deces": row["lieu de décès"],
		"periode": [{
			"periodes_id": periode,
			"auteurs_oeuvres_id": row["uuid"],
			"collection": "periode"
		} for periode in periodes],
		"specialite": [{
			"specialites_id": specialite,
			"auteurs_oeuvres_id": row["uuid"],
			"collection": "specialite"
		} for specialite in specialites],
		"ecole": [{
			"ecoles_id": ecole,
			"auteurs_oeuvres_id": row["uuid"],
			"collection": "ecole"
		} for ecole in ecoles],
		"date_de_deces": row["date de décès"],
		"lieu_de_naissance": row["lieu de naissance"],
		"date_de_naissance": row["date de naissance"],
		"commentaire": row["commentaire"],
		"lieu_dactivite": row["lieu d'activité"],
		"date_dactivite": row["date d'activité"]
	}


	# Ajout du dictionnaire dans la liste de données à envoyer
	data_to_send.append(dict)

#Envoi des données dans Directus
# send_data("auteurs_oeuvres", 3300, 3385)


# 2. OEUVRES LYRIQUES
#------------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(data["5_oeuvres_lyriques"])

# Suppression de la collection Directus
# delete("oeuvres_lyriques")

for row in rows:

	librettistes = []
	compositeurs = []
	types_oeuvres = []

	# Recherche de l'UUID des "librettistes" à partir de leur identifiant euterpe
	if row["librettiste"] != None:
		get_uuid_list("librettiste", librettistes)

	# Recherche de l'UUID des "compositeurs" à partir de leur identifiant euterpe
	if row["compositeur"] != None:
		get_uuid_list("compositeur", compositeurs)

	# Recherche de l'UUID des "types d'oeuvres" à partir de leur identifiant euterpe
	if row["type_oeuvre"] != None:
		try:
			type_oeuvre_uuid = id_uuid[str(row["type_oeuvre"])]
		except:
			print("type_oeuvre :", row["type_oeuvre"], "non trouvé")

	# Ajout de la correspondance identifiant_euterpe-UUID des oeuvres lyriques dans le dictionnaire
	id_uuid[row["id"]] = row["uuid"]

	dict = {
		"id": row["uuid"],
		"titre": row["titre"],
		"librettiste": [{
			"auteurs_oeuvres_id": librettiste,
			"oeuvres_lyriques_id": row["uuid"],
			"collection": "auteurs_oeuvres"
		} for librettiste in librettistes],
		"compositeur": [{
			"auteurs_oeuvres_id": compositeur,
			"oeuvres_lyriques_id": row["uuid"],
			"collection": "auteurs_oeuvres"
		} for compositeur in compositeurs],
		"date_oeuvre": row["date_oeuvre"],
		"type_oeuvre": type_oeuvre_uuid,
		"commentaire": row["commentaire"]
	}

	#Ajout du dictionnaire dans la liste de données à envoyer
	data_to_send.append(dict)

# Envoi des données dans Directus
# send_data("oeuvres_lyriques", 100, 123)


# 3. AUTEURS BIBLIOGRAPHIE
#---------------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(data["6_auteurs_bibli_id"])

# Suppression de la collection Directus
# delete("auteurs_bibliographie")

for row in rows:

	# Ajout de la correspondance identifiant_euterpe-UUID des oeuvres lyriques dans le dictionnaire
	id_uuid[row["id"]] = row["uuid"]

	dict = {
		"id": row["uuid"],
		"nom": row["nom"],
		"prenom": row["prénom"]
	}

	# Ajout du dictionnaire dans la liste de données à envoyer
	data_to_send.append(dict)

# Envoi des données dans Directus
send_data("auteurs_bibliographie", 400, 436)

# 4. BIBLIOGRAPHIE
#--------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(data["3_euterpe_biblio"])

# Suppression de la collection Directus
# delete("bibliographie")

for row in rows:

	auteurs = []

	# Ajout de la correspondance identifiant_euterpe-UUID des oeuvres lyriques dans le dictionnaire
	id_uuid[row["id"]] = row["uuid"]

	dict = {
		"id": row["uuid"],
		"titre": row["titre"],
		"revue_colloque_collection": row["revue_colloque_collection"],
		"parution": row["parution"],
		"editeur": row["editeur"],
		"nbre_n_de_pages": row["nbre_n_de_page"],
		"n_revue_collection": row["n_revue_collection"],
		"lieu_de_publication": row["lieu_d_activite"],
		"commentaire": row["commentaire"]
	}

	# Ajout du dictionnaire dans la liste de données à envoyer
	data_to_send.append(dict)

# Envoi des données dans Directus
# send_data("bibliographie", 700, 721)




