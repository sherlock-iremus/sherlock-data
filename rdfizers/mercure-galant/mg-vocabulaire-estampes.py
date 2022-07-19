import argparse
from sherlockcachemanagement import Cache
from rdflib import Graph, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, XSD, URIRef as u, Literal as l
from openpyxl import load_workbook
from pprint import pprint
import yaml
import sys
import pandas as pd
import numpy as np
from numpy import nan

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--xls")
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# INSTANCIATION DU GRAPHE
g = Graph()
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
g.bind("she", iremus_ns)
crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
g.bind("crm", crm_ns)
lrmoo_ns = Namespace("http://www.cidoc-crm.org/lrmoo/")
g.bind("lrmoo", lrmoo_ns)

def t(s, p, o):
    g.add((s, p, o))


def she(x):
    return iremus_ns[x]


def crm(x):
    return crm_ns[x]


def lrm(x):
    return lrmoo_ns[x]


a = RDF.type

###########################################################################################################
# CREATION DES DONNEES
###########################################################################################################

# Fichier Excel
vocabulaire = pd.read_excel(args.xls)
vocabulaire.dropna()
rows = vocabulaire.values.tolist()

# Le vocabulaire (E32)
E32_uuid = she('957985bf-e95a-4e29-b5ad-3520e2eea34e')
g.add((E32_uuid, RDF.type, crm('E32_Authority_Document')))
g.add((E32_uuid, crm('P1_is_identified_by'), l("Vocabulaire d'indexation des gravures du Mercure Galant")))
g.add((E32_uuid, DCTERMS.creator, she('ea287800-4345-4649-af12-7253aa185f3f')))

# Dictionnaires concept-UUID
concepts_uuid_avec_ancetres = {}

# Cache qui servira à l'indexation des estampes
concepts_uuid = {}

erreurs = []

# Ajout du concept concaténé à ses parents comme clé et de son uuid comme valeur
for row in rows:
    clé = ""
    line = [str(x) for x in row]

    # Récupération de l'équivalent iconclass 
    if line[6] != "nan":
        iconclass = line[6]
        t(she(line[0]), RDFS.seeAlso, l(iconclass))
        
    # Récupération de l'équivalent Getty
    if line[7] != "nan":
        getty = line[7]
        t(she(line[0]), RDFS.seeAlso, l(getty))

    line = [x for x in line[:6] if x != "nan"]
    for x in line[1:]:
        clé = clé + x + "|||"
    concepts_uuid_avec_ancetres[clé[:-3]] = line[0]


for clé, uuid in concepts_uuid_avec_ancetres.items():
    concept_ancetres = clé.split("|||")
    concept = concept_ancetres[-1]
    concept_uri = she(uuid)

    # Création d'un cache qui servira pour l'indexation des estampes
    concepts_uuid[concept] = uuid

    t(concept_uri, a, crm("E55_Type"))
    t(concept_uri, crm("P1_is_identified_by"), l(concept))
    t(E32_uuid, crm("P71_lists"), concept_uri)
    
    # Récupération des concepts de plus haut niveau
    if len(concept_ancetres) <= 1:
        t(E32_uuid, she("sheP_a_pour_entité_de_plus_haut_niveau"), concept_uri)
    
    # Récupération des parents
    else:
        broader_list = concept_ancetres[:-1]
        broader = "|||".join(broader_list)
        try:
            t(concept_uri, crm("P127_has_broader_term"), she(concepts_uuid_avec_ancetres[broader]))
        except:
            if concept_ancetres[-2] not in erreurs:
                erreurs.append(concept)


for erreur in erreurs:
    print("ancêtres mal renseignés:", erreur)


###########################################################################################################
# CREATION DU FICHIER TURTLE
###########################################################################################################

serialization = g.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "w+") as f:
    f.write(serialization)

with open(args.cache, "w+", encoding="utf-8") as f:
    yaml.dump(concepts_uuid, f, default_flow_style=False, allow_unicode=True)