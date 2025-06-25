import os
import yaml
import argparse
import requests
import json
from pathlib import Path
from rdflib import Graph, Namespace
from datetime import datetime
from pprint import pprint

nakala_ns = Namespace("http://nakala.fr/terms#")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")

parser = argparse.ArgumentParser()
parser.add_argument("--file_dir")
parser.add_argument("--cache")
parser.add_argument("--collection")

args = parser.parse_args()
api_url = "https://api.nakala.fr"
api_key = os.getenv("NAKALA_API_KEY")
purl_image_datatype = 'http://purl.org/coar/resource_type/c_c513'


def upload_image_and_return_doi(file_path, file_name, cache_entry):
    print(f"Mise sur Nakala de l'image {file_path}")
    print(cache_entry)

    with open(file_path, 'rb') as f:
        # upload image
        r = requests.post(
            url=f"{api_url}/datas/uploads",
            headers={'accept': 'application/json', 'X-API-KEY': api_key},
            files={'file': f},
        ).json()

    # DATA

    request = requests.post(
        url=f"{api_url}/datas",
        headers={'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-KEY': api_key},
        data=json.dumps({
            'status': 'published',
            'files': [{
                'name': Path(file_name).stem,
                'sha1': r['sha1']
            }],
            'metas': [
                {
                    'value': Path(file_name).stem,
                    'propertyUri': nakala_ns['title'],
                    'typeUri': "http://www.w3.org/2001/XMLSchema#string"
                },
                {
                    'value': purl_image_datatype,
                    'propertyUri': nakala_ns['type'],
                    'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
                },
                {
                    'value': cache_entry.get("e36_uuid", "https://data-iremus.huma-num.fr/id/not-created-yet/"),
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
    )
    r = request.json()
    pprint(r)

    if r['code'] == 201:
        # This is DOI
        return r['payload']['id']
    else:
        return None


def update_yaml_with_nakala_values(folder_path, yaml_file_path):
    if not os.path.exists(yaml_file_path):
        print("Le fichier de cache n'existe pas encore.")
        return

    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file) or {}
        keys = yaml_data.keys()

    for key in keys:
        if not isinstance(yaml_data[key], dict):
            yaml_data[key] = {}
        if 'nakala_doi' not in yaml_data[key] or yaml_data[key]['nakala_doi'] == None:
            yaml_data[key]['nakala_doi'] = upload_image_and_return_doi(folder_path + key, key, yaml_data[key])
            with open(yaml_file_path, 'w') as yaml_file:
                yaml.dump(yaml_data, yaml_file, default_flow_style=False)
        else:
            print(f"{key} déjà uploadée vers Nakala")


def add_all_dois_to_nakala_collection(yaml_file_path, collection):
    dois = []
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file) or {}
        keys = yaml_data.keys()

        for key in keys:
            if not isinstance(yaml_data[key], dict):
                yaml_data[key] = {}
            if 'nakala_doi' in yaml_data[key] and yaml_data[key]['nakala_doi'] != None:
                dois.append(yaml_data[key]['nakala_doi'])

    r = requests.post(
        url=f"{api_url}/collections/{collection}/datas",
        headers={'accept': 'application/json', 'X-API-KEY': api_key},
        data=json.dumps(dois)
    ).json()

    pprint(f"Pushing {len(dois)} dois to nakala : {r}")


folder_path = args.file_dir
yaml_file_path = args.cache
update_yaml_with_nakala_values(folder_path, yaml_file_path)
add_all_dois_to_nakala_collection(yaml_file_path, args.collection)
