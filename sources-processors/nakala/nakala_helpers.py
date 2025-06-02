from datetime import datetime
import json
from pprint import pprint
import requests
import urllib.parse

requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.verify = False


def post_datas_uploads(api_base, api_key, file):
    with open(file, 'rb') as f:
        return session.post(
            url=f"https://{api_base}/datas/uploads",
            headers={'accept': 'application/json', 'X-API-KEY': api_key},
            files={'file': f},
        ).json()


def get_users_me(api_base, api_key):
    return session.get(
        url=f"https://{api_base}/users/me",
        headers={'accept': 'application/json', 'X-API-KEY': api_key}
    ).json()


def post_datas(api_base, api_key, files, sherlock_uuid, title):
    # https://documentation.huma-num.fr/nakala-guide-de-description/#fonctionnement-des-proprietes-nakala-obligatoires
    data = {
        # 'collectionsIds': [collectionId],
        'files': files,
        'status': 'published',
        'metas': [
            {
                'value': title,
                'propertyUri': 'http://nakala.fr/terms#title',
                'typeUri': "http://www.w3.org/2001/XMLSchema#string"
            },
            {
                'propertyUri': 'http://nakala.fr/terms#type',
                'value': 'http://purl.org/coar/resource_type/c_c513',
                'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
            },
            {
                'propertyUri': 'http://purl.org/dc/terms/identifier',
                'value': f"http://data-iremus.huma-num.fr/id/{sherlock_uuid}",
                'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
            },
            {
                # Si on connaît l'auteur, remplir sous la forme : value : {'givenname': '', surname: '', orcid: ''}
                'propertyUri': 'http://nakala.fr/terms#creator',
                'value': None,
                'typeUri': "http://www.w3.org/2001/XMLSchema#anyURI"
            },
            {
                'value': datetime.now().strftime("%Y-%m-%d"),
                'propertyUri': 'http://nakala.fr/terms#created',
                'typeUri': "http://www.w3.org/2001/XMLSchema#string"
            },
            {
                'value': 'PDM',  # licence code : https://apitest.nakala.fr/vocabularies/licenses
                'propertyUri': 'http://nakala.fr/terms#license',
                'typeUri': "http://www.w3.org/2001/XMLSchema#string"
            }
        ]
    }
    try:
        r = session.post(
            url=f"https://{api_base}/datas",
            headers={'accept': 'application/json', 'X-API-KEY': api_key, 'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as err:
        print('❌', err)


def empty_collection(base, api_key, collection_id):
    page = 1
    r = session.get(
        f"{base}/collections/{collection_id}/datas?page={page}&limit=25",
        headers={'accept': 'application/json', 'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    )
    pprint(r.json()['data'])
