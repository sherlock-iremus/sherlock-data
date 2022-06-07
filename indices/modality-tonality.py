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
SELECT ?s
WHERE {
    ?s a owl:Class .
    FILTER NOT EXISTS { ?s rdfs:subClassOf ?o }
    FILTER (regex(str(?s),"%s"))
}
""" % baseIri

rootproperties_query = """
SELECT ?s
WHERE {
    ?s a owl:ObjectProperty .
    { FILTER NOT EXISTS { ?s rdfs:subPropertyOf ?o }}
    UNION
    { ?s rdfs:subPropertyOf <http://www.w3.org/2002/07/owl#topObjectProperty>}
}
""" 

def class_children_query(class_iri):
    return """
    SELECT ?s
    WHERE {
        ?s rdfs:subClassOf <%s>
    }
    """ % class_iri

def property_children_query(property_iri):
    return """
    SELECT ?s
    WHERE {
        ?s rdfs:subPropertyOf <%s>
    }
    """ % property_iri

def get_children(query, owl_type):
    bindings = graph.query(query)
    children = []

    for binding in bindings:
        iri = str(binding.s)
        label = iri[len(baseIri):len(iri)]
        node = {"iri": iri, "label": label}
        if owl_type == "owlClass":
            descendants = get_children(class_children_query(iri), "owlClass")
        if owl_type == "owlObjectProperty":
            descendants = get_children(property_children_query(iri), "owlObjectProperty")
        if descendants:
            node["children"] = descendants
        children.append(node)
    
    return children


ontology = {"iri": baseIri}
ontology["concepts"] = get_children(rootclasses_query, "owlClass")
ontology["properties"] = get_children(rootproperties_query, "owlObjectProperty")


with open(args.outputjson, 'w') as f:
    json.dump(ontology, f)
    print("Fichier JSON créé avec succès !")
