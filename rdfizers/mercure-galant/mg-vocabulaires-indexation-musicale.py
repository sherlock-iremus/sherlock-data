import argparse
import pandas
from pprint import pprint
import os, sys
import yaml
import uuid

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
from helpers_rdf import *

##############################################################################################
## RECUPERATION DES DONNEES
##############################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("--csv")
parser.add_argument("--ttl")
parser.add_argument("--yaml")
args = parser.parse_args()

# TODO souci avec les noms de colonnes trop grands? Si erreur "Usecols do not match columns",
# changer nom de la colonne
cols = ["genre mus. Anne: OK", "genre poétique", "Tonalité. Anne: OK", "forme musicale. Anne: OK", "effectif musical"]

df = pandas.read_csv(args.csv, decimal=",", sep=";", usecols=cols)
df = df.dropna()

# Récupération du cache ou création s'il est vide
cache = yaml.safe_load(open(args.yaml, 'r+'))
if cache is None:
    cache = {}

##############################################################################################
## CREATION DU FICHIER TURTLE
##############################################################################################

# Initialisation du graphe
g = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")

g.bind("crm", crm_ns)
g.bind("she", iremus_ns)

# Fonctions
a = RDF.type

def crm(x):
    return crm_ns[x]

def she(x):
    return iremus_ns[x]

def t(s, p, o):
    g.add((s, p, o))

# Récupération des UUID des vocabulaires
def add_vocabulary(column):
    try:
        # Si l'UUID existe déjà dans le cache
        E32_uuid = cache[column]["uuid"]
    except:
        # L'UUID n'existe pas dans le cache
        E32_uuid = str(uuid.uuid4())
        cache[column] = {"uuid": E32_uuid}
    
    t(she(E32_uuid), a, crm("E32_Authority_Document"))
    t(she(E32_uuid), crm("P1_is_identified_by"), l(column))

    # Création d'une liste à partir de la colonne
    mylist = df[column].tolist()
    mylist_no_duplicates = list(dict.fromkeys(mylist))
    # Suppression des doublons et normalisation des éléments
    mynewlist = []
    for item in mylist_no_duplicates:
        item = item.strip().capitalize()
        if ";" in item:
            items = item.split(";")
            for i in items:
                item = i.strip().capitalize()
        if item not in mynewlist and len(item) >= 1 and "[" not in item:
            mynewlist.append(item)

    # Récupération des UUIDs des concepts
    for item in mynewlist:
        try:
            E55_uuid = cache[column][item]
        except:
            E55_uuid = str(uuid.uuid4())
            cache[column][item] = E55_uuid      

        # Création des triplets RDF
        t(she(E55_uuid), a, crm("E55_Type"))
        t(she(E55_uuid), crm("P1_is_identified_by"), l(item))
        t(she(E32_uuid), crm("P71_lists"), she(E55_uuid))

add_vocabulary("genre mus. Anne: OK")
add_vocabulary("genre poétique")
add_vocabulary("Tonalité. Anne: OK")
add_vocabulary("forme musicale. Anne: OK")
add_vocabulary("effectif musical")


# Réecriture du cache
with open(args.yaml, "w", encoding='utf8') as new_cache:
    yaml.dump(cache, new_cache, default_flow_style=False, allow_unicode=True)

# Ecriture du fichier ttl
print("Ecriture du fichier ttl")

serialization = g.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "w+") as f:
    f.write(serialization)
