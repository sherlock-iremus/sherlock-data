import argparse
import json
import pandas as pd
from pprint import pprint
import py4cytoscape as p4c
from rdflib import Graph
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--ttl')
args = parser.parse_args()

g = Graph()
g.parse(args.ttl, format="ttl")

BASE = 'http://127.0.0.1:1234/v1/'
HEADERS = {'Content-Type': 'application/json'}
print("🐸", p4c.cytoscape_ping())
print("🐸", p4c.cytoscape_version_info())
# p4c.cyrest_api()
# p4c.commands_api()

################################################################################
# INIT EMPTY NETWORK
################################################################################

requests.delete(BASE + 'networks')
empty_network = {
    'data': {
        'name': args.ttl
    },
    'elements': {
        'nodes': [],
        'edges': []
    }
}
res = requests.post(BASE + 'networks?collection=My%20Collection', data=json.dumps(empty_network), headers=HEADERS)
net_suid = res.json()['networkSUID']
print('🍄 New empty network with suid ' + str(net_suid), '!')

print("🐙", "set_edge_target_arrow_shape_default")
p4c.set_edge_target_arrow_shape_default('ARROW')
print("🐙", "set_edge_label_mapping")
p4c.set_edge_label_mapping('interaction')
print("🐙", "set_edge_label_color_default")
p4c.set_edge_label_color_default('deeppink')
print("🐙", "set_node_selection_color_default")
p4c.set_node_selection_color_default("black")

################################################################################
# DATA STRUCTURES
################################################################################

nodes_uri = {}
nodes_literals = {}
edges = {}
edges_literal = {}
NODE_NAME_TO_SUID = {}
types = []

################################################################################
# HELPERS
################################################################################


def census_node(node_name):
    if node_name not in NODE_NAME_TO_SUID:
        res = requests.post(f'{BASE}networks/{net_suid}/nodes', json=[node_name])
        NODE_NAME_TO_SUID[node_name] = res.json()[0]["SUID"]

    return NODE_NAME_TO_SUID[node_name]


def shorten_uri(uri):
    uri = uri.replace('http://data-iremus.huma-num.fr/antony/id/', 'antony:')
    uri = uri.replace('http://data-iremus.huma-num.fr/id/', ':')
    uri = uri.replace('http://iflastandards.info/ns/lrm/lrmoo/', 'lrmoo:')
    uri = uri.replace('http://www.cidoc-crm.org/cidoc-crm/', 'crm:')
    uri = uri.replace('http://www.w3.org/2000/01/rdf-schema#', 'rdfs:')
    uri = uri.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'rdf:')
    uri = uri.replace('http://data-iremus.huma-num.fr/ns/sherlock#', 'sherlock:')
    return uri


################################################################################
# EXPLORE RDF DATA
################################################################################

for r in g.query("SELECT * WHERE { ?s ?p ?o . FILTER (!isLiteral(?o)) }"):
    s = shorten_uri(str(r.s))
    if s not in nodes_uri:
        nodes_uri[s] = {}

    o = shorten_uri(str(r.o))
    if o not in nodes_uri:
        nodes_uri[o] = {}

    p = shorten_uri(str(r.p))
    if p not in edges:
        edges[p] = []
    edges[p].append([s, o])

for r in g.query("SELECT * WHERE { ?s ?p ?o . FILTER (isLiteral(?o)) }"):
    s = shorten_uri(str(r.s))
    if s not in nodes_uri:
        nodes_uri[s] = {}

    o = str(r.o)
    if o not in nodes_literals:
        nodes_literals[o] = {}

    p = shorten_uri(str(r.p))
    if p not in edges_literal:
        edges_literal[p] = []
    edges_literal[p].append([s, o])

################################################################################
# MEMO
################################################################################

nodes_uri_names = list(nodes_uri.keys())
nodes_names = nodes_uri_names + list(nodes_literals.keys())
nodes_literal_names = list(nodes_literals.keys())

# NODES URI
print(f"🍄 {len(nodes_uri)} nodes uri")
res = p4c.add_cy_nodes(nodes_uri_names, skip_duplicate_names=False, network=net_suid)

# NODES LITERALS
print(f"🍄 {len(nodes_literals)} nodes literals")
res = p4c.add_cy_nodes(nodes_literal_names, skip_duplicate_names=False, network=net_suid)

# EDGES
for p, so in edges.items():
    print(f"🍄 {p} : {len(so)} triples")
    if p == "rdf:type":
        for [s, o] in so:
            nodes_uri[s]["rdf:type"] = o
            types.append(o)

    else:
        res = p4c.add_cy_edges(so, edge_type=p, directed=True, network=net_suid)

# EDGES LITERALS
for p, so in edges_literal.items():
    print(f"🍄 {p} : {len(so)} triples")
    p4c.add_cy_edges(so, edge_type=p, directed=True, network=net_suid)

################################################################################
# MAKE TABLES
################################################################################

data = pd.DataFrame(data={'id': nodes_names,
                          'label': [x + (("\nrdf:type :: " + nodes_uri[x]["rdf:type"]) if x in nodes_uri and "rdf:type" in nodes_uri[x] else "") for x in nodes_names]
                          })
p4c.load_table_data(data, data_key_column='id', table='node', table_key_column='name')

###############################################################################
# GLOBAL LAYOUT
###############################################################################

print("🐙", "set_node_label_bypass")
p4c.set_node_label_mapping('label', network=net_suid)
print("🐙", "set_node_width_bypass")
p4c.set_node_width_bypass(nodes_uri_names, [7.5 * max(
    9 + len(nodes_uri[x]["rdf:type"] if "rdf:type" in nodes_uri[x] else ""),
    len(x)
) for x in nodes_uri_names], network=net_suid)
p4c.set_node_width_bypass(nodes_literal_names, [7.5 * len(x) for x in nodes_literal_names], network=net_suid)
print("🐙", "set_node_color_bypass")
p4c.set_node_color_bypass(nodes_uri_names, new_colors='indigo', network=net_suid)
p4c.set_node_color_bypass(nodes_literal_names, new_colors='hotpink', network=net_suid)
print("🐙", "set_node_height_bypass")
p4c.set_node_height_bypass(nodes_uri_names, 50, network=net_suid)
print("🐙", "set_node_label_color_default")
p4c.set_node_label_color_default('white')
print("🐙", "layout_network")
p4c.layout_network(layout_name="force-directed", network=net_suid)
print("🐙", p4c.get_layout_names())
