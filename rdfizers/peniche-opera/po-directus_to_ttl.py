from rdflib import Graph, Namespace, DCTERMS, RDF, RDFS, SKOS, XSD, URIRef as u, Literal as l
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
        E74_uri = she(ensemble["id"])
        t(E74_uri, a, crm("E74_Group"))
        E41_uri = she(cache.get_uuid(["ensembles", E74_uri, "E41", "uuid"], True))
        t(E74_uri, crm("P1_is_identified_by"), E41_uri)
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
        t(lieu_uri, a, crm("E53_Place"))
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

        # F2 Expression
        F2_uri = she(oeuvre["id"])
        t(F2_uri, a, lrm("F2_Expression"))        
        E35_uri = she(cache.get_uuid(["oeuvres littéraires", F2_uri, "E35", "uuid"], True))
        t(F2_uri, crm("P102_has_title"), E35_uri)
        t(E35_uri, a, crm("E35_Title"))
        t(E35_uri, RDFS.label, l(oeuvre["titre"]))

        # F28 Expression Creation
        F28_uri = she(cache.get_uuid(["oeuvres littéraires", F2_uri, "F28", "uuid"], True))
        t(F28_uri, a, lrm("F28_Expression_Creation"))
        t(F28_uri, lrm("R17_created"), F2_uri)
        if oeuvre["auteurs"] != None:
            for auteur in oeuvre["auteurs"]:
                t(F28_uri, crm("P14_carried_out_by"), she(auteur["personne_id"]["id"]))

        # F3 Manifestation
        F3_uri = she(cache.get_uuid(["oeuvres littéraires", F2_uri, "F3", "uuid"], True))
        t(F3_uri, a, lrm("F3_Manifestation"))
        t(F3_uri, lrm("R4_embodies"), F2_uri)
        
        # F30 Manifestation Creation
        F30_uri = she(cache.get_uuid(["oeuvres littéraires", F2_uri, "F3", "F30", "uuid"], True))
        t(F30_uri, a, lrm("F30_Manifestation_Creation"))
        t(F30_uri, lrm("R24_created"), F3_uri)
        
        if oeuvre["date_de_publication"]:
            E52_uri = she(cache.get_uuid(["oeuvres littéraires", F2_uri, "F3", "F30", "E52", "uuid"], True))
            t(E52_uri, a, crm("E52_Time-Span"))
            date = oeuvre["date_de_publication"]
            t(E52_uri, crm("P82_at_some_time_within"), l(f"{date}-01-01T00:00:00Z", datatype=XSD.dateTime))
            t(F30_uri, crm("P4_has_time-span"), E52_uri)


    print(page_size, "éléments traités")
    page_size += 100

    if not response["oeuvres_litteraires"]:
        break

############################################################################################
## OEUVRES MUSICALES
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
        oeuvre_composite_id {
            id
        }
    }
    sources_litteraires {
        oeuvre_litteraire_id {
            id
        }
    }
    representations {
        id
    }
    librettistes {
        personne_id {
            id
        }
    }
    compositeurs {
        personne_id {
            id
        }
    }
    partitions {
        id
    }
    effectifs {
        voix_et_instrument_id {
            id
            nom
        }
        nombre
    }
    usage_de_l_electronique
    responsables_de_l_electronique {
        id
    }
    producteurs {
        item {
                ... on institutions {
                    id
                }
                ... on ensembles {
                    id
                }
            }
    }
  }
}
""")

print("\nOEUVRES MUSICALES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for oeuvre in response["oeuvres_musicales"]:
        F2_uri = she(oeuvre["id"])
        t(F2_uri, a, lrm("F2_Expression"))
        E35_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "E41", "uuid"], True))
        t(F2_uri, crm("P102_has_title"), E35_uri)
        t(E35_uri, a, crm("E35_Title"))
        t(E35_uri, RDFS.label, l(oeuvre["titre"]))

        # F28 Expression Creation
        F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "uuid"], True))
        t(F28_uri, a, lrm("F28_Expression_Creation"))
        t(F28_uri, lrm("R17_created"), F2_uri)

        # Sous-F28 - Compositeurs
        if oeuvre["compositeurs"] != None:
            sous_F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "compositeurs", "uuid"], True))
            t(sous_F28_uri, a, lrm("F28_Expression_Creation"))
            t(sous_F28_uri, crm("P2_has_type"), she("1d2f3f12-5bde-492e-a8ba-a3ac50652758"))
            t(F28_uri, crm("P9_consists_of"), sous_F28_uri)
            for compositeur in oeuvre["compositeurs"]:
                t(sous_F28_uri, crm("P14_carried_out_by"), she(compositeur["personne_id"]["id"]))
        
        # Sous-F28 - Librettistes
        if oeuvre["librettistes"] != None:
            sous_F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "librettistes", "uuid"], True))
            t(sous_F28_uri, a, lrm("F28_Expression_Creation"))
            t(sous_F28_uri, crm("P2_has_type"), she("5cdb2ecf-c05e-4b97-a51f-49e597e89f54"))
            t(F28_uri, crm("P9_consists_of"), sous_F28_uri)
            for librettiste in oeuvre["librettistes"]:
                t(sous_F28_uri, crm("P14_carried_out_by"), she(librettiste["personne_id"]["id"]))

        # Sous-F28 - Electronique
        if oeuvre["usage_de_l_electronique"] == True:
            sous_F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "électronique", "uuid"], True))
            t(sous_F28_uri, a, lrm("F28_Expression_Creation"))
            t(sous_F28_uri, crm("P2_has_type"), she("caf3ea36-ae41-42dd-a7ed-d7c2405f18a5"))
            t(F28_uri, crm("P9_consists_of"), sous_F28_uri)
            # Erreur - graphql ne récupère par toute la table de jointure mais seulement son champ "id"
            #if oeuvre["responsables_de_l_electronique"] != None:
            #    print(oeuvre["responsables_de_l_electronique"])
            #    for institution in oeuvre["responsables_de_l_electronique"]:
            #        t(sous_F28_uri, crm("P14_carried_out_by"), she(institution["institution_id"]["id"]))

        if oeuvre["numero_d_ordre_dans_oeuvre_composite"] != None:
            t(F2_uri, dor("U10_has_order_number"), l(oeuvre["numero_d_ordre_dans_oeuvre_composite"]))

        # Durée de l'oeuvre
        if oeuvre["duree_en_min"] != None:
            E54_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "E54", "uuid"], True))
            t(E54_uri, a, crm("E54_Dimension"))
            t(E54_uri, crm("P90_has_value"), l(oeuvre["duree_en_min"]))
            t(E54_uri, crm("P91_has_unit"), l("minutes"))
            t(F2_uri, dor("U53_has_duration"), E54_uri)

        # Effectif
        if oeuvre["effectifs"] != None:
                M6_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "M6", "uuid"], True))
                t(M6_uri, a, dor("M6_Casting"))
                t(F2_uri, dor("U13_has_casting"), M6_uri)
                

                for instrument in oeuvre["effectifs"]:
                    M23_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "M6", "M23", instrument["voix_et_instrument_id"]["nom"], "uuid"], True))
                    t(M23_uri, a, dor("M23_Casting_Detail"))
                    t(M6_uri, dor("U23_has_casting_detail"), M23_uri)
                    t(M23_uri, dor("U2_foresees_use_of_medium_of_performance"), she(instrument["voix_et_instrument_id"]["id"]))
                    if instrument["nombre"] != None:
                        t(M23_uri, dor("U30_foresees_quantity_of_medium_of_performance"), l(instrument["nombre"]))

        # Source littéraire
        if oeuvre["sources_litteraires"] != None:
            for source in oeuvre["sources_litteraires"]:
                t(F2_uri, crm("P130_shows_features_of"), she(source["oeuvre_litteraire_id"]["id"]))

        # Partitions
        if oeuvre["partitions"] != None:
            for partition in oeuvre["partitions"]:  
                t(she(partition["id"]), lrm("R4_embodies"), F2_uri)

        # Producteurs TODO Revoir avec Thomas suite à la suppression de "commandes"
        if len(oeuvre["producteurs"]) >= 1:
            commande_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "producteur", "uuid"], True))
            t(commande_uri, a, she_ns("Commission"))
            t(commande_uri, she_ns("commission_of"), F2_uri)
            for compositeur in oeuvre["compositeurs"]:
                t(commande_uri, she_ns("commission_received_by"), she(compositeur["personne_id"]["id"]))
            for producteur in oeuvre["producteurs"]:    
                t(commande_uri, crm("P14_carried_out_by"), she(producteur["item"]["id"]))

# TODO ajouter idée d'autonomie d'une oeuvre

    print(page_size, "éléments traités")
    page_size += 100

    if not response["oeuvres_musicales"]:
        break


############################################################################################
## OEUVRES MUSICALES - OEUVRES COMPOSITES
############################################################################################

query = gql("""
query ($page_size: Int) {
	oeuvres_musicales_oeuvres_composites(limit: 100, offset: $page_size) {
        oeuvre_musicale_id {
            id
        }
        oeuvre_composite_id {
            id
        }
        autonome
        commentaire
    }
}
""")

print("\nOEUVRES MUSICALES - OEUVRES COMPOSITES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for oeuvre in response["oeuvres_musicales_oeuvres_composites"]:
        F2_uri = she(oeuvre["oeuvre_musicale_id"]["id"])

        # Autonomie de la sous-oeuvre
        if oeuvre["autonome"] == True or oeuvre["autonome"] == None:
            t(she(oeuvre["oeuvre_composite_id"]["id"]), crm("P165_incorporates"), F2_uri)
        
        if oeuvre["autonome"] == False:
            t(she(oeuvre["oeuvre_composite_id"]["id"]), crm("P148_has_component"), F2_uri)

        if oeuvre["commentaire"] != None:
            E13_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "commentaire sous-oeuvre", "E13", "uuid"], True))
            t(E13_uri, a, crm("E13_Attribute_Assignement"))
            t(E13_uri, crm("P14_carried_out_by"), she(""))
            t(E13_uri, crm("P140_assigned_attribute_to"), F2_uri)
            t(E13_uri, crm("P141_assigned"), l(oeuvre["commentaire"]))
            t(E13_uri, crm("P177_assigned_property_type"), crm("P3_has_note"))


    print(page_size, "éléments traités")
    page_size += 100

    if not response["oeuvres_musicales_oeuvres_composites"]:
        break


############################################################################################
## PERSONNES
############################################################################################

query = gql("""
query ($page_size: Int) {
	personnes(limit: 100, offset: $page_size) {
        id
        Nom
        Prenom
        date_de_naissance
        date_de_mort
    }
}
""")

print("\nPERSONNES")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for personne in response["personnes"]:
        E21_uri = she(personne["id"])
        t(E21_uri, a, crm("E21_Person"))
        nom = str(personne["Prenom"]) + " " + str(personne["Nom"])
        E41_uri = she(cache.get_uuid(["personnes", E21_uri, "E41", "uuid"], True))
        t(E21_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, RDFS.label, l(nom))


        # Naissance de la personne
        E67_uri = she(cache.get_uuid(["personnes", E21_uri, "E67", "uuid"], True))
        t(E67_uri, a, crm("E67_Birth"))
        t(E67_uri, crm("P98_brought_into_life"), E21_uri)
        if personne["date_de_naissance"] != None:
            E52_uri = she(cache.get_uuid(["personnes", E21_uri, "E67", "E52", "uuid"], True))
            t(E52_uri, a, crm("E52_Time-Span"))
            t(E67_uri, crm("P4_has_time-span"), E52_uri)
            date = personne["date_de_naissance"]
            t(E52_uri, crm("P82_at_some_time_within"), l(f"{date}-01-01T00:00:00Z", datatype=XSD.dateTime))
                    
        # Mort de la personne
        E69_uri = she(cache.get_uuid(["personnes", E21_uri, "E69", "uuid"], True))
        t(E69_uri, a, crm("E69_Death"))
        t(E69_uri, crm("P100_was_death_of"), E21_uri)
        if personne["date_de_mort"] != None:
            E52_uri = she(cache.get_uuid(["personnes", E21_uri, "E69", "E52", "uuid"], True))
            t(E52_uri, a, crm("E52_Time-Span"))
            t(E69_uri, crm("P4_has_time-span"), E52_uri)
            date = personne["date_de_mort"]
            t(E52_uri, crm("P82_at_some_time_within"), l(f"{date}-01-01T00:00:00Z", datatype=XSD.dateTime))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["personnes"]:
        break


############################################################################################
## PARTITIONS
############################################################################################

query = gql("""
query ($page_size: Int) {
	partitions(limit: 100, offset: $page_size) {
        id
        titre
        edition {
            item {
                ... on personnes {
                    id
                }
                ... on maisons_d_edition {
                    id
                }
            }
        }
        notes
    }
}
""")

print("\nPARTITIONS")

page_size = 0

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for partition in response["partitions"]:
        F3_uri = she(partition["id"])
        t(F3_uri, a, crm("F3_Manifestation"))
        E35_uri = she(cache.get_uuid(["partitions", F3_uri, "E35", "uuid"], True))
        t(F3_uri, crm("P102_has_title"), E35_uri)
        t(E35_uri, a, crm("E35_Title"))
        t(E35_uri, RDFS.label, l(partition["titre"]))
        t(F3_uri, crm("P2_has_type"), she("792f6ea9-3d3d-4504-9042-4a3f8e23f542"))                     
        ## t(F3_uri, crm("P2_has_type"), she(type de partition))

        # F30 Manifestation Creation
        if partition["edition"] != None:
            F30_uri = she(cache.get_uuid(["partitions", F3_uri, "F30", "uuid"], True))
            t(F30_uri, a, lrm("F30_Manifestation_Creation"))
            t(F30_uri, lrm("R24_created"), F3_uri)
            for editeur in partition["edition"]:
                t(F30_uri, crm("P14_carried_out_by"), she(editeur["item"]["id"]))

        # Notes
        if partition["notes"]:
            t(F3_uri, crm("P3_has_note"), l(partition["notes"]))

    print(page_size, "éléments traités")
    page_size += 100

    if not response["partitions"]:
        break


############################################################################################
## VOIX ET INSTRUMENTS
############################################################################################

query = gql("""
query ($page_size: Int) {
	voix_et_instruments(limit: 100, offset: $page_size) {
        id
        nom
    }
}
""")

print("\nVOIX ET INSTRUMENTS")

page_size = 0  

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for instrument in response["voix_et_instruments"]:
        E55_uri = she(instrument["id"])
        t(E55_uri, a, crm("E55_Type"))
        t(E55_uri, crm("P1_is_identified_by"), l(instrument["nom"]))
    
    print(page_size, "éléments traités")
    page_size += 100

    if not response["voix_et_instruments"]:
        break


############################################################################################
## DATES
############################################################################################

query = gql("""
query ($page_size: Int) {
	dates(limit: 100, offset: $page_size) {
        id
        date
        type_de_representation
        representation {
            oeuvre_musicale {
                id
            }
        }
        premieres_representations {
            oeuvre_musicale {
                id
            }
        }
        dernieres_representations {
            oeuvre_musicale {
                id
            }
        }           
    }
}
""")

print("\nDATES")

page_size = 0  

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for date in response["dates"]:
        F31_uri = she(date["id"])
        t(F31_uri, a, crm("F31_Performance"))
        if date["representation"] != None:
            t(F31_uri, lrm("R66_included_performed_version_of"), she(date["representation"]["oeuvre_musicale"]["id"]))
        elif len(date["premieres_representations"]) >= 1:
            for premiere in date["premieres_representations"]:
                t(F31_uri, lrm("R66_included_performed_version_of"), she(premiere["oeuvre_musicale"]["id"]))
                t(F31_uri, crm("P2_has_type"), she("441ffd78-a065-420f-bb5a-87779dd133c7"))
        else:
            for derniere in date["dernieres_representations"]:
                t(F31_uri, lrm("R66_included_performed_version_of"), she(derniere["oeuvre_musicale"]["id"]))
                t(F31_uri, crm("P2_has_type"), she("77e3eba7-154b-4a42-afde-a73c03839faf"))

        # Type de representation
        if date["type_de_representation"] == "Creation":
            t(F31_uri, crm("P2_has_type"), she("c9ce4b81-5bc1-43d4-986d-4ff98f4f60fb"))
        if date["type_de_representation"] == "Re Creation":
            t(F31_uri, crm("P2_has_type"), she("ce4b0274-4697-44e2-9610-a72714a4ea56"))
        if date["type_de_representation"] == "Reprise":
            t(F31_uri, crm("P2_has_type"), she("caafe301-465c-4084-966f-c1e939d40819"))

        # Date
        E52_uri = she(cache.get_uuid(["representations", F31_uri, "E52", "uuid"], True))
        t(F31_uri, crm("P4_has_time-span"), E52_uri)
        date = date["date"]
        # TODO Supprimer l'horaire du datetime? 
        t(E52_uri, crm("P82_at_some_time_within"), l(f"{date}T00:00:00Z", datatype=XSD.dateTime))    

        
    print(page_size, "éléments traités")
    page_size += 100

    if not response["dates"]:
        break

############################################################################################
## REPRESENTATIONS
############################################################################################

query = gql("""
query ($page_size: Int) {
	representations(limit: 100, offset: $page_size) {
            id
        oeuvre_musicale {
        id
        }
        lieu {
        id
        }
        ensemble {
        id
        }
        usage_de_l_electronique
        date_de_debut {
        id
        }
        date_de_fin {
        id
        }
        presence_d_un_chef_d_orchestre
        chef_d_orchestre {
        id
        }
        dates {
        id
        }
        interpretes {
        personne_id {
            id
            Nom
        }
        }
        decors {
        personne_id {
            id
        }
        }
        mise_en_scene {
        personne_id {
            id
        }
        }
        effectif {
        voix_et_instrument_id {
            id
            nom
        }
        nombre
        musiciens {
            personne_id {
                id
                Nom
            }
        }
        }
        images_et_video {
        personne_id {
            id
        }
        }
        marionnettes {
        personne_id {
            id
        }
        }
        direction_technique {
        personne_id {
            id
        }
        }
        danseurs {
        personne_id {
            id
        }
        }
        scenographie {
        personne_id {
            id
        }
        }
        choregraphie {
        personne_id {
            id
        }
        }
        sonorisation {
        personne_id {
            id
        }
        }
        costumes {
        personne_id {
            id
        }
        }
        dialogues {
        personne_id {
            id
        }
        }
        bande_son {
        personne_id {
            id
        }
        }
        maquillage {
        personne_id {
            id
        }
        }
        regie {
        personne_id {
            id
        }
        }
        eclairages {
        personne_id {
            id
        }
        }
        conseil_gastronomique {
        personne_id {
            id
        }
        }
        dramaturgie {
        personne_id {
            id
        }
        }
        direction_musicale {
        personne_id {
            id
        }
        type
        } 
    }
}
""")

print("\nREPRESENTATIONS")

page_size = 0  

def create_M42_M28(nom, champ, type_po):
    M42_uri = she(cache.get_uuid(["representations", F31_uri, nom, "uuid"], True))
    t(M42_uri, a, dor("M42_Performed_Expression_Creation"))
    t(M42_uri, crm("P2_has_type"), she(type_po))
    t(F31_uri, crm("P9_consists_of"), M42_uri)
    if len(representation[champ]) >= 1:
        for i in representation[champ]:
            M28_uri = she(cache.get_uuid(["representations", F31_uri, nom, "M28", i["personne_id"]["Nom"], "uuid"], True))
            t(M28_uri, a, dor("M28_Individual_Performance"))
            t(M42_uri, crm("P9_consists_of"), M28_uri)
            t(M28_uri, crm("P14_carried_out_by"), she(i["personne_id"]["id"]))

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})
    
    for representation in response["representations"]:
        ids = []
        if len(representation["dates"]) >= 1:
            for date in representation["dates"]:
                ids.append(date["id"])
        else:
            if representation["date_de_debut"] != None:
                ids.append(representation["date_de_debut"]["id"])
            if representation["date_de_fin"] != None:
                ids.append(representation["date_de_fin"]["id"])     
        
        for id in ids:
            F31_uri = she(id)
            
            # Lieu
            t(F31_uri, crm("P7_took_place_at"), she(representation["lieu"]["id"]))

            # Mise en scène
            F28_uri = she(cache.get_uuid(["representations", F31_uri, "mise en scène", "uuid"], True))
            t(F28_uri, a, lrm("F28_Expression_Creation"))
            t(F28_uri, crm("P2_has_type"), she("8d8a50cb-db2e-4c2a-b513-1e646abdf9ba"))
            t(F31_uri, crm("P9_consists_of"), F28_uri)
            if len(representation["mise_en_scene"]) >= 1:
                for mise_en_scene in representation["mise_en_scene"]:
                    t(F28_uri, crm("P14_carried_out_by"), she(mise_en_scene["personne_id"]["id"]))
            
            # Interprètes
            create_M42_M28("interprétation", "interpretes", "8d5b9d50-27a1-488a-82a6-19ee59acd847")

            # Danseurs
            create_M42_M28("danse", "danseurs", "68b77a08-d6c8-42ed-bd3d-a922ec52b064")

            # Effectif
            M42_uri = she(cache.get_uuid(["representations", F31_uri, "musique", "uuid"], True))
            t(M42_uri, a, dor("M42_Performed_Expression_Creation"))
            t(M42_uri, crm("P2_has_type"), she("c0e9693e-3e60-4d89-b005-56dcd864180d"))
            t(F31_uri, crm("P9_consists_of"), M42_uri)
            if len(representation["effectif"]) >= 1:
                for effectif in representation["effectif"]:
                    # TODO tester ce if quand on aura des musiciens dans la base
                    if effectif["nombre"] != None and effectif["nombre"]>= 2:
                        nombre = effectif["nombre"]
                        for i in range(nombre):
                            M28_uri = she(cache.get_uuid(["representations", F31_uri, "musique", "M28", effectif["voix_et_instrument_id"]["nom"], i, "uuid"], True))
                            t(M28_uri, a, dor("M28_Individual_Performance"))
                            t(M42_uri, crm("P9_consists_of"), M28_uri)
                            t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))
                            if len(effectif["musiciens"]) >= 2:
                                musicien = effectif["musiciens"][i]["personne_id"]["id"]
                                t(M28_uri, crm("P14_carried_out_by"), she(musicien))
                    elif len(effectif["musiciens"]) >= 2:
                        for musicien in effectif["musiciens"]:
                            M28_uri = she(cache.get_uuid(["representations", F31_uri, "musique", "M28", effectif["voix_et_instrument_id"]["nom"], musicien["personne_id"]["Nom"], "uuid"], True))
                            t(M28_uri, a, dor("M28_Individual_Performance"))
                            t(M42_uri, crm("P9_consists_of"), M28_uri)
                            t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))
                            t(M28_uri, crm("P14_carried_out_by"), she(musicien["personne_id"]["id"]))
                    else:
                        M28_uri = she(cache.get_uuid(["representations", F31_uri, "musique", "M28", effectif["voix_et_instrument_id"]["nom"], "uuid"], True))
                        t(M28_uri, a, dor("M28_Individual_Performance"))
                        t(M42_uri, crm("P9_consists_of"), M28_uri)
                        t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))

    print(page_size, "éléments traités")
    page_size += 100
    

    if not response["representations"]:
        break

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

save_graph(args.ttl)

cache.bye()