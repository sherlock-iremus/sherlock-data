import argparse
from sherlockcachemanagement import Cache
from rdflib import Graph, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, XSD, URIRef as u, Literal as l
from openpyxl import load_workbook
from pprint import pprint
import yaml
import sys

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--xls")
parser.add_argument("--ttl")
parser.add_argument("--cache")
parser.add_argument("--cache_applati")
args = parser.parse_args()

# CACHE
cache = Cache(args.cache)
cache_applati = Cache(args.cache_applati)

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
fichier_excel = load_workbook(args.xls)
vocab_excel = fichier_excel.active

# Le vocabulaire (E32)
E32_uuid = she('957985bf-e95a-4e29-b5ad-3520e2eea34e')
g.add((E32_uuid, RDF.type, crm('E32_Authority_Document')))
g.add((E32_uuid, crm('P1_is_identified_by'), l("Vocabulaire d'indexation des gravures du Mercure Galant")))
g.add((E32_uuid, DCTERMS.creator, she('ea287800-4345-4649-af12-7253aa185f3f')))

# Dictionnaire concept-UUID
uuid_concepts = {}

# Création d'une liste par ligne de tableur
for row in vocab_excel:

    # Ignorer la première ligne
    if row[0].value == "uuid SHERLOCK":
        continue

    line = []

    # Ajout de chaque concept de la ligne dans la liste
    for colonne in row:
        if colonne.value != None and colonne != row[6] and colonne != row[7] and colonne != row[0]:
            concept = colonne.value.replace(";", "").strip()
            line.append(concept)

            # Ajout du concept dans le dictionnaire UUID-concept
            if concept in uuid_concepts:
                continue
            uuid_concepts[concept] = row[0].value

        # Equivalents Iconclass et Getty AAT
        if colonne == row[6] or colonne == row[7]:
            if colonne.value != None:
                seeAlso = colonne.value
                t(she(row[0].value), RDFS.seeAlso, l(seeAlso))

    if len(line) == 0:
        continue

    # line = [concept.lower() for concept in line]

    # Récupération des concepts de plus haut niveau
    if len(line) <= 1:
        top_concept = she(row[0].value)
    t(E32_uuid, she("sheP_a_pour_entité_de_plus_haut_niveau"), top_concept)


    # Création de triplets pour chaque concept (E55)
    for concept in line:
        E55_Type = she(row[0].value)
        t(E55_Type, a, crm("E55_Type"))
        t(E55_Type, crm("P1_is_identified_by"), l(line[-1]))
        t(E32_uuid, crm("P71_lists"), E55_Type)

    # Broader du concept
    if len(line) > 1:
        broader = line[-2]
        t(E55_Type, crm("P127_has_broader_term"), she(uuid_concepts[broader]))


###########################################################################################################
# CREATION DU FICHIER TURTLE
###########################################################################################################

serialization = g.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "wb") as f:
    f.write(serialization)
