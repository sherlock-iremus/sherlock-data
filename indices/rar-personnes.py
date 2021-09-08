import argparse
import json
from pprint import pprint
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--dburi")
parser.add_argument("--json")
args = parser.parse_args()

index = {}

def normalize_string(s):
    s_norm = ''

    for c in s:
        if c.isalnum() == False:
            pass
        elif c in 'ÀÁÂÃÄÅàáâãäå':
            s_norm += 'a'
        elif c in 'Çç':
            s_norm += 'c'
        elif c in 'ÈÉÊËèéêë':
            s_norm += 'e'
        elif c in 'ÒÓÔÕÖØòóôõöø':
            s_norm += 'o'
        elif c in 'ÌÍÎÏìíîï':
            s_norm += 'i'
        elif c in 'ÙÚÛÜùúûü':
            s_norm += 'u'
        elif c in 'ÿ':
            s_norm += 'y'
        elif c in 'Ññ':
            s_norm += 'n'
        elif c == 'œ':
            s_norm += 'o'
            s_norm += 'e'
        elif c == 'ß':
            s_norm += 'ss'
        else:
            s_norm += c

    return s_norm.lower()


#######################################################################################
# INSERTION DES DONNEES DANS DES DICTIONNAIRES
#######################################################################################

norm_label_to_entities_registry = {}
norm_label_to_label_registry = {}
entity_to_label_registry = {}
entity_to_E32 = {}
preflabels = []

# E21, P1 et E32
r = requests.get(args.dburi,  params={"query": """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?entity ?preflabel ?altlabel ?E32 ?E32_label
WHERE {

    GRAPH <http://data-iremus.huma-num.fr/graph/rar> {
    
      ?entity rdf:type crm:E21_Person .
      ?entity crm:P1_is_identified_by ?E41preflabel .
      ?E41preflabel crm:P2_has_type skos:prefLabel .
      ?E41preflabel rdfs:label ?preflabel .
      
      ?entity crm:P1_is_identified_by ?E41altlabel .
      ?E41altlabel crm:P2_has_type skos:altLabel .
      ?E41altlabel rdfs:label ?altlabel .
      
      ?E32 crm:P71_lists ?entity .

    }  
}
"""})

for b in r.json()["results"]["bindings"]:
    entity = b["entity"]["value"]
    preflabel = b["preflabel"]["value"]
    altlabel = b["altlabel"]["value"]
    E32 = b["E32"]["value"]
    preflabel_norm = normalize_string(preflabel)
    altlabel_norm = normalize_string(altlabel)

    if not preflabel_norm in norm_label_to_entities_registry:
        norm_label_to_entities_registry[preflabel_norm] = entity

    if not altlabel_norm in norm_label_to_entities_registry:
        norm_label_to_entities_registry[altlabel_norm] = entity

    if not entity in entity_to_label_registry:
        entity_to_label_registry[entity] = []

    if not preflabel in entity_to_label_registry[entity]:
        entity_to_label_registry[entity].append(preflabel)

    if not altlabel in entity_to_label_registry[entity]:
        entity_to_label_registry[entity].append(altlabel)

    # Calcul du nombre de preflabel/altlabel
    # for k, v in entity_to_label_registry.items():
    #     if len(v) >= 13:
    #         print(k, len(v))

    if not preflabel_norm in norm_label_to_label_registry:
        norm_label_to_label_registry[preflabel_norm] = preflabel

    if not altlabel_norm in norm_label_to_label_registry:
        norm_label_to_label_registry[altlabel_norm] = altlabel

    if not entity in entity_to_E32:
        entity_to_E32[entity] = E32

# Calcul du nombre de personnes dans le référentiel
r = requests.get(args.dburi,  params={"query": """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?E32 (count(distinct ?entity) as ?cnt)
WHERE {

    GRAPH <http://data-iremus.huma-num.fr/graph/rar> {

      ?E32 crm:P71_lists ?entity .
      ?E32 crm:P1_is_identified_by "Noms de personnes" . 
      
    }
} GROUP BY ?E32 
"""})

for b in r.json()["results"]["bindings"]:
    nombre_E21 = b["cnt"]["value"]

#######################################################################################
# CREATION DE L'INDEX
#######################################################################################

index = {"référentiels": {
    "label": "Noms de personnes",
    "note": "...",
    "n" : nombre_E21
    },
    "concepts": {}}

# le label normalisé de l'entité
for label_norm, iri in norm_label_to_entities_registry.items():
    index["concepts"][label_norm] = {}
    index["concepts"][label_norm][iri] = {}

    if label_norm in norm_label_to_label_registry:
        index["concepts"][label_norm]["label"] = norm_label_to_label_registry[label_norm]

    # E32 Authority Document
    for entity, E32 in entity_to_E32.items():
        if entity == iri:
            index["concepts"][label_norm][iri]["E32"] = E32


# Recherche de doublons dans le thésaurus
duplicates = []

for k, v in entity_to_label_registry.items():
    for personne in v:
        duplicates.append(personne)

pprint([x for x in duplicates if duplicates.count(x) > 1])


# Ecriture du JSON
with open(args.json, 'w', encoding='utf8') as f:
    json.dump(index, f, ensure_ascii=False)
