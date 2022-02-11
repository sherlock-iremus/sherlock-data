import argparse
import glob
from rdflib import Graph, Namespace

parser = argparse.ArgumentParser()
parser.add_argument("--analysis_ontology")
parser.add_argument("--historical_models_dir")
parser.add_argument("--out_ttl")
args = parser.parse_args()

g = Graph()
g.bind("ao", "http://modality-tonality.huma-num.fr/analysisOntology#")
g.parse(args.analysis_ontology)

# Identify Web Portal properties

q = """
SELECT *
WHERE { ?web_portal_property ao:webPortalProperty true . }
"""
qres = g.query(q)
web_portal_properties = [row.web_portal_property for row in qres]

# Load historical models

for ho in glob.glob(args.historical_models_dir+'/*.owl'):
    print(ho)
    hog = Graph()
    hog.parse(ho)
    qres = hog.query("SELECT ?g (COUNT(*) as ?triples) WHERE { ?s ?p ?o }")
    print("    ", int([a for a in qres][0].triples))
    for wpp in web_portal_properties:
        qres = hog.query("SELECT * WHERE { ?s <" + str(wpp) + "> ?o }")
        print("    ", "SELECT * WHERE { ?s <" + str(wpp) + "> ?o }")
        for r in qres:
            print("        ", str(r.s), str(r.o))
