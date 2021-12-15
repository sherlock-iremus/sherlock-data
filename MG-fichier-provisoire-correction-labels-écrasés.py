from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import yaml
import os, sys
import requests
import pandas as pd

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

id_personnes = {}

print("RECUPERATION DES DONNEES DE DIRECTUS")

query = gql("""
query ($page_size: Int) {
	personnes(limit: 500, offset: $page_size) {
    id
    label
	} 
}""")

page_size = 0

while True:

    
    response = client.execute(query, variable_values= {"page_size": page_size} )
    
    for personne in response["personnes"]:
        if personne["id"] not in id_personnes:
            id_personnes[personne["id"]] = personne["label"]
            
            
    print(page_size)
    page_size += 500
    
    if not response["personnes"]:
        
        break

column_names = ["auteur de la musique Nathalie : remplacer directement par l'id de Directus ", "auteur texte Nathalie : normalisation avec Opentheso"]

df = pd.read_csv("corrections_ids.csv", usecols=column_names)

liste_personnes = []

#auteurs_airs = df["auteur de la musique Nathalie : remplacer directement par l'id de Directus "].tolist()
#for auteur in auteurs_airs:
#    if auteur not in liste_personnes:
#        liste_personnes.append(auteur)
#
auteurs_texte = df["auteur texte Nathalie : normalisation avec Opentheso"].tolist()
for auteur in auteurs_texte:
    if auteur not in liste_personnes:
        liste_personnes.append(auteur)


for id in liste_personnes:
    if id in id_personnes:
        print(id, ":", id_personnes[id])

