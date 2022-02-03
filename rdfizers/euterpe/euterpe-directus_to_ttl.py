from rdflib import Graph, Namespace, DCTERMS, RDF, RDFS, SKOS, XSD, URIRef as u, Literal as l
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
## OEUVRES
############################################################################################

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
    contient_ou_contenue_dans {
      oeuvre_contient_contenue_id {
        id
      }
    }
    oeuvres_representees {
      item {
				... on oeuvres_lyriques {
					id
				}
        ... on directus_files {
					id
				}
      }
    }
  } 
}
""")

print("\nCOLLECTION - OEUVRES")

page_size = 0

while True:

  response = client.execute(query, variable_values= {"page_size": page_size})

  #---------------------------------------------------------------------------------------------
  ## CREATION DES TRIPLETS
  #---------------------------------------------------------------------------------------------

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
      t(she(oeuvre_uuid), crm("P102_has_title"), E35_uri)

    # Titre alternatif (E13)
    if oeuvre["titre_alternatif"] != None:
      E35_alt_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "titre alternatif", "uuid"], True))
      t(E35_alt_uri, a, crm("E35_Title"))
      t(E35_alt_uri, RDFS.label, l(oeuvre["titre_alternatif"]))
      t(E35_alt_uri, crm("P2_has_type"), she("dad7fbf8-c629-437e-96ef-594a674e5e37"))
      t(she(oeuvre_uuid), crm("P102_has_title"), E35_alt_uri)

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
      t(she(oeuvre_uuid), crm("P43_has_dimension"), E54_H_uri)

    if oeuvre["largeur"] != None:
      E54_L_uri = she(cache.get_uuid(["oeuvres", oeuvre_uuid, "E54 largeur", "uuid"], True))
      t(E54_L_uri, crm("P2_has_type"), u("http://vocab.getty.edu/page/aat/300055647"))
      t(E54_L_uri, crm("P90_has_value"), l(oeuvre["largeur"]))
      t(she(oeuvre_uuid), crm("P43_has_dimension"), E54_L_uri)
      
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
      t(E52_uri, crm("P79_beginning_is_qualified_by"), l(f"{date}-01-01T00:00:00Z", datatype=XSD.dateTime))
      t(E52_uri, crm("P80_end_is_qualified_by"), l(f"{date}-01-01T00:00:00Z", datatype=XSD.dateTime))
      t(E52_uri, crm("P82_at_some_time_within"), l(oeuvre["date"], datatype=XSD.string))
      
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
      make_E13(["oeuvres", oeuvre_uuid, "précision musique", "E13"], E36_uri, she("70c9af37-5b2e-4731-89f6-e3f317da2bf0"), l(oeuvre["precision_musique"]))    

    # thèmes (E13)
    if oeuvre["themes"] != None:
      for theme in oeuvre["themes"]:
        theme_uri = she(theme["theme_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "themes", theme_uri, "E13"], E36_uri, she("a146f796-e82f-4319-8741-c8eb400918a9"), theme_uri)
    
    # école (E13)
    if oeuvre["ecoles"] != None:
      for ecole in oeuvre["ecoles"]:
        ecole_uri = she(ecole["auteur_oeuvre_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "écoles", ecole_uri, "E13"], E36_uri, she("20eb5622-0c9b-4bfd-b1f4-67664d7f47e2"), ecole_uri)
    
    # inscription (E13) : créer un E55 "inscription" 
    if oeuvre["inscription"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "inscription", "E13"], E36_uri, she("916a8978-391e-4b02-b237-6aa7a9b44bb0"), l(oeuvre["inscription"]))    

    # chant (E13)
    if oeuvre["chants"] != None:
      for chant in oeuvre["chants"]:
        chant_uri = she(chant["chant_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "chants", chant_uri, "E13"], E36_uri, crm("P138_represents"), chant_uri)

    # copie d'après (E13)
    if oeuvre["copie_dapres"] != None:
      for copie in oeuvre["copie_dapres"]:
        copie_uri = she(copie["auteur_oeuvre_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "copie d'après", copie_uri, "E13"], E36_uri, she(""), copie_uri)

    # oeuvres en rapport (E13)
    if oeuvre["oeuvre_en_rapport"] != None:
      make_E13(["oeuvres", oeuvre_uuid, "oeuvre en rapport", "E13"], E36_uri, she("1cabd329-38a9-4712-adc7-04fadfa5ba05"), l(oeuvre["oeuvre_en_rapport"]))

    # contient/contenu dans (E13)
    if oeuvre["contient_ou_contenue_dans"] != None:
      for oeuvre_cont in oeuvre["contient_ou_contenue_dans"]:
        oeuvre_cont_uri = she(oeuvre_cont["oeuvre_contient_contenue_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "contient ou contenue dans", oeuvre_cont_uri, "E13"], E36_uri, she("cae60963-9c65-4e29-bd6e-6b52c628ce41"), oeuvre_cont_uri)

    # oeuvre représentée (E13)
    if oeuvre["oeuvres_representees"] != None:
      for oeuvre_rep in oeuvre["oeuvres_representees"]:
        oeuvre_rep_uri = she(oeuvre_rep["item"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "oeuvre représentée", oeuvre_rep_uri, "E13"], E36_uri, crm("P138_represents"), oeuvre_rep_uri)

    # voir aussi (E13)
    if oeuvre["voir_aussi"] != None:
      for va in oeuvre["voir_aussi"]:
        va_uri = she(va["voir_aussi_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "voir aussi", va_uri, "E13"], E36_uri, RDFS.seeAlso, va_uri)
    
    # d'après (E13)
    if oeuvre["dapres"] != None:
      for dapres in oeuvre["dapres"]:
        dapres_uri = she(dapres["auteur_oeuvre_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "d'après", dapres_uri, "E13"], E36_uri, crm("P15_was_influenced_by"), dapres_uri)

    # à la manière de (E13) 
    if oeuvre["a_la_maniere_de"] != None:
      for maniere in oeuvre["a_la_maniere_de"]:
        maniere_uri = she(maniere["auteur_oeuvre_id"]["id"])
        make_E13(["oeuvres", oeuvre_uuid, "à la manière de", maniere_uri, "E13"], E36_uri, she("5cfae3b1-1493-492f-a687-80825d8f5f68"), dapres_uri)
    
    # source littéraire (E13) 
      if oeuvre["source_litteraire"] != None:
        make_E13(["oeuvres", oeuvre_uuid, "source littéraire", "E13"], E36_uri, she("5d86a902-8f9f-432e-9d80-3d095d6563af"), l(oeuvre["source_litteraire"]))

  print(page_size, "oeuvres traitées")
  page_size += 100

  if not response["oeuvres"]:
      break


############################################################################################
## AUTEURS OEUVRES
############################################################################################

query = gql("""
  query ($page_size: Int) {
    auteurs_oeuvres(limit: 100, offset: $page_size) {
      id
      nom
      alias
      lieu_de_deces
      date_de_deces
      lieu_de_naissance
      date_de_naissance
      commentaire
      lieu_dactivite
      date_dactivite
      periodes {
        periode_id {
          id
        }
      }
      ecoles {
        ecole_id {
          id
        }
      }
      specialites {
        specialite_id {
          id
        }
      }
    }
  }
""")

print("\nCOLLECTION - AUTEURS OEUVRES")

page_size = 0

while True:

  response = client.execute(query, variable_values= {"page_size": page_size})

  #---------------------------------------------------------------------------------------------
  ## CREATION DES TRIPLETS
  #---------------------------------------------------------------------------------------------

  for auteur in response["auteurs_oeuvres"]:
    
    auteur_uuid = auteur["id"]
    auteur_uri = she(auteur_uuid)
    t(auteur_uri, a, crm("E21_Person"))
    
    if auteur["nom"] != None:
      E41_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E41", "uuid"], True))
      t(E41_uri, a, crm("E41_Appellation"))
      t(E41_uri, RDFS.label, l(auteur["nom"]))
      t(E41_uri, crm("P2_has_type"), SKOS.prefLabel)
      t(auteur_uri, crm("P1_is_identified_by"), E41_uri)
      
    if auteur["alias"] != None:      
      alias_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "alias", "uuid"], True))
      t(alias_uri, a, crm("E41_Appellation"))
      t(alias_uri, RDFS.label, l(auteur["nom"]))
      t(E41_uri, crm("P2_has_type"), SKOS.altLabel)
      t(auteur_uri, crm("P1_is_identified_by"), alias_uri)
      
    if auteur["commentaire"] != None:
      make_E13(["auteurs oeuvres", auteur_uuid, "commentaire", "E13"], auteur_uri, crm("P3_has_note"), l(auteur["commentaire"]))

    if auteur["ecoles"] != None:
      for ecole in auteur["ecoles"]:
        ecole_uri = she(ecole["ecole_id"]["id"])
        make_E13(["auteurs oeuvres", auteur_uuid, "écoles", ecole_uri, "E13"], auteur_uri, she("93d99e9b-b857-4fc0-8fa0-b82a76735038"), ecole_uri)

    if auteur["periodes"] != None:
      for periode in auteur["periodes"]:
        periode_uri = she(periode["periode_id"]["id"])
        make_E13(["auteurs oeuvres", auteur_uuid, "périodes", periode_uri, "E13"], auteur_uri, she("6555e041-d417-4df2-b8b5-ac25dca95fd4"), periode_uri)

    if auteur["specialites"] != None:
      for specialite in auteur["specialites"]:
        specialite_uri = she(specialite["specialite_id"]["id"])
        make_E13(["auteurs oeuvres", auteur_uuid, "specialités", specialite_uri, "E13"], auteur_uri, she("aaad25f5-1da4-4980-8e3e-ff0618f76e53"), specialite_uri)

    
    if auteur["date_de_naissance"] != None:
      E67_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E67", "uuid"], True))
      t(E67_uri, a, crm("E67_Birth"))
      t(E67_uri, crm("P98_brought_into_life"), auteur_uri)
      E52_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E67", "E52", "uuid"], True))
      t(E67_uri, crm("P4_has_time-span"), E52_uri)
      t(E52_uri, a, crm("E52_Time-Span"))
      make_E13(["auteurs oeuvres", auteur_uuid, "E67", "E52", "E13"], E52_uri, crm("P82_at_some_time_within"), l(auteur["date_de_naissance"]))

      if auteur["lieu_de_naissance"] != None:
        t(E67_uri, crm("P7_took_place_at"), l(auteur["lieu_de_naissance"]))

    if auteur["date_de_deces"] != None:
      E69_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E69", "uuid"], True))
      t(E69_uri, a, crm("E69_Death"))
      t(E69_uri, crm("P100_was_death_of"), auteur_uri)
      E52_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E69", "E52", "uuid"], True))
      t(E69_uri, crm("P4_has_time-span"), E52_uri)
      t(E52_uri, a, crm("E52_Time-Span"))
      make_E13(["auteurs oeuvres", auteur_uuid, "E69", "E52", "E13"], E52_uri, crm("P82_at_some_time_within"), l(auteur["date_de_deces"]))

      if auteur["lieu_de_deces"] != None:
        t(E69_uri, crm("P7_took_place_at"), l(auteur["lieu_de_deces"]))

    if auteur["date_dactivite"] != None:
      E7_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E7", "uuid"], True))
      t(E7_uri, a, crm("E7_Activity"))
      t(E7_uri, crm("P14_carried_out_by"), auteur_uri)
      E52_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E7", "E52", "uuid"], True))
      t(E7_uri, crm("P4_has_time-span"), E52_uri)
      t(E52_uri, crm("P82_at_some_time_within"), l(auteur["date_dactivite"]))
      if auteur["lieu_dactivite"] != None:
        t(E7_uri, crm("P7_took_place_at"), l(auteur["lieu_dactivite"]))        
    elif auteur["lieu_dactivite"] != None:
      E7_uri = she(cache.get_uuid(["auteurs oeuvres", auteur_uuid, "E7", "uuid"], True))
      t(E7_uri, a, crm("E7_Activity"))
      t(E7_uri, crm("P14_carried_out_by"), auteur_uri)
      t(E7_uri, crm("P7_took_place_at"), l(auteur["lieu_dactivite"]))

  print(page_size, "auteurs traités")
  page_size += 100

  if not response["auteurs_oeuvres"]:
      break


############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

save_graph(args.ttl)

cache.bye()