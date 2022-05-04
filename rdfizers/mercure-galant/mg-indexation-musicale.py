import argparse
from openpyxl import load_workbook
import sys, os
from pprint import pprint
import pandas as pd
import math

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
parser.add_argument("--cache_mots_clefs")
parser.add_argument("--cache_tei")
args = parser.parse_args()

cache = Cache(args.cache)
cache_mots_clefs = Cache(args.cache_mots_clefs)
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

    for index, row in df.iterrows():
        concept = row[column]
        if concept == "null":
            continue
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

    print('Vocabulaire "' + column + '" créé')

# indexations utilisant des vocabulaires
def indexation_partition(vocabulaire, type_indexation):
    if row[vocabulaire] != "null":
        indexation = row[vocabulaire]
        indexations = indexation.split(";")
        for i in indexations:
            indexation = i.strip().capitalize()
            E55_indexation = she(cache_vocabulaires.get_uuid([vocabulaire, indexation]))
            make_E13([id, "air", vocabulaire, indexation, "E13"], partition_uri, she(type_indexation), E55_indexation)    
      
#######################################################################################
# RECUPERATION DES DONNEES ET CREATION DES TRIPLETS
#######################################################################################

# Fichier Excel
df = pd.read_excel(args.xlsx)
df = df.fillna("null")

# Création des vocabulaires (E32)
add_vocabulary("genre mus. Anne: OK")
add_vocabulary("Formes poétiques (fixes) ou description formelle")
add_vocabulary("Tonalité. Anne: OK")
add_vocabulary("forme musicale. Anne: OK")


#---------------------------------------------------------------------------------------
## Chansons regroupant une partition et un texte
#---------------------------------------------------------------------------------------

for index, row in df.iterrows():
    id = row["ref"]
    print("\n" + id)

    air_uri = she(cache.get_uuid([id, "air", "uuid"], True))
    t(air_uri, a, lrm("F2_Expression"))
    t(air_uri, crm("P2_has_type"), she("a9d51926-c0ff-4304-b49d-9a18aff02d7e"))
    E42_uri = she(cache.get_uuid([id, "air", "E42 identifiant", "uuid"], True))
    t(E42_uri, a, crm("E42_Identifier"))
    t(E42_uri, RDFS.label, l(id))
    t(air_uri, crm("P1_is_identified_by"), E42_uri) 

    # instanciation de la chanson (pour lui associer une pagination)
    instanciation_uri = she(cache.get_uuid([id, "air", "E33 instanciation", "uuid"], True))
    t(instanciation_uri, a, crm("E33_Linguistic_Object"))
    t(instanciation_uri, crm("P67_refers_to"), air_uri) 
    if row["pages\nne pas publier"] != "null":
        t(instanciation_uri, crm("P2_has_note"), l(row["pages\nne pas publier"]))

    # rattachement de l'instanciation de la chanson à son article
    if id != "null":
        id_article = id
        id_livraison = id[0:-4]
        if id_livraison.endswith("_"):
            id_livraison = id_livraison[0:-1]
        try:
            # article original
            article_F2_original = she(cache_tei.get_uuid(
                ["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
            t(article_F2_original, crm("P148_has_component"), instanciation_uri)
			# article TEI
            article_F2_TEI = she(cache_tei.get_uuid(
				["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
            t(article_F2_TEI, crm("P148_has_component"), instanciation_uri)
        except:
            pass
            #print("la chanson " + id + " n'est relié à aucun article")

    # titre de la chanson
    if row["TITRES propres. Anne: OK orthographe normalisée"] != "null":
        E35_uri = she(cache.get_uuid([id, "air", "E35 titre", "uuid"], True))
        t(E35_uri, a, crm("E35_Title"))
        t(E35_uri, RDFS.label, l(row["TITRES propres. Anne: OK orthographe normalisée"]))
        
        make_E13([id, "air", "E35 titre", "E13"], air_uri, crm("P102_has_title"), E35_uri)
       

    #-----------------------------------------------------------------------------------------
    ## La partition
    #-----------------------------------------------------------------------------------------

    partition_uri = she(cache.get_uuid([id, "air", "E90 partition", "uuid"], True))
    t(partition_uri, a, crm("E90_Symbolic_Object"))
    t(partition_uri, crm("P2_has_type"), she("fb1ac98a-1645-460f-9f26-23f36e216"))
    t(air_uri, lrm("P148_has_component"), partition_uri)

    E65_creation_partition = she(cache.get_uuid([id, "air", "E90 partition", "E65 Creation", "uuid"], True))
    t(E65_creation_partition, a, lrm("E65_Creation"))
    t(E65_creation_partition, lrm("P94_has_created"), partition_uri)
    # auteur de la partition
    if row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"] != "null":
        auteurs_partition = row["auteur de la musique IDENTIFIANT Nathalie : remplacer directement par l'id de Directus OK"].split(";")

        for auteur in auteurs_partition:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                auteur_partition_uri = auteur.split("[")[0].replace(" ", "")
            else:
                auteur_partition_uri = auteur.replace(" ", "")

        make_E13([id, "air", "E90 partition", "E65 Creation", "E13"], E65_creation_partition, crm("P14_carried_out_by"), she(auteur_partition_uri))

    # !! #   #TODO CREER DES E55 POUR LES TYPES D'ATTRIBUTIONS?
    # !! #   #t(make_E13.E13, crm("P2_has_type"), l(type_attribution))
    # lieux concernés

    # mots-clefs
    if row["MOTS-CLEFS. Anne: OK"] != "null":
        mots_clefs = row["MOTS-CLEFS. Anne: OK"].split(";")
        for x in mots_clefs:
            try:
                if x == "" or x == " ":
                    continue
                mot_clef = x.lower().strip()
                uuid = cache_mots_clefs.get_uuid([mot_clef])
            except:
                print("Le mot-clef", mot_clef, "est introuvable dans le thésaurus")

    # incipit musical
    if row["code incipit musical. Anne: OK"] != "null":
        partition_incipit_musical_uri = she(cache.get_uuid([id, "air", "E90 partition", "E42 incipit musical", "uuid"], True))
        t(partition_incipit_musical_uri, a, crm("E42_Identifier"))
        t(partition_uri, crm("P1_is_identified_by"), partition_incipit_musical_uri)
        t(partition_incipit_musical_uri, crm("P2_has_type"), she("f6ca9e82-e5fa-442d-a9e5-79fca664566e"))

        make_E13([id, "air", "E90 partition", "E42 incipit musical", "E13"], partition_incipit_musical_uri, RDFS.label, l(row["code incipit musical. Anne: OK"]))    

    # note musicale
    if row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"] != "null":
        make_E13([id, "air", "note musicale", "E13"], partition_uri, crm("P3_has_note"), l(row["notes sur la musique (tonalité, chiffre de mesure, nbre de mesures, forme). Anne: OK"]))
   
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
    
    texte_uri = she(cache.get_uuid([id, "air", "E33 texte", "uuid"], True))
    t(texte_uri, a, crm("E33_Linguistic_Object"))
    t(texte_uri, crm("P2_has_type"), she("fb1ac98a-1645-460f-9f26-23f36e216f7e"))
    t(air_uri, lrm("P148_has_component"), texte_uri)

    # Ecriture du texte
    creation_texte_uri = she(cache.get_uuid([id, "air", "E33 texte", "E65 Creation", "uuid"], True))
    t(creation_texte_uri, a, lrm("E65_Creation"))
    t(creation_texte_uri, lrm("P94_has_created"), texte_uri)
    
    # auteur du texte
    if row["auteur texte IDENTIFIANT Nathalie : normalisation avec Directus OK"] != "null":
        auteurs_texte = row["auteur texte IDENTIFIANT Nathalie : normalisation avec Directus OK"].split(";")

        for auteur in auteurs_texte:
            if "[" in auteur:
                type_attribution = auteur.split("[")[1].replace("]", "")
                E21_auteur_texte = auteur.split("[")[0].replace(" ", "")
            else:
                E21_auteur_texte = auteur.replace(" ", "")

        make_E13([id, "air", "E33 texte", "E65 Creation", "E13"], creation_texte_uri, crm("P14_carried_out_by"), she(E21_auteur_texte))
    
    # incipit textuel principal
    if row["Incipit principal ou premier"] != "null":
        texte_incipit_principal_uri = she(cache.get_uuid([id, "air", "E33 texte", "E41 incipit textuel", "principal", "uuid"], True))
        t(texte_incipit_principal_uri, a, crm("E41_Appellation"))
        t(texte_incipit_principal_uri, a, crm("E33_Linguistic_Object"))
        t(texte_incipit_principal_uri, crm("P190_has_symbolic_content"), l(row["Incipit principal ou premier"]))
        t(texte_incipit_principal_uri, crm("P2_has_type"), she("5891daa1-81be-494a-8bf9-9055574f0530"))
       
        make_E13([id, "air", "E33 texte", "E41 incipit textuel", "principal", "E13"], texte_uri, crm("P1_is_identified_by"), texte_incipit_principal_uri)    
        
    # incipit textuel français    
    if row["incipit français"] != "null":
        texte_incipit_francais_uri = she(cache.get_uuid([id, "air", "E33 texte", "E41 incipit textuel", "français", "uuid"], True))
        t(texte_incipit_francais_uri, a, crm("E41_Appellation"))
        t(texte_incipit_francais_uri, a, crm("E33_Linguistic_Object"))
        t(texte_incipit_francais_uri, crm("P190_has_symbolic_content"), l(row["incipit français"]))
        t(texte_incipit_francais_uri, crm("P2_has_type"), she("a7453d39-b7f0-4ca2-ba62-9fc560438c60"))

        make_E13([id, "air", "E33 texte", "E41 incipit textuel", "français", "E13"], texte_uri, crm("P1_is_identified_by"), texte_incipit_francais_uri)    


    # TODO lieux mentionnés
    
    # personnes mentionnées
    pers_mentionnees = row["personnes mentionnées (Nath : vérifier concordance et indexation avec Personnes OK"]
    if pers_mentionnees != "null":
        pers_mentionnees_list = pers_mentionnees.split(";")
        for pers in pers_mentionnees_list:
            make_E13([id, "air", "E33 texte", "E21 personne"], texte_uri, crm("P67_refers_to"), she(pers.strip()))

    # oeuvres citées
    if row["Œuvres citées"] != "null":
        make_E13([id, "air", "E33 texte", "oeuvre citée"], texte_uri, she("fa4f0240-ce36-4268-8c67-d4aa40cb9350"), l(row["Œuvres citées"]))    



#######################################################################################
# CREATION DU GRAPHE ET DU CACHE
#######################################################################################

cache.bye()
cache_vocabulaires.bye()

save_graph(args.ttl)