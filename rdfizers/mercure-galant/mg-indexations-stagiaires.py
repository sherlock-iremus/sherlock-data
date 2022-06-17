import argparse
import glob
from pathlib import Path
import ntpath
from pprint import pprint
from sherlockcachemanagement import Cache
import json
import sys
import os
import requests
import yaml

sys.path.append(os.path.abspath(os.path.join('directus/referentiels-ancien-regime/', '')))

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--txt")
parser.add_argument("--rdf")
parser.add_argument("--ttl")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")

args = parser.parse_args()

# Caches
cache = Cache(args.cache)
cache_tei = Cache(args.cache_tei)

# Helpers RDF
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Initialisation des graphes

input_graph = Graph()
input_graph.load(args.rdf)

def ro(s, p):
    try:
        return list(input_graph.objects(s, p))[0]
    except:
        return None


def make_E13(path, subject, predicate, object):
    E13_uri = she(cache.get_uuid(path, True))
    t(E13_uri, a, crm("E13_Attribute_Assignement"))
    t(E13_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
    t(E13_uri, crm("P140_assigned_attribute_to"), subject)
    t(E13_uri, crm("P141_assigned"), object)
    t(E13_uri, crm("P177_assigned_property_type"), predicate)

init_graph()

mots_clefs_uuid = {}

for s, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):
    mots_clefs_uuid[ro(s, SKOS.prefLabel).value.lower().replace("é", "e").replace("è", "e").replace("É", "e")] = ro(s, DCTERMS.identifier).value

pprint(mots_clefs_uuid)

# Fichiers TXT contenant les indexations
for file in glob.glob(args.txt + '**/*.txt', recursive=True):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
        id_article = ntpath.basename(file)[3:-4]
        id_livraison = id_article.split("_")[0]
        
        for line in lines:
            if "mots-clés" in line:
                mot_clef = line.split("clés")[1].strip().replace("\t", "").replace("’", "'").replace("\n", "").lower().replace("é", "e").replace("è", "e")
                if mot_clef in mots_clefs_uuid:
                    mot_clef_uri = she(mots_clefs_uuid[mot_clef])
                    try:
                        F2_uri = she(cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
                        make_E13(["indexations", "mots-clefs", id_article, mot_clef], F2_uri, crm("P67_refers_to"), mot_clef_uri)
                    except:
                        print("L'article", id_article, "ou la livraison", id_livraison, "est introuvable\n")
                else:
                    print(id_article + ": le mot-clé " + mot_clef + " est introuvable dans le thésaurus")

            elif "oeuvres citées" in line:
                oeuvre_citee = line.split("citées")[1].strip().replace("\t", "").replace("\n", "")
                try:
                        F2_uri = she(cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
                        make_E13(["indexations", "oeuvre citée", id_article, oeuvre_citee], F2_uri, she("fa4f0240-ce36-4268-8c67-d4aa40cb9350"), l(oeuvre_citee))
                except:
                    print("L'article", id_article, "ou la livraison", id_livraison, "est introuvable\n")
                

            elif "personnes" in line or "lieux" in line or "institutions" in line or "corporations" in line or "congrégations" in line:
                continue
                # TODO

            elif "_" in line or line.startswith("  ") or line.endswith("\n") :
                continue

            else:
                print("Mauvaise orthographe de 'mots-clés', 'oeuvres citées', 'lieux', 'personnes', 'institutions' ou 'congrégations' :")
                print("Fichier :", id_article)
                print("Ligne : " + line)
                print("\n")


################################################################################
# Sérialisation du graphe
################################################################################

save_graph(args.ttl)

cache.bye()