from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import argparse
from pprint import pprint
import requests
import os
import sys
import yaml
import json
from sherlockcachemanagement import Cache
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Helpers
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# Cache
cache = Cache(args.cache)

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
## COMMANDES
############################################################################################

query = gql("""
query ($page_size: Int) {
	commandes(limit: 100, offset: $page_size) {
        id
        compositeurs {
            personne_id {
                id
            }
        }
        ensembles {
        ensemble_id {
                id
            }
        }
        commanditaires {
            institution_id {
                id
            }
        }
        oeuvre_musicale {
        id
        }
    }
}
""")

print("\nCOMMANDES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for commande in response["commandes"]:
        commande_uri = she(commande["id"])
        t(commande_uri, a, she("Commission"))
        for commanditaire in commande["commanditaires"]:
            t(commande_uri, crm("P14_carried_out_by"), she(commanditaire["institution_id"]["id"]))
        for compositeur in commande["compositeurs"]:
            t(commande_uri, she("commission_received_by"), she(compositeur["personne_id"]["id"]))
        for ensemble in commande["ensembles"]:
            t(commande_uri, she("commission_received_by"), she(ensemble["ensemble_id"]["id"]))
        t(commande_uri, she("commission_of"), she(commande["oeuvre_musicale"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["commandes"]:
        break


############################################################################################
## ENSEMBLES
############################################################################################

query = gql("""
query ($page_size: Int) {
	ensembles(limit: 100, offset: $page_size) {
        id
        nom
    }
}
""")

print("\nENSEMBLES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for ensemble in response["ensembles"]:
        ensemble_uri = she(ensemble["id"])
        t(ensemble_uri, a, crm("E74_Group"))
        E41_uri = she(cache.get_uuid(["ensembles", ensemble_uri, "E41", "uuid"], True))
        t(ensemble_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, RDFS.label, l(ensemble["nom"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["ensembles"]:
        break

############################################################################################
## INSTITUTIONS
############################################################################################

query = gql("""
query ($page_size: Int) {
	institutions(limit: 100, offset: $page_size) {
        id
        nom
    }
}
""")

print("\nINSTITUTIONS")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for institution in response["institutions"]:
        institution_uri = she(institution["id"])
        t(institution_uri, a, crm("E39_Actor"))
        E41_uri = she(cache.get_uuid(["institutions", institution_uri, "E41", "uuid"], True))
        t(institution_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, RDFS.label, l(institution["nom"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["institutions"]:
        break

############################################################################################
## LIEUX DE REPRESENTATION
############################################################################################

query = gql("""
query ($page_size: Int) {
	lieux_de_representation(limit: 100, offset: $page_size) {
        id
        nom
    }
}
""")

print("\nLIEUX DE REPRESENTATION")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for lieu in response["lieux_de_representation"]:
        lieu_uri = she(lieu["id"])
        t(lieu_uri, a, crm("E39_Actor"))
        E41_uri = she(cache.get_uuid(["lieux de représentation", lieu_uri, "E41", "uuid"], True))
        t(lieu_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, RDFS.label, l(lieu["nom"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["lieux_de_representation"]:
        break


############################################################################################
## MAISONS D'EDITION
############################################################################################

query = gql("""
query ($page_size: Int) {
	maisons_d_edition(limit: 100, offset: $page_size) {
        id
        nom
    }
}
""")

print("\nMAISONS D'EDITION")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for maison in response["maisons_d_edition"]:
        maison_uri = she(maison["id"])
        t(maison_uri, a, crm("E39_Actor"))
        E41_uri = she(cache.get_uuid(["maisons d'édition", maison_uri, "E41", "uuid"], True))
        t(maison_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, RDFS.label, l(maison["nom"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["maisons_d_edition"]:
        break


############################################################################################
## OEUVRES LITTERAIRES
############################################################################################

query = gql("""
query ($page_size: Int) {
	oeuvres_litteraires(limit: 100, offset: $page_size) {
        id
        titre
        auteurs {
            personne_id {
                id
            }
        }
        date_de_publication
    }
}
""")

print("\nOEUVRES LITTERAIRES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for oeuvre in response["oeuvres_litteraires"]:
        oeuvre_uri = she(oeuvre["id"])
        t(oeuvre_uri, a, lrm("F2_Expression"))
        E41_uri = she(cache.get_uuid(["oeuvres littéraires", oeuvre_uri, "E41", "uuid"], True))
        t(oeuvre_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, RDFS.label, l(oeuvre["titre"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["oeuvres_litteraires"]:
        break



############################################################################################
## OEUVRES MUSICALES
############################################################################################
#
#query = gql("""
#query ($page_size: Int) {
#	oeuvres_musicales(limit: 100, offset: $page_size) {
#    id
#    titre
#    date_de_composition
#    numero_d_ordre_dans_oeuvre_composite
#    usage_de_l_electronique
#    duree_en_min
#    oeuvres_composites {
#      id
#    }
#    sources_litteraires {
#      id
#    }
#    representations {
#      id
#    }
#    partitions {
#      id
#    }
#    effectifs {
#      id
#    }
#    responsables_de_l_electronique {
#      id
#    }
#  }
#}
#""")
#
#print("\nOEUVRES MUSICALES")
#
#page_size = 0
#
#while True:
#    response = client.execute(query, variable_values= {"page_size": page_size})
#    
#    for oeuvre in response["oeuvres_musicales"]:
#        print(oeuvre["id"])
#
#    print(page_size, "éléments traités")
#    page_size += 100
#
#    if not response["oeuvres_musicales"]:
#        break
#

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

save_graph(args.ttl)

cache.bye()