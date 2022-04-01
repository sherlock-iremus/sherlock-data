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
        membres {
            id
        }
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
        t(E74_uri, crm("P2_has_type"), she("a00ca873-c10a-4ca6-8a4f-835d7e9bd211"))
        for membre in ensemble["membres"]:
            t(E74_uri, crm("P107_has_current_or_former_member"), she(membre["id"]))

        E41_uri = she(cache.get_uuid(["ensembles", E74_uri, "E41", "uuid"], True))
        t(E74_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, crm("P190_has_symbolic_content"), l(ensemble["nom"]))

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
        E39_uri = she(institution["id"])
        t(E39_uri, a, crm("E39_Actor"))
        t(E39_uri, crm("P2_has_type"), she("d214ea65-1734-41d8-a0e6-e3dbbab3849a"))
        E41_uri = she(cache.get_uuid(["institutions", E39_uri, "E41", "uuid"], True))
        t(E39_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, crm("P190_has_symbolic_content"), l(institution["nom"]))

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
        t(E41_uri, crm("P190_has_symbolic_content"), l(lieu["nom"]))

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
        E39_uri = she(maison["id"])
        t(E39_uri, a, crm("E39_Actor"))
        t(E39_uri, crm("P2_has_type"), she(""))
        E41_uri = she(cache.get_uuid(["maisons d'édition", E39_uri, "E41", "uuid"], True))
        t(E39_uri, crm("P1_is_identified_by"), E41_uri)
        t(E41_uri, a, crm("E41_Appellation"))
        t(E41_uri, crm("P190_has_symbolic_content"), l(maison["nom"]))

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
        t(E35_uri, crm("P190_has_symbolic_content"), l(oeuvre["titre"]))

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
        institution_id {
            id
            nom
        }
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
        t(E35_uri, crm("P190_has_symbolic_content"), l(oeuvre["titre"]))

        # F28 Expression Creation
        F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "uuid"], True))
        t(F28_uri, a, lrm("F28_Expression_Creation"))
        t(F28_uri, lrm("R17_created"), F2_uri)

        # Sous-F28 Composition
        if oeuvre["compositeurs"] != None:
            sous_F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "compositeurs", "uuid"], True))
            t(sous_F28_uri, a, lrm("F28_Expression_Creation"))
            t(sous_F28_uri, crm("P2_has_type"), she("1d2f3f12-5bde-492e-a8ba-a3ac50652758"))
            t(F28_uri, crm("P9_consists_of"), sous_F28_uri)
            for compositeur in oeuvre["compositeurs"]:
                t(sous_F28_uri, crm("P14_carried_out_by"), she(compositeur["personne_id"]["id"]))
            
            # Sous-F28 Ecriture électronique (intégré au sous-F28 Composition)
            if oeuvre["usage_de_l_electronique"] == True:
                electro_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "électronique", "uuid"], True))
                t(electro_uri, a, lrm("F28_Expression_Creation"))
                t(electro_uri, crm("P2_has_type"), she("caf3ea36-ae41-42dd-a7ed-d7c2405f18a5"))
                t(electro_uri, crm("P14_carried_out_by"), she(compositeur["personne_id"]["id"]))
                t(sous_F28_uri, crm("P9_consists_of"), electro_uri)
                # Erreur - graphql ne récupère par toute la table de jointure mais seulement son champ "id"
                if oeuvre["responsables_de_l_electronique"] != None:
                    for institution in oeuvre["responsables_de_l_electronique"]:
                        t(electro_uri, crm("P14_carried_out_by"), she(institution["institution_id"]["id"]))
        
        # Sous-F28 Libretto
        if oeuvre["librettistes"] != None:
            sous_F28_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "F28", "librettistes", "uuid"], True))
            t(sous_F28_uri, a, lrm("F28_Expression_Creation"))
            t(sous_F28_uri, crm("P2_has_type"), she("5cdb2ecf-c05e-4b97-a51f-49e597e89f54"))
            t(F28_uri, crm("P9_consists_of"), sous_F28_uri)
            for librettiste in oeuvre["librettistes"]:
                t(sous_F28_uri, crm("P14_carried_out_by"), she(librettiste["personne_id"]["id"]))

        # Numéro d'ordre dans l'oeuvre composite
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

        # Producteurs
        if len(oeuvre["producteurs"]) >= 1:
            commande_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "producteur", "uuid"], True))
            t(commande_uri, a, she_ns("Commission"))
            t(commande_uri, she_ns("commission_of"), F2_uri)
            for compositeur in oeuvre["compositeurs"]:
                t(commande_uri, she_ns("commission_received_by"), she(compositeur["personne_id"]["id"]))
            for producteur in oeuvre["producteurs"]:    
                t(commande_uri, crm("P14_carried_out_by"), she(producteur["item"]["id"]))

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
        t(F2_uri, crm("P2_has_type"), she("b9b15a16-0c60-499a-8eca-dc8dee26c5a8"))

        # Autonomie de la sous-oeuvre
        if oeuvre["autonome"] == True or oeuvre["autonome"] == None:
            t(she(oeuvre["oeuvre_composite_id"]["id"]), crm("P165_incorporates"), F2_uri)
        
        if oeuvre["autonome"] == False:
            t(she(oeuvre["oeuvre_composite_id"]["id"]), crm("P148_has_component"), F2_uri)

        if oeuvre["commentaire"] != None:
            E13_uri = she(cache.get_uuid(["oeuvres musicales", F2_uri, "commentaire sous-oeuvre", "E13", "uuid"], True))
            t(E13_uri, a, crm("E13_Attribute_Assignement"))
            t(E13_uri, crm("P14_carried_out_by"), she("60324ad9-35a3-489f-a203-5aecc435f7aa"))
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
        t(E41_uri, crm("P190_has_symbolic_content"), l(nom))


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
        t(E35_uri, crm("P190_has_symbolic_content"), l(partition["titre"]))
        t(F3_uri, crm("P2_has_type"), she("792f6ea9-3d3d-4504-9042-4a3f8e23f542"))                     
        ## t(F3_uri, crm("P2_has_type"), she(type de partition))
        t(F3_uri, lrm("R4_embodies"), F2_uri)

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
        M14_uri = she(instrument["id"])
        t(M14_uri, a, crm("M14_Medium_of_Performance"))
        t(M14_uri, crm("P1_is_identified_by"), l(instrument["nom"]))
    
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
        date_uri = she(date["id"])

        # Type de representation
        if date["type_de_representation"] == "Creation":
            t(date_uri, crm("P2_has_type"), she("c9ce4b81-5bc1-43d4-986d-4ff98f4f60fb"))
        if date["type_de_representation"] == "Re Creation":
            t(date_uri, crm("P2_has_type"), she("ce4b0274-4697-44e2-9610-a72714a4ea56"))
        if date["type_de_representation"] == "Reprise":
            t(date_uri, crm("P2_has_type"), she("caafe301-465c-4084-966f-c1e939d40819"))
    
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
        date_de_debut {
            id
            date
        }
        date_de_fin {
            id
            date
        }
        presence_d_un_chef_d_orchestre
        chef_d_orchestre {
            id
            Nom
        }
        dates {
            id
            date
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
                Nom
            }
        }
        mise_en_scene {
            personne_id {
                id
                Nom
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
                Nom
            }
        }
        marionnettes {
            personne_id {
                id
                Nom
            }
        }
        direction_technique {
            personne_id {
                id
                Nom
            }
        }
        danseurs {
            personne_id {
                id
                Nom
            }
        }
        scenographie {
            personne_id {
                id
                Nom
            }
        }
        choregraphie {
            personne_id {
                id
                Nom
            }
            }
        sonorisation {
            personne_id {
                id
                Nom
            }
        }
        costumes {
            personne_id {
                id
                Nom
            }
        }
        dialogues {
            personne_id {
                id
                Nom
            }
        }
        bande_son {
            personne_id {
                id
                Nom
            }
        }
        maquillage {
            personne_id {
                id
                Nom
            }
            }
        regie {
            personne_id {
                id
                Nom
            }
        }
        eclairages {
            personne_id {
                id
                Nom
            }
        }
        conseil_gastronomique {
            personne_id {
                id
                Nom
            }
        }
        dramaturgie {
            personne_id {
                id
                Nom
            }
        }
        direction_musicale {
            personne_id {
                id
                Nom
            }
            type
        } 
    }
}
""")

print("\nREPRESENTATIONS")

page_size = 0  

def create_M42_M43_M28(F31, nom, champ, P2_type):
    if representation[champ] != None and len(representation[champ]) >= 1:
        M42_uri = she(cache.get_uuid(["representations", F31, nom, "uuid"], True))
        t(M42_uri, a, dor("M42_Performed_Expression_Creation"))
        t(M42_uri, crm("P2_has_type"), she(P2_type))
        t(F31, crm("P9_consists_of"), M42_uri)
        M43_uri = she(cache.get_uuid(["representations", F31, nom, "M43", "uuid"], True))
        t(M43_uri, a, dor("M43_Performed_Expression"))
        t(M43_uri, dor("U54_is_performed_expression_of"), she(representation["oeuvre_musicale"]["id"]))
        t(M42_uri, lrm("R17_created"), M43_uri)
        if nom == "chef d'orchestre":
            M28_uri = she(cache.get_uuid(["representations", F31, nom, "M28", representation[champ]["Nom"], "uuid"], True))
            t(M28_uri, a, dor("M28_Individual_Performance"))
            t(M42_uri, crm("P9_consists_of"), M28_uri)
            t(M28_uri, crm("P14_carried_out_by"), she(representation[champ]["id"]))
        else:
            for i in representation[champ]:
                M28_uri = she(cache.get_uuid(["representations", F31, nom, "M28", i["personne_id"]["Nom"], "uuid"], True))
                t(M28_uri, a, dor("M28_Individual_Performance"))
                t(M42_uri, crm("P9_consists_of"), M28_uri)
                t(M28_uri, crm("P14_carried_out_by"), she(i["personne_id"]["id"]))
                # S'il s'agit du champ "direction musicale", on récupère son type
                try:
                    t(M28_uri, crm("P2_has_type"), l(i["type"]))
                except:
                    pass


def create_E29(nom, champ, P2_type):
    if len(representation[champ]) >= 1:
        E29_uri = she(cache.get_uuid(["performance plan", F31_serie_uri, nom, "uuid"], True))
        t(E29_uri, a, crm("E29_Design_or_Procedure"))
        t(E29_uri, a, lrm("F2_Expression"))
        t(E29_uri, crm("P2_has_type"), she(P2_type))
        t(pp_uri, crm("P165_incorporates"), E29_uri)
        E29_F28_uri = she(cache.get_uuid(["performance plan", F31_serie_uri, nom, "F28", "uuid"], True))
        t(E29_F28_uri, a, lrm("F28_Expression_Creation"))
        t(E29_F28_uri, lrm("R17_created"), E29_uri)
        for i in representation[champ]:
            t(E29_F28_uri, crm("P14_carried_out_by"), she(i["personne_id"]["id"]))

while True:
    response = client.execute(query, variable_values= {"page_size": page_size})

    #--------------------------------------------------------------------------------------
    #  Série de représentations
    #--------------------------------------------------------------------------------------     

    for representation in response["representations"]:

        F31_serie_uri = she(representation["id"])
        t(F31_serie_uri, a, lrm("F31_Performance"))
        t(F31_serie_uri, crm("P2_has_type"), she("ffc01a36-69b8-4ca2-9048-714961d1397b"))
        t(F31_serie_uri, lrm("R66_included_performed_version_of"), she(representation["oeuvre_musicale"]["id"]))

        #--------------------------------------------------------------------------------------
        #  Performance Plan (F25 déprécié, devenu E29/F2)
        #-------------------------------------------------------------------------------------- 

        pp_uri = she(cache.get_uuid(["performance plan", F31_serie_uri, "uuid"], True))
        t(pp_uri, a, crm("E29_Design_or_Procedure"))
        t(pp_uri, a, lrm("F2_Expression"))
        t(pp_uri, crm("P2_has_type"), she("de64ccd2-6a0a-4017-b3fe-7530a27d778c"))
        t(pp_uri, crm("P165_incorporates"), she(representation["oeuvre_musicale"]["id"]))

        t(F31_serie_uri, lrm("R66_included_performed_version_of"), pp_uri)
        
        # Chorégraphie
        create_E29("chorégraphie", "choregraphie", "561e8ef8-6786-4df4-8cd5-c74479860753")

        # Mise en scène
        create_E29("mise en scène", "mise_en_scene", "ff33c9d3-8e91-4b1e-ba5c-1d7f4c8c34bd")

        # Scénographie
        create_E29("scénographie", "scenographie", "e5e5890d-d774-43cc-b573-e1dc871bd05b")

        # Dramaturgie
        create_E29("dramaturgie", "dramaturgie", "12597890-dcac-42f4-b780-d9795364ed74")

        # Dialogues
        create_E29("dialogues", "dialogues", "63da5276-9d37-4e5f-9d40-b16723c42ed2")

        # Conseil gastronomique à ignorer pour l'instant - pas de données

        # Costumes
        create_E29("costumes", "costumes", "181dc490-d221-41e8-81e6-1de21326c15f")

        # Décors
        create_E29("décors", "decors", "06a632d6-44c5-4337-8922-a04e5bd3641e")

        #--------------------------------------------------------------------------------------
        #  Dates de représentations (F31 pour chaque date de la représentation)
        #-------------------------------------------------------------------------------------- 

        # Si on a plusieurs dates de représentations, on associera tous les champs de la table
        # "representations" à chaque date de représentation.
        # Si on n'a qu'une date de début et de fin pour la série de représentations,
        # on associera tous les champs de la table "representations" à la série de représentations.
        
        # 1. Association des champs de la table "representations" à chaque date de représentation
        if len(representation["dates"]) >= 1:
            ids = []

            for date in representation["dates"]:
                ids.append(date["id"])
            
            for id in ids:
                F31_uri = she(id)
                t(F31_uri, a, crm("F31_Performance"))
                t(F31_serie_uri, crm("P9_consists_of"), F31_uri)

                # Date
                E52_uri = she(cache.get_uuid(["representations", F31_uri, "E52", "uuid"], True))
                t(F31_uri, crm("P4_has_time-span"), E52_uri)
                date_iso = date["date"]
                t(E52_uri, crm("P82_at_some_time_within"), l(f"{date_iso}T00:00:00Z", datatype=XSD.dateTime))  

                # Lieu
                t(F31_uri, crm("P7_took_place_at"), she(representation["lieu"]["id"]))

                # Effectif
                M42_uri = she(cache.get_uuid(["representations", F31_uri, "effectif", "uuid"], True))
                t(M42_uri, a, dor("M42_Performed_Expression_Creation"))
                t(M42_uri, crm("P2_has_type"), she("c0e9693e-3e60-4d89-b005-56dcd864180d"))
                t(F31_uri, crm("P9_consists_of"), M42_uri)
                M43_uri = she(cache.get_uuid(["representations", F31_uri, "effectif", "M43", "uuid"], True))
                t(M43_uri, a, dor("M43_Performed_Expression"))
                t(M42_uri, lrm("R17_created"), M43_uri)
                t(M43_uri, dor("U54_is_performed_expression_of"), she(representation["oeuvre_musicale"]["id"]))
                if len(representation["effectif"]) >= 1:
                    for effectif in representation["effectif"]:
                        # TODO tester ce if quand on aura des musiciens dans la base
                        if effectif["nombre"] != None and effectif["nombre"]>= 2:
                            nombre = effectif["nombre"]
                            for i in range(nombre):
                                M28_uri = she(cache.get_uuid(["representations", F31_uri, "effectif", "M28", effectif["voix_et_instrument_id"]["nom"], i, "uuid"], True))
                                t(M28_uri, a, dor("M28_Individual_Performance"))
                                t(M42_uri, crm("P9_consists_of"), M28_uri)
                                t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))
                                if len(effectif["musiciens"]) >= 2:
                                    musicien = effectif["musiciens"][i]["personne_id"]["id"]
                                    t(M28_uri, crm("P14_carried_out_by"), she(musicien))
                        elif len(effectif["musiciens"]) >= 2:
                            for musicien in effectif["musiciens"]:
                                M28_uri = she(cache.get_uuid(["representations", F31_uri, "effectif", "M28", effectif["voix_et_instrument_id"]["nom"], musicien["personne_id"]["Nom"], "uuid"], True))
                                t(M28_uri, a, dor("M28_Individual_Performance"))
                                t(M42_uri, crm("P9_consists_of"), M28_uri)
                                t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))
                                t(M28_uri, crm("P14_carried_out_by"), she(musicien["personne_id"]["id"]))
                        else:
                            M28_uri = she(cache.get_uuid(["representations", F31_uri, "effectif", "M28", effectif["voix_et_instrument_id"]["nom"], "uuid"], True))
                            t(M28_uri, a, dor("M28_Individual_Performance"))
                            t(M42_uri, crm("P9_consists_of"), M28_uri)
                            t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))

                # Interprètes
                create_M42_M43_M28(F31_uri, "interprétation", "interpretes", "8d5b9d50-27a1-488a-82a6-19ee59acd847")

                # Danseurs
                create_M42_M43_M28(F31_uri, "danse", "danseurs", "68b77a08-d6c8-42ed-bd3d-a922ec52b064")

                # Eclairages
                create_M42_M43_M28(F31_uri, "éclairages", "eclairages", "8e27d9eb-1b30-4b14-98a8-71d48a5b3a4d")

                # Régie
                create_M42_M43_M28(F31_uri, "régie", "regie", "ed23180f-5cd4-448a-9852-4078aeebc53b")

                # Maquillage
                create_M42_M43_M28(F31_uri, "maquillage", "maquillage", "6a9dc63f-f6f0-467f-9703-864e7781b47d")

                # Bande son 
                create_M42_M43_M28(F31_uri, "bande son", "bande_son", "4b774fbe-6557-4589-9ae2-f9965e8e9bba")

                # Direction musicale
                create_M42_M43_M28(F31_uri, "direction musicale", "direction_musicale", "1d0cccc9-35a6-4847-80a5-ad48a6fefe6b")

                # Chef d'orchestre
                create_M42_M43_M28(F31_uri, "chef d'orchestre", "chef_d_orchestre", "bf07dbd8-09ef-4152-bd6e-570984ec294f")
                
                # Sonorisation
                create_M42_M43_M28(F31_uri, "sonorisation", "sonorisation", "d0bf0c77-1a79-4a66-9679-4cd8326cd226")

                # Marionnettes
                create_M42_M43_M28(F31_uri, "marionnettes", "marionnettes", "92b8d777-0495-4482-ad2d-f17c9ea682d1")

                # Images et vidéo
                create_M42_M43_M28(F31_uri, "images et vidéo", "images_et_video", "1f9b29ea-3da4-4974-99ca-e01bbf2bb9e4")

                # Direction technique
                create_M42_M43_M28(F31_uri, "direction technique", "direction_technique", "4583a259-9bfa-4275-bb17-06d0d1c28779")

                # Usage de l'électronique
                create_M42_M43_M28(F31_uri, "direction technique", "direction_technique", "4583a259-9bfa-4275-bb17-06d0d1c28779")


        # 2. Association des champs de la table "representations" à la série de représentations
        else:
            if representation["date_de_debut"] != None and representation["date_de_fin"] != None:
                E52_uri = she(cache.get_uuid(["representations", F31_serie_uri, "E52", "uuid"], True))
                t(E52_uri, a, crm("E52_Time-Span"))
                date_debut_iso = representation["date_de_debut"]["date"]
                date_fin_iso = representation["date_de_fin"]["date"]
                t(E52_uri, crm("P79_beginning_is_qualified_by"), l(f"{date_debut_iso}-01-01T00:00:00Z", datatype=XSD.dateTime))
                t(E52_uri, crm("P80_end_is_qualified_by"), l(f"{date_fin_iso}-01-01T00:00:00Z", datatype=XSD.dateTime))
                t(F31_serie_uri, crm("P4_has_time-span"), E52_uri)

                # Lieu
                t(F31_serie_uri, crm("P7_took_place_at"), she(representation["lieu"]["id"]))

                # Effectif
                M42_uri = she(cache.get_uuid(["representations", F31_serie_uri, "effectif", "uuid"], True))
                t(M42_uri, a, dor("M42_Performed_Expression_Creation"))
                t(M42_uri, crm("P2_has_type"), she("c0e9693e-3e60-4d89-b005-56dcd864180d"))
                t(F31_serie_uri, crm("P9_consists_of"), M42_uri)
                M43_uri = she(cache.get_uuid(["representations", F31_serie_uri, "effectif", "M43", "uuid"], True))
                t(M43_uri, a, dor("M43_Performed_Expression"))
                t(M42_uri, lrm("R17_created"), M43_uri)
                t(M43_uri, dor("U54_is_performed_expression_of"), she(representation["oeuvre_musicale"]["id"]))
                if len(representation["effectif"]) >= 1:
                    for effectif in representation["effectif"]:
                        # TODO tester ce if quand on aura des musiciens dans la base
                        if effectif["nombre"] != None and effectif["nombre"]>= 2:
                            nombre = effectif["nombre"]
                            for i in range(nombre):
                                M28_uri = she(cache.get_uuid(["representations", F31_serie_uri, "effectif", "M28", effectif["voix_et_instrument_id"]["nom"], i, "uuid"], True))
                                t(M28_uri, a, dor("M28_Individual_Performance"))
                                t(M42_uri, crm("P9_consists_of"), M28_uri)
                                t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))
                                if len(effectif["musiciens"]) >= 2:
                                    musicien = effectif["musiciens"][i]["personne_id"]["id"]
                                    t(M28_uri, crm("P14_carried_out_by"), she(musicien))
                        elif len(effectif["musiciens"]) >= 2:
                            for musicien in effectif["musiciens"]:
                                M28_uri = she(cache.get_uuid(["representations", F31_serie_uri, "effectif", "M28", effectif["voix_et_instrument_id"]["nom"], musicien["personne_id"]["Nom"], "uuid"], True))
                                t(M28_uri, a, dor("M28_Individual_Performance"))
                                t(M42_uri, crm("P9_consists_of"), M28_uri)
                                t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))
                                t(M28_uri, crm("P14_carried_out_by"), she(musicien["personne_id"]["id"]))
                        else:
                            M28_uri = she(cache.get_uuid(["representations", F31_serie_uri, "effectif", "M28", effectif["voix_et_instrument_id"]["nom"], "uuid"], True))
                            t(M28_uri, a, dor("M28_Individual_Performance"))
                            t(M42_uri, crm("P9_consists_of"), M28_uri)
                            t(M28_uri, dor("U1_used_medium_of_performance"), she(effectif["voix_et_instrument_id"]["id"]))

                # Interprètes
                create_M42_M43_M28(F31_serie_uri, "interprétation", "interpretes", "8d5b9d50-27a1-488a-82a6-19ee59acd847")

                # Danseurs
                create_M42_M43_M28(F31_serie_uri, "danse", "danseurs", "68b77a08-d6c8-42ed-bd3d-a922ec52b064")

                # Eclairages
                create_M42_M43_M28(F31_serie_uri, "éclairages", "eclairages", "8e27d9eb-1b30-4b14-98a8-71d48a5b3a4d")

                # Régie
                create_M42_M43_M28(F31_serie_uri, "régie", "regie", "ed23180f-5cd4-448a-9852-4078aeebc53b")

                # Maquillage
                create_M42_M43_M28(F31_serie_uri, "maquillage", "maquillage", "6a9dc63f-f6f0-467f-9703-864e7781b47d")

                # Bande son 
                create_M42_M43_M28(F31_serie_uri, "bande son", "bande_son", "4b774fbe-6557-4589-9ae2-f9965e8e9bba")

                # Direction musicale
                create_M42_M43_M28(F31_serie_uri, "direction musicale", "direction_musicale", "1d0cccc9-35a6-4847-80a5-ad48a6fefe6b")

                # Chef d'orchestre
                create_M42_M43_M28(F31_serie_uri, "chef d'orchestre", "chef_d_orchestre", "bf07dbd8-09ef-4152-bd6e-570984ec294f")
                
                # Sonorisation
                create_M42_M43_M28(F31_serie_uri, "sonorisation", "sonorisation", "d0bf0c77-1a79-4a66-9679-4cd8326cd226")

                # Marionnettes
                create_M42_M43_M28(F31_serie_uri, "marionnettes", "marionnettes", "92b8d777-0495-4482-ad2d-f17c9ea682d1")

                # Images et vidéo
                create_M42_M43_M28(F31_serie_uri, "images et vidéo", "images_et_video", "1f9b29ea-3da4-4974-99ca-e01bbf2bb9e4")

                # Direction technique
                create_M42_M43_M28(F31_serie_uri, "direction technique", "direction_technique", "4583a259-9bfa-4275-bb17-06d0d1c28779")

                # TODO Usage de l'électronique
            
    
    print(page_size, "éléments traités")
    page_size += 100
    

    if not response["representations"]:
        break

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

save_graph(args.ttl)

cache.bye()