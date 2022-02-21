from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import argparse
from pprint import pprint
import requests
import os
import sys
import yaml
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Helpers
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
args = parser.parse_args()

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

def make_E13(path, subject, predicate, object):
  E13_uri = she(cache.get_uuid(path, True))
  t(E13_uri, a, crm("E13_Attribute_Assignement"))
  t(E13_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
  t(E13_uri, crm("P140_assigned_attribute_to"), subject)
  t(E13_uri, crm("P141_assigned"), object)
  t(E13_uri, crm("P177_assigned_property_type"), predicate)


############################################################################################
## DONNEES
############################################################################################

query = gql("""
query ($page_size: Int) {
	oeuvres_musicales(limit: 100, offset: $page_size) {
    id
    titre
    date_de_composition
    numero_d_ordre_dans_oeuvre_composite
    usage_de_l_electronique
    duree_en_min
    oeuvres_composites {
      id
    }
    sources_litteraires {
      id
    }
    representations {
      id
    }
    partitions {
      id
    }
    effectifs {
      id
    }
    responsables_de_l_electronique {
      id
    }
  }
}
""")

print("\nOEUVRES MUSICALES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for oeuvre in response["oeuvres_musicales"]:
        print(oeuvre["id"])

    print(page_size, "oeuvres musicales traitées")
    page_size += 100

    if not response["oeuvres_musicales"]:
        break
