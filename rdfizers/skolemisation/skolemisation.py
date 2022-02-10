import argparse
from rdflib import ConjunctiveGraph

parser = argparse.ArgumentParser()
parser.add_argument("--inowl")
parser.add_argument("--query")
parser.add_argument("--outowl")
parser.add_argument("--base")
args = parser.parse_args()

g = ConjunctiveGraph()
g.parse(args.inowl, format='application/rdf+xml')

with open(args.query, 'r') as file:
    q = file.read()
    g.update(q)

g.serialize(destination=args.outowl, format='application/rdf+xml', base=args.base)
