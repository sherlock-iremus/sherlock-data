import argparse
import glob
from pathlib import Path
import ntpath
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import yaml
import requests
import os, sys
import json
from sherlockcachemanagement import Cache

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--txt")
parser.add_argument("--cache_tei")
parser.add_argument("--cache")
args = parser.parse_args()

# Cache
cache_tei = Cache(args.cache_tei)
cache = Cache(args.cache)

# Helpers RDFlib
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

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


############################################################################################
## FONCTIONS
############################################################################################

init_graph()

############################################################################################
## PERSONNES, LIEUX, CONGREGATIONS
############################################################################################

print("\nPERSONNES, LIEUX, CONGREGATIONS")

query = """
query {
  sources_articles(limit: -1) {
    id
    personnes{personnes_id{id}}
    lieux{lieu_id{id}}
    congregations_religieuses{congregations_religieuses_id{id}}
    }
  }"""

r = requests.post(secret["url"] + '/graphql' + '?access_token=' + access_token, json={'query': query})
print(r.status_code)
result = json.loads(r.text)

for indexation in result["data"]["sources_articles"]:
	id_livraison = indexation["id"][3:].split("_")
	id_livraison = id_livraison[0]
	id_article = indexation["id"][3:]

	# Récupération de l'uuid de l'article dans le cache du corpus
	try:
		F2_article_uri = she(cache_tei.get_uuid(
			["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
	except:
		print("l'article ou la livraison", id_article, "(" + id_livraison + ") est introuvable dans les sources TEI")

	# Personnes
	for personne in indexation["personnes"]:
		uuid_personne = personne["personnes_id"]["id"]
		E13_indexation_uri = she(cache.get_uuid(["indexations", id_article, "personnes", uuid_personne, "E13 Attribute Assignement"], True))
		t(E13_indexation_uri, a, crm("E13_Attribute_Assignement"))
		t(E13_indexation_uri, crm("P14_carried_out_by"),
		  she("684b4c1a-be76-474c-810e-0f5984b47921"))
		t(E13_indexation_uri, crm("P140_assigned_attribute_to"), F2_article_uri)
		t(E13_indexation_uri, crm("P141_assigned"), she(uuid_personne))
		t(E13_indexation_uri, crm("P177_assigned_property_type"), crm("P67_refers_to"))

	# Lieux

	# Congrégations

# Oeuvres citées - ne sont pas issues de Directus mais des fichiers txt des stagiaires
print("\nOEUVRES CITEES")


for file in glob.glob(args.txt + '**/*.txt', recursive=True):
    with open(file, "r") as f:
        lines = f.readlines()

        id_article = ntpath.basename(file)[3:-4]
        id_livraison = id_article.split("_")[0]

        try:
            article = she(cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
        except:
            print(id_article, "(" + id_livraison + "): erreur dans l'id de l'article ou de la livraison")
        else:

            for line in lines:
                if "oeuvres citées=" in line:
                    oeuvre_citée = line[15:].replace("\n", "")

                    uuid_oeuvre_citée = she(cache.get_uuid(["indexations", id_article, "oeuvre citée", oeuvre_citée, "uuid"], True))
                    t(uuid_oeuvre_citée, a, lrm("F2_Expression"))
                    t(uuid_oeuvre_citée, RDFS.label, l(oeuvre_citée))
                    E13_oeuvre_citée = she(cache.get_uuid(["indexations", id_article, "oeuvre citée", oeuvre_citée, id_article, "E13", "uuid"], True))
                    t(E13_oeuvre_citée, a, crm("E13_Attribute_Assignement"))
                    t(E13_oeuvre_citée, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
                    t(E13_oeuvre_citée, crm("P140_assigned_attribute_to"), article)
                    t(E13_oeuvre_citée, crm("P141_assigned"), uuid_oeuvre_citée)
                    t(E13_oeuvre_citée, crm("P177_assigned_property_type"), she("fa4f0240-ce36-4268-8c67-d4aa40cb9350"))


############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

save_graph(args.ttl)

cache.bye()