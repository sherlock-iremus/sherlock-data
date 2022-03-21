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
    
    # Production de l'item
    F32_uri = she(cache.get_uuid(["livrets", k, "F32", "uuid"], True))
    t(F32_uri, a, lrm("F32_Carrier_Production_Event"))
    t(F32_uri, lrm("R28_produced"), F5_uri)

    # Manifestation
    F3_uri = she(cache.get_uuid(["livrets", k, "F3", "uuid"], True))
    t(F3_uri, a, lrm("F3_Manifestation"))
    t(F5_uri, lrm("R7_is_materialization_of"), F3_uri)
    t(F32_uri, lrm("R27_materialized"), F3_uri)

    # Creation de la manifestation
    F30_uri = she(cache.get_uuid(["livrets", k, "F30", "uuid"], True))
    t(F30_uri, a, lrm("F30_Manifestation_Creation"))
    t(F30_uri, lrm("R24_created"), F3_uri)

    # Expression
    F2_uri = she(cache.get_uuid(["livrets", k, "F2", "uuid"], True))
    t(F2_uri, a, lrm("F2_Expression"))
    t(F3_uri, lrm("R4_embodies"), F2_uri)

    # Creation de l'expression
    F28_uri = she(cache.get_uuid(["livrets", k, "F28", "uuid"], True))
    t(F28_uri, a, lrm("F28_Expression_Creation"))
    t(F28_uri, lrm("R17_created"), F2_uri)

    # Photographie de l'item
    E65_uri = she(cache.get_uuid(["livrets", k, "E65", "uuid"], True))
    t(E65_uri, a, crm("E65_Creation"))
    t(E65_uri, crm("P16_used_specific_object"), F5_uri)
    t(E65_uri, crm("P14_carried_out_by"), she("710d0c6e-48ed-47b6-b209-00520636d7be"))
    E36_uri = she(cache.get_uuid(["livrets", k, "E65", "E36", "uuid"], True))
    t(E36_uri, a, crm("E36_Visual_Item"))
    t(E65_uri, crm("P94_has_created"), E36_uri)


# Sérialisation du graphe
save_graph(args.ttl)

cache.bye()