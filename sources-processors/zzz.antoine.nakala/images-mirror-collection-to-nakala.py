############################################################################################
# Written for NAKALA 3.11.1
############################################################################################

import argparse
import json
from rdflib import Graph, Namespace
from datetime import datetime
import requests
from pathlib import Path
from pprint import pprint
import os
import sys
from dotenv import load_dotenv

from sherlockcachemanagement import Cache

############################################################################################
# SETUP
############################################################################################

load_dotenv(dotenv_path=Path('.') / '.env')

parser = argparse.ArgumentParser()
parser.add_argument("--pictures")
parser.add_argument('--collection')
parser.add_argument('--cache')
args = parser.parse_args()

cache = Cache(args.cache)

iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
nakala_ns = Namespace("http://nakala.fr/terms#")

g = Graph(base=str(iremus_ns))

g.bind("iremus", iremus_ns)
g.bind("nakala", nakala_ns)

files = Path(args.pictures).glob('*')
api_key = os.getenv("NAKALA_API_KEY")
api_url = "https://api.nakala.fr"
purl_image_datatype = 'http://purl.org/coar/resource_type/c_c513'

############################################################################################
# HELPERS
############################################################################################


def delete_data_from_collection(collection_identifier, data_identifiers_list):
    r = requests.delete(
        url=f"{api_url}/collections/{collection_identifier}/datas",
        headers={'accept': 'application/json', 'X-API-KEY': api_key},
        data=json.dumps(data_identifiers_list)
    )


def fix_metadatas_of_existing_data(all_data):
    for data in all_data:
        title = get_metadata_value(all_data, data["identifier"], "http://nakala.fr/terms#title")[0]
        if title == "Rêve":
            continue
        print(data["identifier"], title)

        r = requests.delete(
            url=f"{api_url}/datas/{data['identifier']}/metadatas",
            headers={'accept': 'application/json', 'X-API-KEY': api_key},
            data=json.dumps({
                "propertyUri": "http://purl.org/dc/terms/identifier",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            })
        )
        print("  ", r.json())

        r = requests.delete(
            url=f"{api_url}/datas/{data['identifier']}/metadatas",
            headers={'accept': 'application/json', 'X-API-KEY': api_key},
            data=json.dumps({
                "propertyUri": "http://purl.org/dc/terms/identifier",
            })
        )
        print("  ", r.json())

        r = requests.delete(
            url=f"{api_url}/datas/{data['identifier']}/metadatas",
            headers={'accept': 'application/json', 'X-API-KEY': api_key},
            data=json.dumps({
                "propertyUri": "http://purl.org/dc/terms/identifier",
                "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
            })
        )
        print("  ", r.json())

        r = requests.post(
            url=f"{api_url}/datas/{data['identifier']}/metadatas",
            headers={'accept': 'application/json', 'X-API-KEY': api_key},
            data=json.dumps({
                "propertyUri": "http://purl.org/dc/terms/identifier",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "value": title,
            })
        )
        print("  ", r.json())

        e36_uuid = cache.get_uuid([title, 'E36_uuid'])
        if e36_uuid:
            r = requests.post(
                url=f"{api_url}/datas/{data['identifier']}/metadatas",
                headers={'accept': 'application/json', 'X-API-KEY': api_key},
                data=json.dumps({
                    "propertyUri": "http://purl.org/dc/terms/identifier",
                    "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
                    "value": "http://data-iremus.huma-num.fr/id/" + e36_uuid,
                })
            )
            print("  ", r.json())
        else:
            print(f"  [ERROR] No cached E36 UUID for {title}")


def get_metadata_value(data, identifier, propertyUri):
    values = []
    for data in data:
        if data["identifier"] == identifier:
            for md in data["metas"]:
                for k, v in md.items():
                    if k == "propertyUri" and v == propertyUri:
                        values.append(md["value"])
            return values


############################################################################################
# RÉCUPÉRER TOUTES LES DONNÉES
############################################################################################

nakala_doi_list = []

all_data = requests.post(
    url=f"{api_url}/users/datas/deposited",
    headers={'accept': 'application/json', 'X-API-KEY': api_key},
    data=json.dumps({"limit": 1000})
).json()["data"]

business_id_list_in_cache = [k for k, v in cache.cache.items()]

############################################################################################
# DATA
############################################################################################

# on itère sur les identifiants métiers des images, à savoir le nom du fichier.
files = list(files)
i = 1
files = [f for f in files if f.stem not in [".gitattributes", ".git", ".DS_Store"]]

for file in files:
    print(f"{i}/{len(files)} ajout de données")
    i += 1

    e36_uuid = cache.get_uuid([file.stem, 'E36_uuid'])
    try:
        nakala_doi = cache.cache[file.stem]['nakala_doi']
    except:
        nakala_doi = None

    if not nakala_doi:
        # IMAGE

        with file.open('rb') as f:
            # upload image
            r = requests.post(
                url=f"{api_url}/datas/uploads",
                headers={'accept': 'application/json', 'X-API-KEY': api_key},
                files={'file': f},
            ).json()

            cache.set_kv([file.stem, "nakala_sha1"], r['sha1'])

        # DATA

        r = requests.post(
            url=f"{api_url}/datas",
            headers={'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-KEY': api_key},
            data=json.dumps({
                'status': 'published',
                'files': [{
                    'name': file.stem,
                    'sha1': r['sha1']
                }],
                'metas': [
                    {
                        'value': file.stem,
                        'propertyUri': nakala_ns['title'],
                        'typeUri': "http://www.w3.org/2001/XMLSchema#string"
                    },
                    {
                        'value': purl_image_datatype,
                        'propertyUri': nakala_ns['type'],
                        'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
                    },
                    {
                        'value': iremus_ns[e36_uuid],
                        'propertyUri': 'http://purl.org/dc/terms/identifier',
                        'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
                    },
                    {
                        # Si on connaît l'auteur, remplir sous la forme : value : {'givenname': '', surname: '', orcid: ''}
                        'propertyUri': nakala_ns['creator'],
                        'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
                    },
                    {
                        'value': datetime.now().strftime("%Y-%m-%d"),
                        'propertyUri': nakala_ns['created'],
                        'typeUri': "http://www.w3.org/2001/XMLSchema#string"
                    },
                    {
                        'value': 'PDM',  # licence code : https://apitest.nakala.fr/vocabularies/licenses
                        'propertyUri': nakala_ns['license'],
                        'typeUri': "http://www.w3.org/2001/XMLSchema#string"
                    },
                ],
            }),
        ).json()

        pprint(r)

        if r['code'] == 201:
            cache.set_kv([file.stem, "nakala_doi"], r['payload']['id'])
            cache.bye()
            nakala_doi = r['payload']['id']
        else:
            pprint(r)

    nakala_doi_list.append(nakala_doi)

############################################################################################
# SUPPRIMER TOUTES LES DONNÉES DE LA COLLECTION
############################################################################################

data_in_collection = []
fetch_more = True
while fetch_more:
    r = requests.get(
        url=f"{api_url}/collections/{args.collection}/datas",
        headers={'accept': 'application/json', 'X-API-KEY': api_key}
    )
    data_in_collection = r.json()["data"]
    n_data_in_collection = r.json()["total"]

    identifiers = [dic["identifier"] for dic in data_in_collection]

    if len(identifiers) > 0:
        print(f"Suppression paginée des données de la collection ({n_data_in_collection} restantes)")
        delete_data_from_collection(args.collection, identifiers)

    else:
        fetch_more = False

################################################################################
# ADD TO COLLECTION
################################################################################

r = requests.post(
    url=f"{api_url}/collections/{args.collection}/datas",
    headers={'accept': 'application/json', 'X-API-KEY': api_key},
    data=json.dumps(nakala_doi_list)
).json()

cache.bye()
