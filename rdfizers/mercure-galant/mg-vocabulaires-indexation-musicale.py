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
parser.add_argument("--cache")
args = parser.parse_args()

# TODO souci avec les noms de colonnes trop grands? Si erreur "Usecols do not match columns",
# changer nom de la colonne
cols = ["genre mus. Anne: OK", "genre poétique", "Tonalité. Anne: OK", "forme musicale. Anne: OK", "effectif musical"]

df = pandas.read_csv(args.csv, decimal=",", sep=";", usecols=cols)
df = df.dropna()

cache = yaml.safe_load(open(args.cache, 'r+'))

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


# Création des données

def create_list(column):
    mylist = df[column].tolist()
    mylist_no_duplicates = list(dict.fromkeys(mylist))
    mynewlist = []
    for item in mylist_no_duplicates:
        item = item.strip().capitalize()
        if ";" in item:
            items = item.split(";")
            for i in items:
                item = i.strip().capitalize()
        if item not in mynewlist and len(item) >= 1 and "[" not in item:
            mynewlist.append(item)
   
    for item in mynewlist:
        try:
            E55_uuid = cache[column][item]
        except:
            E55_uuid = str(uuid.uuid4())
            d = {}
            d[column] = {item: E55_uuid}
            with open(args.cache, "w", encoding='utf8') as cache:
                yaml.dump(d, cache, default_flow_style=False, allow_unicode=True)
                

create_list("genre mus. Anne: OK")
create_list("genre poétique")
create_list("Tonalité. Anne: OK")
create_list("forme musicale. Anne: OK")
create_list("effectif musical")

# Ecriture du fichier ttl

print("Ecriture du fichier ttl")

serialization = g.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "w+") as f:
    f.write(serialization)
