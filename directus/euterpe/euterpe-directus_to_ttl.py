from rdflib import Graph, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef as u, Literal as l
import requests
import os
import sys
import yaml
import json
from sherlockcachemanagement import Cache
import argparse
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# Cache
cache = Cache(args.cache)

# Helpers
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
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

def create_sub_production(sub_prod, type):
  if oeuvre[sub_prod] != None:
    sub_prod_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E12", sub_prod, "uuid"], True))
    t(sub_prod_uri, a, crm("E12_Production"))
    t(sub_prod_uri, crm("P2_has_type"), she(type))
    t(E12_uri, crm("P9_consists_of"), sub_prod_uri)
  
  for person in oeuvre[sub_prod]:
    person_uri = she(person["auteur_oeuvre_id"]["id"])
    make_E13(["oeuvres", oeuvre_uuid, "E12", sub_prod, "E13"], sub_prod_uri, crm("P14_carried_out_by"), person_uri)


############################################################################################
## RECUPERATION DES DONNEES DANS DIRECTUS
############################################################################################

# Taxonomies
query = gql("""
query ($page_size: Int) {
	oeuvres(limit: 100, offset: $page_size) {
    id
    titre
    titre_alternatif
    reference_iremus
    num_inventaire
    cote
    inscription
    technique
    oeuvre_en_rapport
    precision_oeuvre
    precision_instrument
    commentaire
    bibliographie
    reference_agence
    url
    diametre
    precision_musique
    source_litteraire
    date
    date_iso
    hauteur
    largeur
    chants {
      chant_id {
        id
      }
    }
    ateliers {
      auteur_oeuvre_id{
        id
      }
    }
    artistes {
      auteur_oeuvre_id{
        id
      }
    }
    notations_musicales {
      notation_musicale_id {
        id
      }
    }
    ecoles {
      auteur_oeuvre_id{
        id
      }
    }
    graveurs {
      auteur_oeuvre_id{
        id
      }
    }
    lieux_de_conservation {
      lieu_de_conservation_id {
        id
        nom
      }
    }
    domaines {
      domaine_id {
        id
      }
    }
    inventeurs {
      auteur_oeuvre_id{
        id
      }
    }
    dapres {
      auteur_oeuvre_id{
        id
      }
    }
    a_la_maniere_de {
      auteur_oeuvre_id{
        id
      }
    }
    editeurs {
      auteur_oeuvre_id{
        id
      }
    }
    anciennes_attributions {
      auteur_oeuvre_id{
        id
      }
    }
    copie_dapres {
      auteur_oeuvre_id{
        id
      }
    }
    instruments_de_musique {
      instrument_de_musique_id {
        id
      }
    }
    themes {
      theme_id {
        id
      }
    }
    attributions{
      auteur_oeuvre_id{
        id
      }
    }
    voir_aussi {
      voir_aussi_id {
        id
      }
    }
  } 
}
""")

page_size = 0

while True:

  response = client.execute(query, variable_values= {"page_size": page_size})

  ############################################################################################
  ## CREATION DES TRIPLETS
  ############################################################################################

  for oeuvre in response["oeuvres"]:

    # L'oeuvre
    oeuvre_uuid = oeuvre["id"]
    t(she(oeuvre_uuid), a, crm("E22_Human-Made_Object"))

    # Unité de mesure, utilisée pour les dimensions des oeuvres
    E58_uri = she(cache.get_uuid(["oeuvres", "E58", "uuid"], True))
    t(E58_uri, a, crm("E58_Measurement_Unit"))
    t(E58_uri, RDFS.label, l("cm"))

    # Titre
    if oeuvre["titre"] != None:
      E35_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "titre principal", "uuid"], True))
      t(E35_uri, a, crm("E35_Title"))
      t(E35_uri, RDFS.label, l(oeuvre["titre"]))
      t(E35_uri, crm("P2_has_type"), she("1126a1f7-2b7d-45ab-b02c-a25b225e2977"))

      make_E13(["oeuvres", oeuvre_uuid, "titre principal", "E13"], she(oeuvre_uuid), crm("P102_has_title"), E35_uri)

    # Titre alternatif (E13)
    if oeuvre["titre_alternatif"] != None:
      E35_alt_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "titre alternatif", "uuid"], True))
      t(E35_alt_uri, a, crm("E35_Title"))
      t(E35_alt_uri, RDFS.label, l(oeuvre["titre_alternatif"]))
      t(E35_alt_uri, crm("P2_has_type"), she("dad7fbf8-c629-437e-96ef-594a674e5e37"))

      make_E13(["oeuvres", oeuvre_uuid, "titre alternatif", "E13"], she(oeuvre_uuid), crm("P102_has_title"), E35_alt_uri)

    # Cote
    if oeuvre["cote"] != None:
      E42_cote_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "identifiant cote"], True))
      t(E42_cote_uri, a, crm("E42_Identifier"))
      t(she(oeuvre_uuid), crm("P1_is_identified_by"), E42_cote_uri)
      t(E42_cote_uri, RDFS.label, l(oeuvre["cote"]))
      t(E42_cote_uri, crm("P2_has_type"), she("d74076d1-a145-449a-8403-88841ba29dfb"))

    # Référence iremus
    if oeuvre["reference_iremus"] != None:
      E42_iremus_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "référence IReMus"], True))
      t(E42_iremus_uri, a, crm("E42_Identifier"))
      t(she(oeuvre_uuid), crm("P1_is_identified_by"), E42_iremus_uri)
      t(E42_iremus_uri, RDFS.label, l(oeuvre["reference_iremus"]))
      t(E42_iremus_uri, crm("P2_has_type"), she("cbce1a5e-4b6d-4d58-9fe0-4e5f41ae4d19"))

    # N° inventaire
    if oeuvre["num_inventaire"] != None:
      E42_inventaire_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "n° inventaire"], True))
      t(E42_inventaire_uri, a, crm("E42_Identifier"))
      t(she(oeuvre_uuid), crm("P1_is_identified_by"), E42_inventaire_uri)
      t(E42_inventaire_uri, RDFS.label, l(oeuvre["num_inventaire"]))
      t(E42_inventaire_uri, crm("P2_has_type"), she("8cefd485-0d51-4b95-a135-0feaf4896d11"))

    # Bibliographie
    if oeuvre["bibliographie"] != None:
      E31_biblio_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "bibliographie", "uuid"], True))
      t(E31_biblio_uri, a, crm("E31_Document"))
      t(E31_biblio_uri, RDFS.label, l(oeuvre["bibliographie"]))

      make_E13(["oeuvres", oeuvre_uuid, "bibliographie", "E13"], E31_biblio_uri, crm("P70_documents"), she(oeuvre_uuid))

    # Domaine
    if oeuvre["domaines"] != None:
      for domaine in oeuvre["domaines"]:
        domaine_uri = she(domaine["domaine_id"]["id"])

        make_E13(["oeuvres", oeuvre_uuid, "domaine", "E13"], she(oeuvre_uuid), she("894b8a02-1f03-48ad-b22a-875aead9b326"), domaine_uri)

    # Lieu de conservation
    if oeuvre["lieux_de_conservation"] != None:
      for lieu in oeuvre["lieux_de_conservation"]:
        E39_uri = she(lieu["lieu_de_conservation_id"]["id"])
        t(E39_uri, a, crm("E39_Actor"))

        make_E13(["oeuvres", oeuvre_uuid, "lieu de conservation", E39_uri, "E13"], she(oeuvre_uuid), crm("P49_has_former_or_current_keeper"), E39_uri)
    
    # Précision oeuvre
    if oeuvre["precision_oeuvre"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "précision", "E13"], she(oeuvre_uuid), she("bb919bee-7a73-4ade-a42c-996062df8ac2"), l(oeuvre["precision_oeuvre"]))

    # Commentaire
    if oeuvre["commentaire"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "commentaire", "E13"], she(oeuvre_uuid), she("48b6de1f-259b-41b9-af48-a1a05094ab9f"), l(oeuvre["commentaire"]))

    # Référence agence : E42 de type E55 "référence agence"
    if oeuvre["reference_agence"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "référence agence", "E13"], she(oeuvre_uuid), she("1483a1a9-7193-4cb2-853f-ab6193155673"), l(oeuvre["reference_agence"]))   

    # URL/titre URL
    if oeuvre["url"] != None:
      E42_URL_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "url", "E42"], True))
      t(E42_URL_uri, a, crm("E42_Identifier"))
      # Ajouter titre URL (P102)

      make_E13(["oeuvres", oeuvre_uuid, "url", "E13"], she(oeuvre_uuid), crm("P1_is_identified_by"), E42_URL_uri)   

    # Dimensions
    if oeuvre["hauteur"] != None:
      E54_H_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E54 hauteur", "uuid"], True))
      t(E54_H_uri, crm("P2_has_type"), u("http://vocab.getty.edu/page/aat/300055644"))
      t(E54_H_uri, crm("P90_has_value"), l(oeuvre["hauteur"]))
      
      make_E13(["oeuvres", oeuvre_uuid, "E54 hauteur", "E13"], she(oeuvre_uuid), crm("P43_has_dimension"), E54_H_uri)

    if oeuvre["largeur"] != None:
      E54_L_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E54 largeur", "uuid"], True))
      t(E54_L_uri, crm("P2_has_type"), u("http://vocab.getty.edu/page/aat/300055647"))
      t(E54_L_uri, crm("P90_has_value"), l(oeuvre["largeur"]))
      
      make_E13(["oeuvres", oeuvre_uuid, "E54 largeur", "E13"], she(oeuvre_uuid), crm("P43_has_dimension"), E54_L_uri)
      
    if oeuvre["diametre"] != None:
      E54_D_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E54 diamètre", "uuid"], True))
      t(E54_D_uri, crm("P2_has_type"), u("http://vocab.getty.edu/page/aat/300055624"))
      t(E54_D_uri, crm("P90_has_value"), l(oeuvre["diametre"]))

      make_E13(["oeuvres", oeuvre_uuid, "E54 dimètre", "E13"], she(oeuvre_uuid), crm("P43_has_dimension"), E54_D_uri)

    # Production de l'oeuvre
    E12_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E12", "uuid"], True))
    t(E12_uri, a, crm("E12_Production"))
    t(E12_uri, crm("P108_has_produced"), she(oeuvre_uuid))

    # Technique
    if oeuvre["technique"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "E12", "technique", "E13"], E12_uri, crm("P32_used_general_technique"), l(oeuvre["technique"]))

    # éditeur (E13)
    create_sub_production("editeurs", "31c6d6b8-09ca-46fd-994a-ca8aa8d9583b")

    # inventeur (E13)
    create_sub_production("inventeurs", "4f324bd5-5982-4d99-949a-a9063e328599")

    # graveur (E13)
    create_sub_production("graveurs", "7727e6e7-8c66-46c7-8bfe-7b2de70063c8")
    
    # artiste (E13)
    create_sub_production("artistes", "b7f72f03-ae41-4605-bd1c-ba636b5165a2")
    
    # attribution (E13)
    create_sub_production("attributions", "ea8dbeda-c5ba-42ff-a2eb-2fa87f6e8581")
    
    # ancienne attribution (E13)
    create_sub_production("anciennes_attributions", "a4d8ae34-ffb2-4562-9a92-2d8536004745")
    
    # atelier (E13)
    if oeuvre["ateliers"] != None:  
      for atelier in oeuvre["ateliers"]:
        atelier_uri = she(atelier["auteur_oeuvre_id"]["id"])
        t(atelier_uri, a, crm("E39_Actor"))
        make_E13(["oeuvres", oeuvre_uuid, "E12", "atelier", atelier_uri, "E13"], E12_uri, crm("P14_carried_out_by"), atelier_uri)
   
    # date de l'oeuvre
    if oeuvre["date_iso"] != None:
      date = oeuvre["date_iso"]
      E52_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E52", "uuid"], True))
      t(E52_uri, a, crm("E52_Time-Span"))
      t(she(oeuvre_uuid), crm("P4_has_time-span"), E52_uri)
      t(E52_uri, crm("begin_of_the_begin"), l(f"{date}-01-01T00:00:00Z"))
      t(E52_uri, crm("end_of_the_end"), l(f"{date}-01-01T00:00:00Z"))
      t(E52_uri, crm("P3_has_note"), l(oeuvre["date"]))
      
    # contenu sémiotique de l'oeuvre
    E36_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E36", "uuid"], True))
    t(E36_uri, a, crm("E36_Visual_Item"))
    make_E13(["oeuvres", oeuvre_uuid, "E36", "E13"], she(oeuvre_uuid), crm("P65_shows_visual_item"), E36_uri)

    # images
    D1_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "D1", "uuid"], True))
    t(D1_uri, a, crmdig("D1_Digital_Object"))
    t(E36_uri, u("https://linked.art/digitally_shown_by"), D1_uri)
    t(D1_uri, u("https://linked.art/access_point"), u(f"https://ceres.huma-num.fr/iiif/3/euterpe--{oeuvre_uuid}/full/max/0/default.jpg"))

    # instruments de musique (E13)
    if oeuvre["instruments_de_musique"] != None:
      for instrument in oeuvre["instruments_de_musique"]:
        instrument_uri = she(instrument["instrument_de_musique_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "instruments", instrument_uri, "E13"], E36_uri, crm("P138_represents"), instrument_uri)
        
    if oeuvre["precision_instrument"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "précision instruments", "E13"], E36_uri, she("84b986a0-a1d9-46be-b1c3-447f4b9c4f10"), l(oeuvre["precision_instrument"]))

    # notations musicales (E13)
    if oeuvre["notations_musicales"] != None:
      for notation in oeuvre["notations_musicales"]:
        notation_uri = she(notation["notation_musicale_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "notations musicales", notation_uri, "E13"], E36_uri, crm("P138_represents"), notation_uri)

    # précision musique (E13)
    if oeuvre["precision_musique"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "précision musique", "E13"], E36_uri, she(""), l(oeuvre["precision_musique"]))

    # Créer un E55 "oeuvre en rapport" (E13)
    # thème (E13)
    # On créera le type "thématique" #<uuid du thème> ; information de la colonne très variée (mélange de pré-iconographie/iconographie)
    # oeuvre représentée (E13)
    crm:P138_represents #<uuid de l'oeuvre> ;
    # voir aussi (E13)
    rdfs:seeAlso "" ;
    # école (E13)
     # Créer un E55 "école"
    # TODO copie d'après : P130 ?
    # contient/contenu dans (E13) à revoir
    # genre - colonne vide
    # inscription (E13) : créer un E55 "inscription" 
    # chant (E13)
    crm:P138_represents #E55 type de la taxonomie

  # TODO Ne pas oublier oeuvres représentées

  # TODO  d'après (E13)
    #crm:P15_was_influenced_by #<uuid de l'artiste> ;
    # à la manière de (E13) - Créer un E55, Questionner Fabien sur le sens de cette colonne ;
    # source littéraire (E13) - Créer un E55 "Source littéraire" ;
  


  print(page_size, "oeuvres traitées")
  page_size += 100

  if not response["oeuvres"]:
      break

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

save_graph(args.ttl)

cache.bye()