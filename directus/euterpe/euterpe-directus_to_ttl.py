from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import requests
import os
import sys
import yaml
import json
from sherlockcachemanagement import Cache
import argparse

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
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

############################################################################################
## INITIALISATION DU GRAPHE ET NAMESPACES
############################################################################################

output_graph = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
sdt_ns = Namespace("http://data-iremus.huma-num.fr/datatypes/")
sherlock_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

output_graph.bind("crm", crm_ns)
output_graph.bind("dcterms", DCTERMS)
output_graph.bind("skos", SKOS)
output_graph.bind("sdt", sdt_ns)
output_graph.bind("she_ns", sherlock_ns)

a = RDF.type

def crm(x):
	return URIRef(crm_ns[x])

def she(x):
	return URIRef(iremus_ns[x])

def she_ns(x):
	return URIRef(sherlock_ns[x])

def t(s, p, o):
	output_graph.add((s, p, o))


############################################################################################
## RECUPERATION DES DONNEES DANS DIRECTUS
############################################################################################

# Taxonomies
query = """
query {
  oeuvres(limit: 100) {
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
      ecole_id{
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
        coordonnees_geographiques
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
"""

r = requests.post(secret["url"] + '/graphql' + '?access_token=' + access_token, json={'query': query})
print(r.status_code)
result = json.loads(r.text)

############################################################################################
## CREATION DES TRIPLETS
############################################################################################

for oeuvre in result["data"]["oeuvres"]:

	# L'oeuvre
	oeuvre_uuid = oeuvre["id"]
	t(she(oeuvre_uuid), a, crm("E22_Human-Made_Object"))

	# Titre
	E35_uuid = cache.get_uuid(["oeuvres", oeuvre_uuid, "Titre principal"], True)
	t(she(oeuvre_uuid), crm("P102_has_title"), she(E35_uuid))
	t(she(E35_uuid), RDFS.label, Literal(oeuvre["titre"]))
	# Typer le E35 principal/secondaire

	# Titre alternatif (E13)
	E35_alt_uuid = cache.get_uuid(["oeuvres", oeuvre_uuid, "Titre alternatif"], True)
	t(she(oeuvre_uuid), crm("P102_has_title"), she(E35_alt_uuid))
	t(she(E35_alt_uuid), RDFS.label, Literal(oeuvre["titre_alternatif"]))

	# Cote
	crm: P1_is_identified_by
	crm: E42_Identifier / rdfs:label
	"P 95-825";  # typer le E42

# 	# référence iremus
# 	crm: P1_is_identified_by
# 	crm: E42_Identifier / rdfs:label
# 	"P 95-8";  # typer le E42 (E55 "référence iremus" dans data)
# 	# n° inventaire
# 	crm: P1_is_identified_by
# 	crm: E42_Identifier / rdfs:label
# 	"Département des estampes et de
# 	la
# 	photographie, Ed
# 	20
# 	" ; #typer le E42
# 	# bibliographie (E13)
# 	crm: P70i_is_documented_in < 6701782
# 	f - e5a8 - 4e60 - a541 - 2
# 	a2db08a8d07 >;
# 	# domaine (E13)
# 	# P177/E55 "domaine"  P141/E55/rdfs:label "Estampe" ;
# 	# Contenu sémiotique de l'oeuvre
# 	crm: P65_shows_visual_item < cea7eded - 75
# 	d0 - 4724 - b13e - 7
# 	d1c233754c9 >;
# 	# lieu de conservation
# 	crm: P49_has_former_or_current_keeper
# 	crm: E39_Actor / rdfs:label
# 	"";
# 	# précision oeuvre (E13)
# 	crm: P3_has_note
# 	"frontispice du premier livre des 'Pièces pour clavessin' de Jacques
# 	Champion
# 	de
# 	Chambonnières
# 	" ;
# 	# commmentaire (E13)
# 	crm: P3_has_note
# 	"Jacques Champion de Chambonnières : vers 1601, 1670.
# 	L
# 	'estampe est anonyme mais il existe un tirage signé Lepautre de cette estampe à la BnF" ;
# 	# référence agence : E42 de type E55 "référence agence"
# 	# url/titre url
# 	crm: P1_is_identified_by
# 	crm: E42_Identifier / rdfs:label
# 	"gallica: http...";  # Ajouter titre URL (P102)
# 	# hauteur/largeur/diamètre
# 	crm: P43_has_dimension < 8
# 	a494870 - 0
# 	ca3 - 4
# 	a11 - aa8b - e04fb74ebf65 >;
# .


# TODO Ne pas oublier les images + oeuvres représentées

############################################################################################
## SERIALISATION DU GRAPHE
############################################################################################

serialization = output_graph.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "wb") as f:
	f.write(serialization)

cache.bye()