import argparse
import os
import sys
import yaml
import json
from pprint import pprint
from sherlockcachemanagement import Cache

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--json_file")
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# Cache
cache = Cache(args.cache)

# Helpers RDF
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Graphe RDF
init_graph()

data = {}

with open(args.json_file, 'r') as f:
    data = json.load(f)

for k, v in data["livrets"].items():
    
    # Item
    F5_uri = she(v["sherlock_uuid"])
    t(F5_uri, a, lrm("F5_Item"))
    t(F5_uri, crm("P1_is_identified_by"), l(k))
    
    # Evenement de production de l'item
    F32_uri = she(cache.get_uuid(["livrets", k, "F32", "uuid"], True))
    t(F32_uri, a, lrm("F32_Carrier_Production_Event"))
    t(F32_uri, lrm("R28_produced"), F5_uri)

    # Manifestation
    F3_uri = she(cache.get_uuid(["livrets", k, "F3", "uuid"], True))
    t(F3_uri, a, lrm("F3_Manifestation"))
    t(F5_uri, lrm("R7_is_materialization_of"), F3_uri)
    t(F32_uri, lrm("R27_materialized"), F3_uri)

    # Expression
    F2_uri = she(cache.get_uuid(["livrets", k, "F2", "uuid"], True))
    t(F2_uri, a, lrm("F2_Expression"))
    t(F3_uri, lrm("R4_embodies"), F2_uri)



# Sérialisation du graphe
save_graph(args.ttl)

cache.bye()