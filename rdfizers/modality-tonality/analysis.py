import argparse
from pprint import pprint
from typing import Literal
from rdflib import XSD, Graph, Literal, Namespace, RDF, RDFS, URIRef
from sherlockcachemanagement import Cache

################################################################################
# SETUP
################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("--analysis_ontology")
parser.add_argument("--cache")
parser.add_argument("--historical_models_dir")
parser.add_argument("--out_ttl")
parser.add_argument("--researcher_uuid")
args = parser.parse_args()

cache = Cache(args.cache)

MTNS = "http://modality-tonality.huma-num.fr/analysisOntology#"
crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
crmdig = Namespace('http://www.cidoc-crm.org/crmdig/')
lrmoo = Namespace('http://www.cidoc-crm.org/lrmoo/')
sherlock = Namespace('http://data-iremus.huma-num.fr/id/')
sherlockns = Namespace('http://data-iremus.huma-num.fr/ns/sherlock#')
zarlino1588 = Namespace("http://modality-tonality.huma-num.fr/Zarlino_1558#")

g_in = Graph()
g_in.bind("mtao", MTNS)
g_in.parse(args.analysis_ontology)

g_out = Graph()
g_out.bind("crm", str(crm))
g_out.bind("crmdig", str(crmdig))
g_out.bind("lrmoo", lrmoo)
g_out.bind("mtao", MTNS)
g_out.bind("sherlock", str(sherlock))
g_out.bind("sherlockns", str(sherlockns))
g_out.bind("zarlino1588", zarlino1588)

################################################################################
# PROCESS
################################################################################

analyses = g_in.query(f"SELECT * WHERE {{ ?s a <{MTNS}Analysis> }}")
for analysis in analyses:
    analysis_key = URIRef(analysis[0])

    origin = g_in.query(f"SELECT * WHERE {{ <{analysis_key}> <{MTNS}hasOrigin> ?o }}").bindings[0]['o']

    # Work
    work = g_in.query(f"SELECT * WHERE {{ ?work <{MTNS}hasAnalysis> <{analysis_key}> }}").bindings[0]['work']
    work_triples = g_in.query(f"SELECT * WHERE {{ <{work}> ?p ?o }}").bindings
    for binding in work_triples:
        if str(binding["p"]) == MTNS + "hasURL":
            work = sherlock[URIRef(cache.get_uuid(["works", binding["o"], "uuid"], True))]

    # Software

    pythonModuleName = g_in.query(f"SELECT * WHERE {{ <{origin}> <{MTNS}hasPythonModuleName> ?o }}").bindings[0]['o']
    pythonClassName = g_in.query(f"SELECT * WHERE {{ <{origin}> <{MTNS}hasPythonClassName> ?o }}").bindings[0]['o']
    pythonDefName = g_in.query(f"SELECT * WHERE {{ <{origin}> <{MTNS}hasPythonDefName> ?o }}").bindings[0]['o']
    software = URIRef(cache.get_uuid(["D14_software", pythonModuleName+'•'+pythonClassName+'•'+pythonDefName, "uuid"], True))
    g_out.add((software, RDF.type, crmdig["D14_Software"]))
    g_out.add((software, URIRef(MTNS+"hasPythonModuleName"), Literal(pythonModuleName)))
    g_out.add((software, URIRef(MTNS+"hasPythonClassName"), Literal(pythonClassName)))
    g_out.add((software, URIRef(MTNS+"hasPythonDefName"), Literal(pythonDefName)))

    # Analytical project

    analytical_project = URIRef(cache.get_uuid(["analyses", analysis_key, "E7", "uuid"], True))
    g_out.add((analytical_project, RDF.type, crm["E7_Activity"]))
    g_out.add((analytical_project, crm["P2_has_type"], URIRef("f122c08a-5084-4a94-80ed-019102976309")))  # E55 « Projet analytique »
    g_out.add((analytical_project, crm["P14_carried_out_by"], URIRef(args.researcher_uuid)))
    g_out.add((analytical_project, crm["P16_used_specific_object"], software))

    date = g_in.query(f"SELECT * WHERE {{ <{analysis_key}> <{MTNS}hasDate> ?o . }}").bindings[0]['o']
    E52 = URIRef(cache.get_uuid(["analyses", analysis_key, "E52" "uuid"], True))
    g_out.add((analytical_project, crm["P4_has_time-span"], E52))
    g_out.add((E52, RDF.type, crm["E52_Time-Span"]))
    g_out.add((E52, crm["P82b_end_of_the_end"], Literal(date, datatype=XSD.dateTime)))

    # Software execution

    software_execution = URIRef(cache.get_uuid(["analyses", analysis_key, "D10", "uuid"], True))
    g_out.add((software_execution, RDF.type, crmdig["D10_Software_Execution"]))
    g_out.add((software_execution, crmdig["L23_used_software_or_firmware"], software))
    # TODO g_out.add((software_execution, crmdig["L2_used_as_source"], ))
    # TODO g_out.add((software_execution, crmdig["L10_had_input"], ))
    # TODO g_out.add((software_execution, crmdig["L11_had_output"], ))

    software_date = g_in.query(f"SELECT * WHERE {{ <{origin}> <{MTNS}hasDate> ?o . }}").bindings[0]['o']
    software_E52 = URIRef(cache.get_uuid(["analyses", analysis_key, "software", "E52" "uuid"], True))
    g_out.add((software_execution, crm["P4_has_time-span"], software_E52))
    g_out.add((software_E52, RDF.type, crm["E52_Time-Span"]))
    g_out.add((software_E52, crm["P82b_end_of_the_end"], Literal(software_date, datatype=XSD.dateTime)))

    # Theoretical model

    theoretical_model_iri = URIRef(g_in.query(f"SELECT * WHERE {{ <{analysis_key}> <{MTNS}hasTheoreticalModel> ?tm . ?tm <{MTNS}hasIRI> ?iri }}").bindings[0]['iri'])
    theoretical_model_name = g_in.query(f"SELECT * WHERE {{ <{analysis_key}> <{MTNS}hasTheoreticalModel> ?tm . ?tm <{MTNS}hasName> ?name }}").bindings[0]['name']
    g_out.add((theoretical_model_iri, RDF.type, lrmoo["F2_Work"]))
    g_out.add((theoretical_model_iri, RDFS.label, Literal(theoretical_model_name)))
    g_out.add((theoretical_model_iri, crm["P2_has_type"], URIRef("ae6c2f18-c8ae-4fac-83c8-9486fd00db2c")))  # E55 « Traité théorique »
    g_out.add((analytical_project, crm["P33_used_specific_technique"], theoretical_model_iri))

    # Annotations

    annotations = g_in.query(f"SELECT * WHERE {{ <{analysis_key}> <{MTNS}hasAnalyticalObservation> ?ao . ?ao ?p ?a }}").bindings
    for a in annotations:
        annotation_body = a["a"]
        annotation_id = annotation_body.split("#")[-1]

        if str(a["p"]).startswith("http://modality-tonality.huma-num.fr/"):

            # Annotation body (P141)
            annotation_iri = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "uuid"], True))

            # E13
            e13 = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "e13", "uuid"], True))
            g_out.add((e13, RDF.type, crm["E13_Attribute_Assignment"]))
            g_out.add((software_execution, crm["P9_consists_of"], e13))
            g_out.add((e13, crm["P140_assigned_attribute_to"], work))
            g_out.add((e13, crm["P177_assigned_property_of_type"], a["p"]))
            g_out.add((e13, crm["P141_assigned"], annotation_iri))
            g_out.add((e13, sherlockns["has_document_context"], work))
            g_out.add((e13, crm["P33_used_specific_technique"], theoretical_model_iri))

            annotation_triples = g_in.query(f"SELECT * WHERE {{ <{annotation_body}> ?p ?o }}").bindings
            for t in annotation_triples:
                if (str(t["p"]).startswith("http://modality-tonality.huma-num.fr/") or str(t["o"]).startswith("http://modality-tonality.huma-num.fr/")) and str(t["p"]) != MTNS + "hasOrigin":
                    o = str(t["o"])
                    note_id = g_in.query(f"SELECT * WHERE {{ <{o}> a <http://modality-tonality.huma-num.fr/music21#Note> . <{o}> <http://modality-tonality.huma-num.fr/music21#id> ?note_id }}").bindings
                    if len(note_id) == 1:
                        g_out.add((annotation_iri, t["p"], URIRef(str(work)+"_"+note_id[0]["note_id"])))
                    else:
                        g_out.add((annotation_iri, t["p"], t["o"]))

################################################################################
# THAT'S ALL FOLKS
################################################################################

cache.bye()
g_out.serialize(format='turtle', destination=args.out_ttl, base=sherlock)
