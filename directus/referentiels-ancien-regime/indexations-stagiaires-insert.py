from delete_and_send_data import delete, send_data, send_indexations
import argparse
import glob
from pathlib import Path
import ntpath
from pprint import pprint
from sherlockcachemanagement import Cache
import json
import sys
import os
import requests
import yaml
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

sys.path.append(os.path.abspath(os.path.join('directus/referentiels-ancien-regime/', '')))

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login", json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Sélection de l'URL des requêtes GraphQL et création d'un client l'utilisant
transport = AIOHTTPTransport(url=secret["url"] + '/graphql' + '?access_token=' + access_token)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--txt")
parser.add_argument("--cache_personnes")
parser.add_argument("--cache_lieux")
parser.add_argument("--cache_mots_clefs")
parser.add_argument("--cache_stagiaires")
parser.add_argument("--cache_congregations")

args = parser.parse_args()

# Caches
cache_personnes = Cache(args.cache_personnes)
cache_lieux = Cache(args.cache_lieux)
cache_congregations = Cache(args.cache_congregations)
cache_mots_clefs = Cache(args.cache_mots_clefs)

# Récupération des indexations déjà présentes dans Directus
def get_indexations(collection, articles, query_body, index, champ1, champ2):

    query = gql(query_body)

    page_size = 0

    while True:
        response = client.execute(query, variable_values={"page_size": page_size})
        for i in response[index]:
            collection.append({champ1: i[champ1]["id"], champ2: i[champ2]["id"]})
            articles.append(i[champ2]["id"])
        page_size += 500
        if not response[index]:
            break


articles = []

# Personnes
personnes = []
query = """
		query ($page_size: Int) {
			sources_articles_personnes(limit: 500, offset: $page_size){
				sources_articles_id {
				id
				}
				personnes_id {
				id
				}
			}
		}
		"""
get_indexations(personnes, articles, query, "sources_articles_personnes", "personnes_id", "sources_articles_id")

# Lieux
lieux = []
query = """
		query ($page_size: Int) {
			sources_articles_lieux(limit: 500, offset: $page_size){
				source_article_id {
				id
				}
				lieu_id {
				id
				}
			}
		}
		"""
get_indexations(lieux, articles, query, "sources_articles_lieux", "lieu_id", "source_article_id")

print(len(articles), "articles indexés dans la base\n")

# Fichiers TXT contenant les indexations
for file in glob.glob(args.txt + '**/*.txt', recursive=True):
    with open(file, "r") as f:
        lines = f.readlines()

        id_article = ntpath.basename(file)[0:-4]
        print("\n" + id_article)
        if id_article not in articles:
            print("Ajout de l'article dans Directus")
            r = requests.post(secret["url"] + '/items/sources_articles?access_token=' + access_token, json={"id": id_article})
            print(r.json())

        for line in lines:
            line = line.split("=")
            if line[0] == "personnes":

                id = line[1].strip().replace("\n", "")
                try:
                    uuid = cache_personnes.get_uuid(["personnes", id, "uuid"])
                    body = {"personnes_id": uuid, "sources_articles_id": id_article}
                    if body in personnes:
                        pass
                    else:
                        try:
                            r = requests.post(secret["url"] + '/items/sources_articles_personnes?access_token=' + access_token, json=body)
                            print(r.json())
                        except Exception as e:
                            print("voici une erreur")
                            print(e)
                except:
                    print(line[1], ": introuvable dans le cache des personnes")

            if line[0] == "lieux":
                id = line[1].strip().replace("\n", "")
                try:
                    uuid = cache_lieux.get_uuid(["lieux", id, "E93", "uuid"])
                    body = {"lieu_id": uuid, "source_article_id": id_article}
                    if body in lieux:
                        pass
                    else:
                        try:
                            r = requests.post(secret["url"] + '/items/sources_articles_lieux?access_token=' + access_token, json=body)
                            print(r.json())
                        except Exception as e:
                            print("voici une erreur")
                            print(e)
                except:
                    print(line[1], ": introuvable dans le cache des lieux")

            # TODO Congrégations

            # TODO Pas de référentiel des institutions (il doit être entièrement remanié dans Directus)
