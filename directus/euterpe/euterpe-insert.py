import os, sys
import requests
import yaml
import argparse
from openpyxl import load_workbook
from pprint import pprint
import time
import uuid
import re
from pprint import pprint
from geopy.geocoders import Nominatim

# Helpers
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--excel_data")
parser.add_argument("--excel_taxonomies")
args = parser.parse_args()

# YAML Secret
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()


################################################################################################
## FUNCTIONS
################################################################################################

# Deleting a Directus collection
def delete(collection):
    try:
        # GET Request listing the collection's items
        r = requests.get(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token)
        print("Retrieving the collection items:", r)
        ids = [item["id"] for item in r.json()["data"]]

        # Deleting the data in paquets of 100
        try:
            for i in range(0, len(ids), 100):
                ids_slice = [ids[j] for j in range(i, i + 100) if j < len(ids)]
                print(i)
                try:
                    r = requests.delete(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=ids_slice)
                    print("Deleting the items in paquets of 100 :", r)
                except Exception as e:
                    print(e)
                n = i
        except:
            n = 0

        # Deleting the remaining data (not sent because it didn't reach a hundred)
        try:
            for i in range(n, len(ids), 1):
                print(i)
                try:
                    r = requests.delete(
                        secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=ids[i])
                    print("Deleting the remaining items :", r)
                except Exception as e:
                    print(e)
        except:
            pass
    except:
        print("There are no items in the collection\n")

def create_dict_id_uuid(sheet):
    rows = get_xlsx_sheet_rows_as_dicts(excel_taxonomies[sheet])
    for row in rows:
        if row["name"] != None:
            # Linking an object's identifier to its UUID in the "id_uuid" dictionary
            id_uuid[str(row["id"])] = row["uuid"]

# Creating a Directus collection from "taxonomies.xlsx"
def send_taxonomy(sheet, collection):
    rows = get_xlsx_sheet_rows_as_dicts(excel_taxonomies[sheet])
    for row in rows:
        if row["name"] != None:
            # Creating one dictionary per Excel sheet line
            dict = {"id": row["uuid"], "nom": row["name"]}

            # Retrieving geographical coordinates
            if sheet == "Lieu de conservation":

                # Creating geolocator object
                geolocator = Nominatim(user_agent="Iremus")

                # Creating a dictionary to store the data
                dict_coords = {}

                try:
                    location = geolocator.geocode(row["name"])
                    latitude = str(location.latitude)
                    longitude = str(location.longitude)
                    dict["coordonnees_geographiques"] = latitude + ", " + longitude
                except:
                    try:
                        city_split = row["name"].split(",")
                        city = city_split[0]
                        location = geolocator.geocode(city)
                        latitude = str(location.latitude)
                        longitude = str(location.longitude)
                        dict["coordonnees_geographiques"] = latitude + ", " + longitude
                    except:
                        print("Coordonnées du lieu", row["name"], "non trouvées")

        # Sending the items into the collection
        r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=dict)
        print(r)


# Creating a Directus collection from "euterpe_data.xlsx"
def send_data(collection, paquet, range_min, range_max):
    print("Sending", len(data_to_send), "items")

    # Sending the data in paquets of 100
    for i in range(0, len(data_to_send), paquet):
        data_slice = [data_to_send[j] for j in range(i, i + paquet) if j < len(data_to_send)]
        print(i)
        try:
            r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=data_slice)
            r.raise_for_status()
        except Exception as e:
            print(e)
            pprint(data_slice)
            print(r.json())
            print("\n")
        # time.sleep(2)

    # Sending the remaining data (not sent because it didn't reach a hundred)
    for i in range(range_min, range_max):
        print(i)
        try:
            r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=data_to_send[i])
            r.raise_for_status()
        except Exception as e:
            print(e)
            # pprint(data_to_send[i])
            print(r.json())
            print("\n")
        # time.sleep(2)


# Looking for an indexed object's UUID using its identifier in the "id_uuid" dictionary
def get_uuid_list(column_name, uuid_list):
    row[column_name] = str(row[column_name])
    if "🍄" in row[column_name]:
        ids = row[column_name].split("🍄")
        for id in ids:
            try:
                uuid = id_uuid[id.strip()]
                uuid_list.append(uuid)
            except:
                print(column_name, ":", id, "- id not found")
    else:
        try:
            id = row[column_name]
            uuid = id_uuid[id.strip()]
            uuid_list.append(uuid)
        except:
            print(column_name, ":", row[column_name], "- id not found")


################################################################################################
## TAXONOMIES
################################################################################################

# Reading the Excel file
excel_taxonomies = load_workbook(args.excel_taxonomies)
excel_taxonomies_sheets = excel_taxonomies.sheetnames

# Dictionary matching an object's identifier to its UUID
id_uuid = {}

# Creating one Directus collection per taxonomy
print("\nTAXONOMIES\n")

for sheet in excel_taxonomies_sheets:
    if sheet == "spécialité":
        # print("SPECIALITES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "specialites")
        # print("\n" * 2)
    if sheet == "Période":
        # print("PERIODES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "periodes")
        # print("\n" * 2)
    if sheet == "École":
        # print("ECOLES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "ecoles")
        # print("\n" * 2)
    if sheet == "Domaine":
        # print("DOMAINES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "domaines")
        # print("\n" * 2)
    if sheet == "Lieu de conservation":
        # print("LIEU DE CONSERVATION")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "lieux_de_conservation")
        # print("\n" * 2)
    if sheet == "Thème":
        # print("THEMES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "themes")
        # print("\n" * 2)
    if sheet == "Instrument de musique":
        # print("INSTRUMENTS DE MUSIQUE")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "instruments_de_musique")
        # print("\n" * 2)
    if sheet == "Chant":
        print("CHANTS")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "chants")
        # print("\n" * 2)
    if sheet == "Support":
        # print("SUPPORTS")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "supports")
        # print("\n" * 2)
    if sheet == "Type oeuvre":
        # print("TYPES D'OEUVRES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "types_doeuvres")
        # print("\n" * 2)
    if sheet == "Rôles":
        # print("ROLES")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "roles")
        # print("\n" * 2)
    if sheet == "Notation musicale":
        print("NOTATION MUSICALE")
        create_dict_id_uuid(sheet)
        # send_taxonomy(sheet, "notation_musicale")
        # print("\n" * 2)


################################################################################################
## DATA
################################################################################################

# Reading the Excel file
excel_data = load_workbook(args.excel_data)
excel_sheets = excel_data.sheetnames


# 1. "AUTEURS OEUVRES"
#----------------------------------------------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(excel_data["1_auteurs"])

# Deleting all items in the Directus collection
print("\n'AUTEURS OEUVRES' COLLECTION\n")
# delete("auteurs_oeuvres")

for row in rows:

    periodes = []
    specialites = []
    ecoles = []

    # Adding the link between the object's identifier and UUID in the "id_uuid" dictionary
    id_uuid[str(row["id"])] = row["uuid"]

    # Retrieving indexed object's UUIDs using their identifier
    if row["siècle"] != None:
        get_uuid_list("siècle", periodes)

    if row["spécialité"] != None:
        get_uuid_list("spécialité", specialites)

    if row["école"] != None:
        get_uuid_list("école", ecoles)

    # Creating the request's body
    dict = {
        "id": row["uuid"],
        "nom": row["nom"],
        "alias": row["alias"],
        "lieu_de_deces": row["lieu de décès"],
        "periodes": [{
            "periodes_id": periode,
            "auteurs_oeuvres_id": row["uuid"],
            "collection": "periode"
        } for periode in periodes],
        "specialites": [{
            "specialites_id": specialite,
            "auteurs_oeuvres_id": row["uuid"],
            "collection": "specialite"
        } for specialite in specialites],
        "ecoles": [{
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

    data_to_send.append(dict)

# Inserting the data into the Directus collection
# send_data("auteurs_oeuvres", 100, 3300, 3385)


# 2. "OEUVRES LYRIQUES"
#------------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(excel_data["5_oeuvres_lyriques"])

# Deleting all items in the Directus collection
print("\n'OEUVRES LYRIQUES' COLLECTION\n")
# delete("oeuvres_lyriques")

for row in rows:

    librettistes = []
    compositeurs = []
    types_oeuvres = []

    # Adding the link between the object's identifier and UUID in the "id_uuid" dictionary
    id_uuid[str(row["id"])] = row["uuid"]

    # Retrieving indexed object's UUIDs using their identifier
    if row["librettiste"] != None:
        get_uuid_list("librettiste", librettistes)

    if row["compositeur"] != None:
        get_uuid_list("compositeur", compositeurs)

    if row["type_oeuvre"] != None:
        try:
            type_oeuvre_uuid = id_uuid[str(row["type_oeuvre"])]
        except:
            print("type_oeuvre :", row["type_oeuvre"], "not found")

    # Creating the request's body
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
        "type": type_oeuvre_uuid,
        "commentaire": row["commentaire"]
    }

    data_to_send.append(dict)

# Inserting the data into the Directus collection
# send_data("oeuvres_lyriques", 100, 100, 123)


# 3. "AUTEURS BIBLIOGRAPHIE"
#---------------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(excel_data["6_auteurs_bibli_id"])

# Deleting all items in the Directus collection
print("\n'AUTEURS BIBLIOGRAPHIE' COLLECTION\n")
# delete("auteurs_bibliographie")

for row in rows:

    # Adding the link between the object's identifier and UUID in the "id_uuid" dictionary
    id_uuid[str(row["id"])] = row["uuid"]

    # Creating the request's body
    dict = {
        "id": row["uuid"],
        "nom": row["nom"],
        "prenom": row["prénom"]
    }


    data_to_send.append(dict)

# Inserting the data into the Directus collection
# send_data("auteurs_bibliographie", 100, 400, 436)


# 4. "BIBLIOGRAPHIE"
#--------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(excel_data["3_euterpe_biblio"])

# Deleting all items in the Directus collection
print("\n'BIBLIOGRAPHIE' COLLECTION\n")
# delete("bibliographie")

for row in rows:

    auteurs = []

    # Adding the link between the object's identifier and UUID in the "id_uuid" dictionary
    id_uuid[str(row["id"])] = row["uuid"]

    # Retrieving indexed object's UUIDs using their identifier
    if row["auteur_id"] != None:
        get_uuid_list("auteur_id", auteurs)

    # Creating the request's body
    dict = {
        "id": row["uuid"],
        "auteurs": [{
            "auteurs_bibliographie_id": auteur,
            "bibliographie_id": row["uuid"],
            "collection": "auteurs_bibliographie"
        } for auteur in auteurs],
        "titre": row["titre"],
        "revue_colloque_collection": row["revue_colloque_collection"],
        "parution": row["parution"],
        "editeur": row["editeur"],
        "nbre_n_de_pages": row["nbre_n_de_page"],
        "n_revue_collection": row["n_revue_collection"],
        "lieu_de_publication": row["lieu_d_activite"],
        "commentaire": row["commentaire"]
    }

    data_to_send.append(dict)

# Inserting the data into the Directus collection
# send_data("bibliographie", 100, 700, 721)


# 5. "OEUVRES"
#--------------------

data_to_send = []

rows = get_xlsx_sheet_rows_as_dicts(excel_data["4_euterpe_images"])

# Retrieving the files (pictures) from Directus's file library
r = requests.get(secret["url"] + f'/files?limit=-1&access_token=' + access_token)
print("\nRetrieving the pictures from Directus's file library :", r, "\n")

# Matching a picture's identifier to its UUID
images_uuid = {}
for item in r.json()["data"]:
    images_uuid[item["title"]] = item["id"]

# Deleting all items in the Directus collection
print("\n'OEUVRES' COLLECTION\n")
# delete("oeuvres")

for row in rows:

    # Lists of indexed object's UUIDs
    editeurs = []
    domaines = []
    instruments = []
    inventeurs = []
    themes = []
    lieux_conservation = []
    notations_musicales = []
    graveurs = []
    artistes = []
    chants = []
    attributions = []
    ecoles = []
    anciennes_attributions = []
    ateliers = []
    copies = []
    dapres_list = []
    manieres = []
    voir_aussi = []

    # Selecting one of the indexed pictures
    if row["image"] != None:
        images_unstripped = row["image"].split("🍄")
        images = [image.strip() for image in images_unstripped]
        image_default = images[0]

    # Retrieving indexed object's UUIDs using their identifier and adding them to the list
    if row["éditeur"] != None:
        get_uuid_list("éditeur", editeurs)

    if row["domaine"] != None:
        get_uuid_list("domaine", domaines)

    if row["instrument de musique"] != None:
        get_uuid_list("instrument de musique", instruments)

    if row["inventeur"] != None:
        get_uuid_list("inventeur", inventeurs)

    if row["thème"] != None:
        get_uuid_list("thème", themes)

    if row["lieu de conservation"] != None:
        get_uuid_list("lieu de conservation", lieux_conservation)

    if row["musique écrite"] != None:
        get_uuid_list("musique écrite", notations_musicales)

    if row["graveur"] != None:
        get_uuid_list("graveur", graveurs)

    if row["artiste"] != None:
        get_uuid_list("artiste", artistes)

    if row["chant"] != None:
        get_uuid_list("chant", chants)

    if row["attribution"] != None:
        get_uuid_list("attribution", attributions)

    if row["école"] != None:
        get_uuid_list("école", ecoles)

    if row["ancienne attribution"] != None:
        get_uuid_list("ancienne attribution", anciennes_attributions)

    if row["atelier"] != None:
        get_uuid_list("atelier", ateliers)

    if row["copie d'après"] != None:
        get_uuid_list("copie d'après", copies)

    if row["d'après"] != None:
        get_uuid_list("d'après", dapres_list)

    if row["manière de"] != None:
        get_uuid_list("manière de", manieres)

    if row["voir aussi"] != None:
        get_uuid_list("voir aussi", voir_aussi)

    # Creating an ISO date
    try:
        date = re.search("[0-9]{4}", str(row["date œuvre"]))
        date = date.group()[:4] + "-01-01T00:00:00Z"
    except:
        date = None

    # Creating the request's body
    dict = {
        "id": row["uuid"],
        "titre": row["titre"],
        "titre_alternatif": row["titre alternatif"],
        "editeur": [{
            "auteurs_oeuvres_id": editeur,
            "oeuvres_id": row["uuid"],
            "collection": "auteurs_oeuvres"
        } for editeur in editeurs],
        "reference_iremus": row["référence iremus"].replace("🍄", ",") if row["référence iremus"] != None else row["référence iremus"],
        "domaine": [{
            "domaines_id": domaine,
            "oeuvres_id": row["uuid"]
        } for domaine in domaines],
        "num_inventaire": row["n° inventaire"],
        "cote": row["cote"],
        "inscription": row["inscription"],
        "technique": row["technique"],
        "oeuvre_en_rapport": row["œuvre en rapport"],
        "themes": [{
            "themes_id": theme,
            "oeuvres_id": row["uuid"]
        } for theme in themes],
        "inventeur": [{
            "auteurs_oeuvres_id": inventeur,
            "oeuvres_id": row["uuid"]
        } for inventeur in inventeurs],
        "lieu_de_conservation": [{
            "lieux_de_conservation_id": lieu_conservation,
            "oeuvres_id": row["uuid"]
        } for lieu_conservation in lieux_conservation],
        "date_oeuvre": row["date œuvre"],
        "date_oeuvre_iso": date,
        "precision_oeuvre": row["précision œuvre"],
        "precision_instrument": row["précision instrument"],
        "notation_musicale": [{
            "notation_musicale_id": notation_musicale,
            "oeuvres_id": row["uuid"]
        } for notation_musicale in notations_musicales],
        "graveur": [{
            "auteurs_oeuvres_id": graveur,
            "oeuvres_id": row["uuid"]
        } for graveur in graveurs],
        "commentaire": row["commentaire"],
        "bibliographie": row["bibliographie"],
        "reference_agence": row["référence agence"],
        "url": row["url"],
        "titre_url": row["titre de l'url"],
        "hauteur": row["hauteur"],
        "largeur": row["largeur"],
        "diametre": row["diamètre"],
        "chants": [{
            "chants_id": chant,
            "oeuvres_id": row["uuid"]
        } for chant in chants],
        "artiste": [{
            "auteurs_oeuvres_id": artiste,
            "oeuvres_id": row["uuid"],
            "collection": "auteurs_oeuvres"
        } for artiste in artistes],
        "ecole": [{
                "auteurs_oeuvres_id": ecole,
                "oeuvres_id": row["uuid"],
                "collection": "auteurs_oeuvres"
            } for ecole in ecoles],
        "attribution": [{
                    "auteurs_oeuvres_id": attribution,
                    "oeuvres_id": row["uuid"],
                    "collection": "auteurs_oeuvres"
                } for attribution in attributions],
        "precision_musique": row["précision musique"],
        "ancienne_attribution": [{
            "auteurs_oeuvres_id": ancienne_attribution,
            "oeuvres_id": row["uuid"]
        } for ancienne_attribution in anciennes_attributions],
        "atelier": [{
            "auteurs_oeuvres_id": atelier,
            "oeuvres_id": row["uuid"]
        } for atelier in ateliers],
        "source_litteraire": row["source littéraire"],
        "copie_dapres": [{
            "auteurs_oeuvres_id": copie,
            "oeuvres_id": row["uuid"]
        } for copie in copies],
        "dapres": [{
            "auteurs_oeuvres_id": dapres,
            "oeuvres_id": row["uuid"]
        } for dapres in dapres_list],
        "a_la_maniere_de": [{
            "auteurs_oeuvres_id": maniere,
            "oeuvres_id": row["uuid"]
        } for maniere in manieres],
        "instruments_de_musique": [{
            "instruments_de_musique_id": instrument,
            "oeuvres_id": row["uuid"]
        } for instrument in instruments],
        "voir_aussi": [{
            "voir_aussi_id": v,
            "oeuvres_id": row["uuid"]
        } for v in voir_aussi]
    }

    # Adding the selected picture for the thumbnail
    try :
        dict["image"] = images_uuid[image_default]
    except:
        print(image_default, ": picture not found in Directus file library")

    # Adding all the pictures
    try :
        dict["images"] = [{
            "images_title": images_uuid[image],
            "oeuvres_id": row["uuid"]
        } for image in images]
    except:
        print(image_default, ": picture not found in Directus file library")

    # "contient/contenu dans" à écrire à la main? (un seul enregistrement)
    # ajouter "oeuvre représentée"

    data_to_send.append(dict)

# Inserting the data into the Directus collection
send_data("oeuvres", 25, 10600, 10692)


