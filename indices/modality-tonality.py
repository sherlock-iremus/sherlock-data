import argparse
from rdflib import Graph
import json

parser = argparse.ArgumentParser()
parser.add_argument("--inputrdf")
parser.add_argument("--outputjson")
args = parser.parse_args()

graph = Graph()
graph.parse(args.inputrdf)

baseIri = ''
query = """
SELECT ?s
WHERE {
    ?s rdf:type owl:Ontology
}
"""
bindings = graph.query(query)
for binding in bindings:
    baseIri = binding.s + '#'

rootclasses_query = """
SELECT ?owlClass
WHERE {
    ?owlClass a owl:Class .
    FILTER NOT EXISTS { ?owlClass rdfs:subClassOf ?b }
    FILTER (regex(str(?owlClass),"%s"))
}
""" % baseIri


def subclasses_query(class_iri):
    return """
    SELECT ?owlClass
    WHERE {
        ?owlClass rdfs:subClassOf <%s>
    }
    """ % class_iri


def get_subclasses(query):
    bindings = graph.query(query)
    subClasses = []

    for binding in bindings:
        iri = str(binding.owlClass)
        label = iri[len(baseIri):len(iri)]
        node = {"iri": iri, "label": label}
        subsubClasses = get_subclasses(subclasses_query(iri))
        if subsubClasses:
            node["subClasses"] = subsubClasses
        subClasses.append(node)
    
    return subClasses


ontology = {"iri": baseIri, "rootClasses": get_subclasses(rootclasses_query)}

with open(args.outputjson, 'w') as f:
    json.dump(ontology, f)
    print("Fichier JSON créé avec succès !")
