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
parser.add_argument("--cache_vocabulaires")
parser.add_argument("--cache_tei")
args = parser.parse_args()

cache = Cache(args.cache)
cache_vocabulaires = Cache(args.cache_vocabulaires)
cache_tei = Cache(args.cache_tei)

######################################################################################
# INITIALISATION DU GRAPHE
######################################################################################

graph = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmdig_ns = Namespace("http://www.ics.forth.gr/isl/CRMdig/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
lrmoo_ns = Namespace("http://www.cidoc-crm.org/lrmoo/")
sdt_ns = Namespace("http://data-iremus.huma-num.fr/datatypes/")
sherlock_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

graph.bind("crm", crm_ns)
graph.bind("dcterms", DCTERMS)
graph.bind("lrm", lrmoo_ns)
graph.bind("sdt", sdt_ns)
graph.bind("skos", SKOS)
graph.bind("crmdig", crmdig_ns)
graph.bind("she_ns", sherlock_ns)
graph.bind("she", iremus_ns)

######################################################################################
# FONCTIONS
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
    graph.add((s, p, o))


def make_E13(path, subject, predicate, object):
    make_E13.E13 = she(cache.get_uuid(path, True))
    t(make_E13.E13, a, crm("E13_Attribute_Assignement"))
    t(make_E13.E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
    t(make_E13.E13, crm("P140_assigned_attribute_to"), subject)
    t(make_E13.E13, crm("P141_assigned"), object)
    t(make_E13.E13, crm("P177_assigned_property_type"), predicate)

# Récupération des UUID des vocabulaires
def add_vocabulary(column):
    E32_uuid = cache_vocabulaires.get_uuid([column, "uuid"], True)
    
    t(she(E32_uuid), a, crm("E32_Authority_Document"))
    t(she(E32_uuid), crm("P1_is_identified_by"), l(column))

    for row in rows[1:]:
        concept = row[column]
        if concept != None:
            if ";" in concept:
                concepts = concept.split(";")
                for c in concepts:
                    concept = c.strip().capitalize()
                    E55_uuid = cache_vocabulaires.get_uuid([column, concept], True)
            else:
                concept = concept.strip().capitalize()
                E55_uuid = cache_vocabulaires.get_uuid([column, concept], True)

            # Création des triplets RDF
            t(she(E55_uuid), a, crm("E55_Type"))
            t(she(E55_uuid), crm("P1_is_identified_by"), l(concept))
            t(she(E32_uuid), crm("P71_lists"), she(E55_uuid))

# indexations utilisant des vocabulaires
def indexation(vocabulaire, type_indexation):
    if row[vocabulaire] != None:
        indexation = row[vocabulaire]
        if ";" in indexation:
            indexations = indexation.split(";")
            for i in indexations:
                indexation = i.strip().capitalize()
                E55_indexation = she(cache_vocabulaires.get_uuid([vocabulaire, indexation]))
                make_E13([id, "F2 air", vocabulaire, indexation, "E13"], F2_air, she(type_indexation), E55_indexation)    
        else:
            indexation = indexation.strip().capitalize()
            E55_indexation = she(cache_vocabulaires.get_uuid([vocabulaire, indexation]))
            make_E13([id, "F2 air", vocabulaire, indexation, "E13"], F2_air, she(type_indexation), E55_indexation)  


#######################################################################################
# RECUPERATION DES DONNEES ET CREATION DES TRIPLETS
#######################################################################################

# Fichier Excel
sheet = load_workbook(args.xlsx).active
rows = get_xlsx_sheet_rows_as_dicts(sheet)

#------------------------------------------------------------------------------------
# Vocabulaires (E32 et E55)
#------------------------------------------------------------------------------------   
add_vocabulary("genre mus. Anne: OK")
add_vocabulary("genre poétique")
add_vocabulary("Tonalité. Anne: OK")
add_vocabulary("forme musicale. Anne: OK")
add_vocabulary("effectif musical")

#------------------------------------------------------------------------------------
#  Airs (F2)
#------------------------------------------------------------------------------------

for row in rows[1:]:
    id = row["id"]

    F2_air = she(cache.get_uuid([id, "F2 air", "uuid"], True))
    t(F2_air, a, lrm("F2_Expression"))
    t(F2_air, crm("P2_has_type"), she("a9d51926-c0ff-4304-b49d-9a18aff02d7e")) 

    # instanciation de l'air (pour lui associer une pagination)
    E33_instanciation_uuid = she(cache.get_uuid([id, "F2 air", "E33 instanciation", "uuid"], True))
    t(E33_instanciation_uuid, a, crm("E33_Linguistic_Object"))
    t(E33_instanciation_uuid, crm("P2_has_note"), l(row["pages"]))
    t(E33_instanciation_uuid, crm("P67_refers_to"), F2_air) 

    # rattachement de l'instanciation de l'air à son article
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

    # création de l'air
    F28_creation_air = she(cache.get_uuid([id, "F2 air", "F28 Creation", "uuid"], True))
    t(F28_creation_air, a, lrm("F28_Expression_Creation"))
    t(F28_creation_air, lrm("R17_created"), F2_air)
    # auteur de l'air
    if row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"] != None:
        auteurs_air = row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"].split(";")

        for auteur in auteurs_air:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                E21_auteur_air = auteur.split("[")[0].replace(" ", "")
            else:
                E21_auteur_air = auteur.replace(" ", "")

        make_E13([id, "F2 air", "F28 Creation", "E13"], F28_creation_air, crm("P14_carried_out_by"), she(E21_auteur_air))

    # !! #   #TODO CREER DES E55 POUR LES TYPES D'ATTRIBUTIONS?
    # !! #   #t(make_E13.E13, crm("P2_has_type"), l(type_attribution))


    # incipit musical
    if row["code incipit musical. Anne: OK"] != None:
        E42_air_incipit_musical = she(cache.get_uuid([id, "F2 air", "E42 incipit musical", "uuid"], True))
        t(E42_air_incipit_musical, a, crm("E42_Identifier"))
        t(F2_air, crm("P1_is_identified_by"), E42_air_incipit_musical)
        t(E42_air_incipit_musical, crm("P2_has_type"), she("f6ca9e82-e5fa-442d-a9e5-79fca664566e"))

        make_E13([id, "F2 air", "E42 incipit musical", "E13"], E42_air_incipit_musical, RDFS.label, l(row["code incipit musical. Anne: OK"]))    

    # note musicale
    if row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"] != None:
        make_E13([id, "F2 air", "note musicale", "E13"], F2_air, crm("P3_has_note"), l(row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"]))
   
    # genre musical
    indexation("genre mus. Anne: OK", "e6836743-fa50-4995-b534-ba13d1d24380")

    # formation musicale
    indexation("forme musicale. Anne: OK", "1deed97c-80cd-4ff5-a16b-b9e0cfc55a4c")

    # effectif musical
    indexation("effectif musical", "d1b826ac-83f6-4a39-a53d-3cf582c134da")
    # TODO notes sur les effectifs musicaux : typer le E13?

    # article et notes sur les sources??

    #------------------------------------------------------------------------------------
    #  Textes des airs (F2)
    #------------------------------------------------------------------------------------

    F2_texte = she(cache.get_uuid([id, "F2 texte", "uuid"], True))
    t(F2_texte, a, lrm("F2_Expression"))
    t(F2_texte, crm("P2_has_type"), she("fb1ac98a-1645-460f-9f26-23f36e216f7e"))
    make_E13([id, "F2 air", "F2 texte", "E13"], F2_air, lrm("R75_incorporates"), F2_texte)
    
    # Ecriture du texte
    F28_creation_texte = she(cache.get_uuid([id, "F2 texte", "F28 Creation", "uuid"], True))
    t(F28_creation_texte, a, lrm("F28_Expression_Creation"))
    t(F28_creation_texte, lrm("R17_created"), F2_texte)
    
    # auteur du texte
    if row["auteur texte IDENTIFIANT Nathalie : normalisation avec Directus OK"] != None:
        auteurs_texte = row["auteur texte IDENTIFIANT Nathalie : normalisation avec Directus OK"].split(";")

        for auteur in auteurs_texte:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                E21_auteur_texte = auteur.split("[")[0].replace(" ", "")
            else:
                E21_auteur_texte = auteur.replace(" ", "")

        make_E13([id, "F2 texte", "F28 Creation", "E13"], F28_creation_texte, crm("P14_carried_out_by"), she(E21_auteur_texte))
    
    # titre du texte
    if row["TITRES propres. Anne: OK orthographe normalisée"] != None:
        E35_titre_texte = she(cache.get_uuid([id, "F2 texte", "E35 titre", "uuid"], True))
        t(E35_titre_texte, a, crm("E35_Title"))
        t(E35_titre_texte, RDFS.label, l(row["TITRES propres. Anne: OK orthographe normalisée"]))
        make_E13([id, "F2 texte", "E35 titre", "E13"], F2_texte, crm("P102_has_title"), E35_titre_texte)
    
    # incipit textuel principal
    if row["Incipit principal ou premier"] != None:
        E41_texte_incipit_principal = she(cache.get_uuid([id, "F2 texte", "E41 incipit textuel", "principal", "uuid"], True))
        t(E41_texte_incipit_principal, a, crm("E41_Appellation"))
        t(E41_texte_incipit_principal, a, crm("E33_Linguistic_Object"))
        t(F2_texte, crm("P1_is_identified_by"), E41_texte_incipit_principal)
        t(E41_texte_incipit_principal, crm("P2_has_type"), she("5891daa1-81be-494a-8bf9-9055574f0530"))
        make_E13([id, "F2 texte", "E41 incipit textuel", "principal", "E13"], E41_texte_incipit_principal, crm("P190_has_symbolic_content"), l(row["Incipit principal ou premier"]))    
        
    # incipit textuel français    
    if row["incipit français"] != None:
        E41_texte_incipit_francais = she(cache.get_uuid([id, "F2 texte", "E41 incipit textuel", "français", "uuid"], True))
        t(E41_texte_incipit_francais, a, crm("E41_Appellation"))
        t(E41_texte_incipit_francais, a, crm("E33_Linguistic_Object"))
        t(F2_texte, crm("P1_is_identified_by"), E41_texte_incipit_francais)
        t(E41_texte_incipit_francais, crm("P2_has_type"), she("a7453d39-b7f0-4ca2-ba62-9fc560438c60"))

        make_E13([id, "F2 texte", "E41 incipit textuel", "français", "E13"], E41_texte_incipit_francais, crm("P190_has_symbolic_content"), l(row["incipit français"]))    


    # TODO lieux mentionnés
    

    # personnes mentionnées
    if row["personnes mentionnées (Nath : vérifier concordance et indexation avec Personnes"] != None:
        pass
        # colonne pleine d'anomalies
        #make_E13([id, "F2 texte", "E21 personne"], F2_texte, crm("P67_refers_to"), she(row["personnes mentionnées (Nath : vérifier concordance et indexation avec Personnes"]))

    # oeuvres citées
    if row["Œuvres citées"] != None:
        make_E13([id, "F2 texte", "oeuvre citée"], F2_texte, she("fa4f0240-ce36-4268-8c67-d4aa40cb9350"), l(row["Œuvres citées"]))    



#######################################################################################
# CREATION DU GRAPHE ET DU CACHE
#######################################################################################

cache.bye()
cache_vocabulaires.bye()

print("Ecriture du fichier ttl")

serialization = graph.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "w+") as f:
    f.write(serialization)
