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

init_graph()

######################################################################################
# FONCTIONS
######################################################################################

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
def indexation_partition(vocabulaire, type_indexation):
    if row[vocabulaire] != None:
        indexation = row[vocabulaire]
        if ";" in indexation:
            indexations = indexation.split(";")
            for i in indexations:
                indexation = i.strip().capitalize()
                E55_indexation = she(cache_vocabulaires.get_uuid([vocabulaire, indexation]))
                make_E13([id, "F2 chanson", vocabulaire, indexation, "E13"], E90_partition, she(type_indexation), E55_indexation)    
        else:
            indexation = indexation.strip().capitalize()
            E55_indexation = she(cache_vocabulaires.get_uuid([vocabulaire, indexation]))
            make_E13([id, "F2 chanson", vocabulaire, indexation, "E13"], E90_partition, she(type_indexation), E55_indexation)  


#######################################################################################
# RECUPERATION DES DONNEES ET CREATION DES TRIPLETS
#######################################################################################

# Fichier Excel
sheet = load_workbook(args.xlsx).active
rows = get_xlsx_sheet_rows_as_dicts(sheet)

# Création des vocabulaires (E32)
add_vocabulary("genre mus. Anne: OK")
add_vocabulary("Formes poétiques (fixes) ou description formelle")
add_vocabulary("Tonalité. Anne: OK")
add_vocabulary("forme musicale. Anne: OK")


#---------------------------------------------------------------------------------------
## Chansons regroupant une partition et un texte
#---------------------------------------------------------------------------------------

for row in rows[1:]:
    id = row["id"]

    F2_chanson = she(cache.get_uuid([id, "F2 chanson", "uuid"], True))
    t(F2_chanson, a, lrm("F2_Expression"))
    t(F2_chanson, crm("P2_has_type"), she("a9d51926-c0ff-4304-b49d-9a18aff02d7e")) 

    # instanciation de la chanson (pour lui associer une pagination)
    E33_instanciation_uuid = she(cache.get_uuid([id, "F2 chanson", "E33 instanciation", "uuid"], True))
    t(E33_instanciation_uuid, a, crm("E33_Linguistic_Object"))
    t(E33_instanciation_uuid, crm("P2_has_note"), l(row["pages"]))
    t(E33_instanciation_uuid, crm("P67_refers_to"), F2_chanson) 

    # rattachement de l'instanciation de la chanson à son article
    if id != None:
        id_article = id
        id_livraison = id[0:-4]
        if id_livraison.endswith("_"):
            id_livraison = id_livraison[0:-1]
        try:
            # article original
            article_F2_original = she(cache_tei.get_uuid(
                ["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
            t(article_F2_original, crm("P148_has_component"), F2_chanson)
			# article TEI
            article_F2_TEI = she(cache_tei.get_uuid(
				["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
            t(article_F2_TEI, crm("P148_has_component"), F2_chanson)
        except:
            pass
            #print("la chanson " + id + " n'est relié à aucun article")

    # titre de la chanson
    if row["TITRES propres. Anne: OK orthographe normalisée"] != None:
        E35_titre = she(cache.get_uuid([id, "F2 chanson", "E35 titre", "uuid"], True))
        t(E35_titre, a, crm("E35_Title"))
        t(E35_titre, RDFS.label, l(row["TITRES propres. Anne: OK orthographe normalisée"]))
        
        make_E13([id, "F2 chanson", "E35 titre", "E13"], F2_chanson, crm("P102_has_title"), E35_titre)
       

    #-----------------------------------------------------------------------------------------
    ## La partition
    #-----------------------------------------------------------------------------------------

    E90_partition = she(cache.get_uuid([id, "F2 chanson", "E90 partition", "uuid"], True))
    t(E90_partition, a, crm("E90_Symbolic_Object"))
    t(E90_partition, crm("P2_has_type"), she("fb1ac98a-1645-460f-9f26-23f36e216f7e"))
    t(F2_chanson, lrm("P148_has_component"), E90_partition)

    E65_creation_partition = she(cache.get_uuid([id, "F2 chanson", "E90 partition", "E65 Creation", "uuid"], True))
    t(E65_creation_partition, a, lrm("E65_Creation"))
    t(E65_creation_partition, lrm("P94_has_created"), E90_partition)
    # auteur de la partition
    if row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"] != None:
        auteurs_partition = row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"].split(";")

        for auteur in auteurs_partition:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                E21_auteur_partition = auteur.split("[")[0].replace(" ", "")
            else:
                E21_auteur_partition = auteur.replace(" ", "")

        make_E13([id, "F2 chanson", "E90 partition", "E65 Creation", "E13"], E65_creation_partition, crm("P14_carried_out_by"), she(E21_auteur_partition))

    # !! #   #TODO CREER DES E55 POUR LES TYPES D'ATTRIBUTIONS?
    # !! #   #t(make_E13.E13, crm("P2_has_type"), l(type_attribution))

    # incipit musical
    if row["code incipit musical. Anne: OK"] != None:
        E42_partition_incipit_musical = she(cache.get_uuid([id, "F2 chanson", "E90 partition", "E42 incipit musical", "uuid"], True))
        t(E42_partition_incipit_musical, a, crm("E42_Identifier"))
        t(E90_partition, crm("P1_is_identified_by"), E42_partition_incipit_musical)
        t(E42_partition_incipit_musical, crm("P2_has_type"), she("f6ca9e82-e5fa-442d-a9e5-79fca664566e"))

        make_E13([id, "F2 chanson", "E90 partition", "E42 incipit musical", "E13"], E42_partition_incipit_musical, RDFS.label, l(row["code incipit musical. Anne: OK"]))    

    # note musicale
    if row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"] != None:
        make_E13([id, "F2 chanson", "note musicale", "E13"], E90_partition, crm("P3_has_note"), l(row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"]))
   
    # genre musical
    indexation_partition("genre mus. Anne: OK", "e6836743-fa50-4995-b534-ba13d1d24380")

    # forme musicale
    indexation_partition("forme musicale. Anne: OK", "1deed97c-80cd-4ff5-a16b-b9e0cfc55a4c")

    # formes poétiques
    indexation_partition("forme musicale. Anne: OK", "99239c96-a989-4a39-9c00-20c9d4b4c424")

    # effectif musical
    ## en attente du thésaurus Directus de Nathalie
    # TODO notes sur les effectifs musicaux : typer le E13?

    #------------------------------------------------------------------------------------
    #  Textes des chansons (F2)
    #------------------------------------------------------------------------------------

    
    E33_texte = she(cache.get_uuid([id, "F2 chanson", "E33 texte", "uuid"], True))
    t(E33_texte, a, crm("E33_Linguistic_Object"))
    t(E33_texte, crm("P2_has_type"), she("fb1ac98a-1645-460f-9f26-23f36e216f7e"))
    t(F2_chanson, lrm("P148_has_component"), E33_texte)

    # Ecriture du texte
    E65_creation_texte = she(cache.get_uuid([id, "F2 chanson", "E33 texte", "E65 Creation", "uuid"], True))
    t(E65_creation_texte, a, lrm("E65_Creation"))
    t(E65_creation_texte, lrm("P94_has_created"), E33_texte)
    
    # auteur du texte
    if row["auteur texte IDENTIFIANT Nathalie : normalisation avec Directus OK"] != None:
        auteurs_texte = row["auteur texte IDENTIFIANT Nathalie : normalisation avec Directus OK"].split(";")

        for auteur in auteurs_texte:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                E21_auteur_texte = auteur.split("[")[0].replace(" ", "")
            else:
                E21_auteur_texte = auteur.replace(" ", "")

        make_E13([id, "F2 chanson", "E33 texte", "E65 Creation", "E13"], E65_creation_texte, crm("P14_carried_out_by"), she(E21_auteur_texte))
    
    # incipit textuel principal
    if row["Incipit principal ou premier"] != None:
        E41_texte_incipit_principal = she(cache.get_uuid([id, "F2 chanson", "E33 texte", "E41 incipit textuel", "principal", "uuid"], True))
        t(E41_texte_incipit_principal, a, crm("E41_Appellation"))
        t(E41_texte_incipit_principal, a, crm("E33_Linguistic_Object"))
        t(E41_texte_incipit_principal, crm("P190_has_symbolic_content"), l(row["Incipit principal ou premier"]))
        t(E41_texte_incipit_principal, crm("P2_has_type"), she("5891daa1-81be-494a-8bf9-9055574f0530"))
       
        make_E13([id, "F2 chanson", "E33 texte", "E41 incipit textuel", "principal", "E13"], E33_texte, crm("P1_is_identified_by"), E41_texte_incipit_principal)    
        
    # incipit textuel français    
    if row["incipit français"] != None:
        E41_texte_incipit_francais = she(cache.get_uuid([id, "F2 chanson", "E33 texte", "E41 incipit textuel", "français", "uuid"], True))
        t(E41_texte_incipit_francais, a, crm("E41_Appellation"))
        t(E41_texte_incipit_francais, a, crm("E33_Linguistic_Object"))
        t(E41_texte_incipit_francais, crm("P190_has_symbolic_content"), l(row["incipit français"]))
        t(E41_texte_incipit_francais, crm("P2_has_type"), she("a7453d39-b7f0-4ca2-ba62-9fc560438c60"))

        make_E13([id, "F2 chanson", "E33 texte", "E41 incipit textuel", "français", "E13"], E33_texte, crm("P1_is_identified_by"), E41_texte_incipit_francais)    


    # TODO lieux mentionnés
    

    # personnes mentionnées
    pers_mentionnees = row["personnes mentionnées (Nath : vérifier concordance et indexation avec Personnes"]
    if pers_mentionnees != None:
        pers_mentionnees_list = pers_mentionnees.split(";")
        for pers in pers_mentionnees_list:
            make_E13([id, "F2 chanson", "E33 texte", "E21 personne"], E33_texte, crm("P67_refers_to"), she(pers.strip()))

    # oeuvres citées
    if row["Œuvres citées"] != None:
        make_E13([id, "F2 chanson", "E33 texte", "oeuvre citée"], E33_texte, she("fa4f0240-ce36-4268-8c67-d4aa40cb9350"), l(row["Œuvres citées"]))    



#######################################################################################
# CREATION DU GRAPHE ET DU CACHE
#######################################################################################

cache.bye()
cache_vocabulaires.bye()

save_graph(args.ttl)