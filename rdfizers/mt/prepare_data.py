import argparse
import glob
from rdflib import Graph, Namespace

parser = argparse.ArgumentParser()
parser.add_argument("--analysis_ontology")
parser.add_argument("--historical_models_dir")
parser.add_argument("--out_webportal_ttl")
parser.add_argument("--out_skolemized")
args = parser.parse_args()

g = Graph()
g.bind("ao", "http://modality-tonality.huma-num.fr/analysisOntology#")
g.parse(args.analysis_ontology)


for ho in glob.glob(args.historical_models_dir+'/*.owl'):
    print(ho)
