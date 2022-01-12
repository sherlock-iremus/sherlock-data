import argparse
from openpyxl import load_workbook
import sys, os
from pprint import pprint

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
from helpers_rdf import *
from sherlockcachemanagement import Cache
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

######################################################################################
# ARGUMENTS ET CACHES
######################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("--xlsx")
parser.add_argument("--ttl")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")
args = parser.parse_args()

cache = Cache(args.cache)
cache_tei = Cache(args.cache_tei)

######################################################################################
# INITIALISATION DU GRAPHE
######################################################################################

g = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmdig_ns = Namespace("http://www.ics.forth.gr/isl/CRMdig/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
lrmoo_ns = Namespace("http://www.cidoc-crm.org/lrmoo/")
sdt_ns = Namespace("http://data-iremus.huma-num.fr/datatypes/")
sherlock_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

g.bind("crm", crm_ns)
g.bind("dcterms", DCTERMS)
g.bind("lrm", lrmoo_ns)
g.bind("sdt", sdt_ns)
g.bind("skos", SKOS)
g.bind("crmdig", crmdig_ns)
g.bind("she_ns", sherlock_ns)
g.bind("she", iremus_ns)

######################################################################################
# FONCTIONS RDF
######################################################################################

a = RDF.type

def crm(x):
    return crm_ns[x]

def crmdig(x):
    return crmdig_ns[x]

def lrm(x):
    return lrmoo_ns[x]

def she(x):
    return iremus_ns[x]

def she_ns(x):
    return sherlock_ns[x]

def t(s, p, o):
    g.add((s, p, o))


def make_E13(path, subject, predicate, object):
    make_E13.E13 = she(cache.get_uuid(path, True))
    t(make_E13.E13, a, crm("E13_Attribute_Assignement"))
    t(make_E13.E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
    t(make_E13.E13, crm("P140_assigned_attribute_to"), subject)
    t(make_E13.E13, crm("P141_assigned"), object)
    t(make_E13.E13, crm("P177_assigned_property_type"), predicate)


#######################################################################################
# RECUPERATION DES DONNEES
#######################################################################################

# Fichier Excel
sheet = load_workbook(args.xlsx).active

rows = get_xlsx_sheet_rows_as_dicts(sheet)

for row in rows[1:]:
    id = row["id"]

    #------------------------------------------------------------------------------------
    #  Air (F2)
    #------------------------------------------------------------------------------------

    F2_air = she(cache.get_uuid([id, "F2 air", "uuid"], True))
    t(F2_air, a, lrm("F2_Expression"))
    t(F2_air, crm("P2_has_type"), she("a9d51926-c0ff-4304-b49d-9a18aff02d7e")) 

    # Instanciation de l'air (pour lui associer une pagination)
    E33_instanciation_uuid = she(cache.get_uuid([id, "F2 air", "E33 instanciation" "uuid"], True))
    t(E33_instanciation_uuid, a, crm("E33_Linguistic_Object"))
    t(E33_instanciation_uuid, crm("P2_has_note"), l(row["pages"]))
    t(E33_instanciation_uuid, crm("P67_refers_to"), F2_air) 

    # Rattachement de l'instanciation de l'air à son article
    if id != None:
        id_article = id
        id_livraison = id[0:-4]
        if id_livraison.endswith("_"):
            id_livraison = id_livraison[0:-1]
        try:
            # article original
            article_F2_original = she(cache_tei.get_uuid(
                ["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
            t(article_F2_original, crm("P148_has_component"), F2_air)
			# article TEI
            article_F2_TEI = she(cache_tei.get_uuid(
				["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
            t(article_F2_TEI, crm("P148_has_component"), F2_air)
        except:
            pass
            #print("L'air " + id + " n'est relié à aucun article")

    # Création de l'air
    F2_air_creation = she(cache.get_uuid([id, "F2 air", "F28 Creation" "uuid"], True))
    t(F2_air_creation, a, lrm("F28_Expression_Creation"))
    t(F2_air_creation, lrm("R17_created"), F2_air)
    # auteur de l'air
    if row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"] != None:
        auteurs_musique = row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"].split(";")

        for auteur in auteurs_musique:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                E21_auteur_musique = auteur.split("[")[0].replace(" ", "")
            else:
                E21_auteur_musique = auteur.replace(" ", "")

        make_E13([id, "F2 air", "F28 Creation" "E13"], F2_air_creation, crm("P14_carried_out_by"), she(E21_auteur_musique))

     # !! #   # TODO CREER DES E55 POUR LES TYPES D'ATTRIBUTIONS?
    # !!#    t(make_E13.E13, crm("P2_has_type"), l(type_attribution))

    # Incipit musical
    if row["code incipit musical. Anne: OK"] != None:
        F2_air_incipit_musical = she(cache.get_uuid([id, "F2 air", "E42 incipit musical", "uuid"], True))
        t(F2_air_incipit_musical, a, crm("E42_Identifier"))
        t(F2_air, crm("P1_is_identified_by"), F2_air_incipit_musical)
        t(F2_air_incipit_musical, crm("P2_has_type"), she("f6ca9e82-e5fa-442d-a9e5-79fca664566e"))

        make_E13([id, "F2 air", "E42 incipit musical", "E13"], F2_air_incipit_musical, RDFS.label, l(row["code incipit musical. Anne: OK"]))    

        # note musicale
        make_E13([id, "F2 air", "note musicale", "E13"], F2_air, crm("P3_has_note"), l(row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"]))    

        # genre musical
        #Créer un E32 et ses E55 avec P177 "genre musical"
        make_E13([id, "F2 air", "genre musical", "E13"], F2_air, crm("P3_has_note"), l(row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"]))    

        # Même chose pour formation musicale

    # Le texte de l'air (F2)
    if row["Incipit principal ou premier"] != None or row["incipit français"] != None:
        F2_texte = she(cache.get_uuid([id, "F2 texte", "uuid"], True))
        t(F2_texte, a, lrm("F2_Expression"))
        t(F2_texte, crm("P2_has_type"), she("fb1ac98a-1645-460f-9f26-23f36e216f7e"))

        make_E13([id, "F2 air", "F2 texte", "E13"], F2_air, lrm("R75_incorporates"), F2_texte)

        # incipit textuel principal
        if row["Incipit principal ou premier"] != None:
            F2_texte_incipit_principal = she(cache.get_uuid([id, "F2 texte", "E41 incipit textuel", "principal", "uuid"], True))
            t(F2_texte_incipit_principal, a, crm("E41_Appellation"))
            t(F2_texte_incipit_principal, a, crm("E33_Linguistic_Object"))
            t(F2_texte, crm("P1_is_identified_by"), F2_texte_incipit_principal)
            t(F2_texte_incipit_principal, crm("P2_has_type"), she("5891daa1-81be-494a-8bf9-9055574f0530"))

            make_E13([id, "F2 texte", "E41 incipit textuel", "principal", "E13"], F2_texte_incipit_principal, crm("P190_has_symbolic_content"), l(row["Incipit principal ou premier"]))    
            

        # incipit textuel français    
        if row["incipit français"] != None:
            F2_texte_incipit_francais = she(cache.get_uuid([id, "F2 texte", "E41 incipit textuel", "français", "uuid"], True))
            t(F2_texte_incipit_francais, a, crm("E41_Appellation"))
            t(F2_texte_incipit_francais, a, crm("E33_Linguistic_Object"))
            t(F2_texte, crm("P1_is_identified_by"), F2_texte_incipit_francais)
            t(F2_texte_incipit_francais, crm("P2_has_type"), she("a7453d39-b7f0-4ca2-ba62-9fc560438c60"))

            make_E13([id, "F2 texte", "E41 incipit textuel", "français", "E13"], F2_texte_incipit_francais, crm("P190_has_symbolic_content"), l(row["incipit français"]))    


#######################################################################################
# CREATION DU GRAPHE ET DU CACHE
#######################################################################################

cache.bye()

print("Ecriture du fichier ttl")

serialization = g.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "w+") as f:
    f.write(serialization)
