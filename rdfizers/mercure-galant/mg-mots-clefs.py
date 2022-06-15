import argparse
import os
from pathlib import Path, PurePath
import sys
from sherlockcachemanagement import Cache
import re
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--rdf")
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# Helpers RDF
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Cache mots-clefs
concepts_uuid = {}

################################################################################
# Initialisation des graphes
################################################################################

input_graph = Graph()
input_graph.load(args.rdf)

def ro(s, p):
    try:
        return list(input_graph.objects(s, p))[0]
    except:
        return None


def ro_list(s, p):
    try:
        return list(input_graph.objects(s, p))
    except:
        return None

init_graph()

erreurs_id = []

for s, p, o in input_graph.triples((None, RDF.type, SKOS.ConceptScheme)):
    thesaurus_uri = s
    E32_uri = she("7cb0fe26-bd5b-42de-a0bb-e70ecc2a9a7a")

    topconcepts = ro_list(thesaurus_uri, SKOS.hasTopConcept)
    # print(topconcepts)
    
    def explore(c):
            E55_label = ro(c, SKOS.prefLabel).value.lower().strip()
            E55_uuid = ro(c, DCTERMS.identifier).value
            concepts_uuid[E55_label] = E55_uuid

            # Récupération des identifiants qui ne sont pas des uuid
            regex = r"(?:[a-zA-Z0-9]+-[a-zA-Z0-9]+){4,}$"
            m = re.search(regex, E55_uuid)
            if not m:
                erreurs_id.append(E55_uuid)

            E55_uri = she(E55_uuid)
            t(E55_uri, a, crm("E55_Type"))

            label = ro(c, SKOS.prefLabel)
            t(E55_uri, crm("P1_is_identified_by"), l(label))

            t(E32_uri, crm("P71_lists"), E55_uri)
            
            # Si c'est un topconcept
            if c in topconcepts:
                t(E32_uri, she_ns("sheP_a_pour_entité_de_plus_haut_niveau"), E55_uri)

            narrowers = ro_list(c, SKOS.narrower)
            for narrower in narrowers:
                narrower_uri = she(ro(narrower, DCTERMS.identifier).value)
                t(narrower_uri, crm("P127_has_broader_term"), E55_uri)

                explore(narrower)

    for topconcept in topconcepts:
        explore(topconcept)

for erreur in erreurs_id:
    print("Erreurs d'identifiants (devraient être des UUID)")
    print(erreur)

#print(concepts_uuid)

####################################################################################
# ECRITURE DES TRIPLETS
####################################################################################

save_graph(args.ttl)

with open(args.cache, "w+", encoding="utf-8") as f:
    yaml.dump(concepts_uuid, f, default_flow_style=False, allow_unicode=True)
