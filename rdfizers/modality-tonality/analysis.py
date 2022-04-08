import argparse
from pprint import pprint
import sys
from typing import Literal
from rdflib import XSD, Graph, Literal, Namespace, RDF, RDFS, URIRef
from sherlockcachemanagement import Cache

################################################################################
# SETUP
################################################################################

# TODO passer le bon cache pour les notes & l'oeuvre
parser = argparse.ArgumentParser()
parser.add_argument("--analysis_ontology")
parser.add_argument("--cache")
parser.add_argument("--mei_cache")
parser.add_argument("--historical_models_dir")
parser.add_argument("--out_ttl")
parser.add_argument("--researcher_uuid")
args = parser.parse_args()

cache = Cache(args.cache)
mei_cache = Cache(args.mei_cache)

crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
crmdig = Namespace('http://www.cidoc-crm.org/crmdig/')
lrmoo = Namespace('http://www.cidoc-crm.org/lrmoo/')
sherlock = Namespace('http://data-iremus.huma-num.fr/id/')
sherlockns = Namespace('http://data-iremus.huma-num.fr/ns/sherlock#')
zarlino1588 = Namespace("http://modality-tonality.huma-num.fr/Zarlino_1558#")

g_in = Graph()
g_in.parse(args.analysis_ontology)
MTNS = ''
bindings = g_in.query("SELECT ?s WHERE { ?s rdf:type owl:Ontology }")
for binding in bindings:
    MTNS = str(binding.s + '#')
g_in.bind("mtao", MTNS)

M21NS = "http://modality-tonality.huma-num.fr/music21#"
g_out = Graph()
g_out.bind("crm", str(crm))
g_out.bind("crmdig", str(crmdig))
g_out.bind("lrmoo", lrmoo)
g_out.bind("music21", M21NS)
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

    # Work

    work = g_in.query(f"SELECT * WHERE {{ ?work <{MTNS}hasAnalysis> <{analysis_key}> }}").bindings[0]['work']
    work_triples = g_in.query(f"SELECT * WHERE {{ <{work}> ?p ?o }}").bindings
    for binding in work_triples:
        if str(binding["p"]) == MTNS + "hasURL":
            mei_file = str(binding["o"]).replace("https://raw.githubusercontent.com/guillotel-nothmann/", "").replace("/main", "")
            work = sherlock[URIRef(mei_cache.get_uuid([mei_file]))]

    # Software

    origin = g_in.query(f"SELECT * WHERE {{ <{analysis_key}> <{MTNS}hasOrigin> ?o }}").bindings[0]['o']
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

            if str(a["p"].split("#")[-1]) == "hasCadence":

                # Création de la sélection
                selection = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "selection", "uuid"], True))
                g_out.add((selection, RDF["type"], crm["E28_Conceptual_Object"]))
                g_out.add((selection, crm["P2_has_type"], sherlock["9d0388cb-a178-46b2-b047-b5a98f7bdf0b"]))

                # Création de l'entité analytique
                analytical_entity = URIRef(cache.get_uuid(["analyses", analysis_key, "analytical_entities", annotation_id, "uuid"], True))

                # Création de l'E13 reliant la sélection à l'entité analytique
                e13 = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "e13", "uuid"], True))
                g_out.add((e13, RDF.type, crm["E13_Attribute_Assignment"]))
                g_out.add((e13, crm["P140_assigned_attribute_to"], selection))
                g_out.add((e13, crm["P177_assigned_property_of_type"], a["p"]))
                g_out.add((e13, crm["P141_assigned"], analytical_entity))
                g_out.add((e13, sherlockns["has_document_context"], work))
                g_out.add((e13, crm["P33_used_specific_technique"], theoretical_model_iri))
                # TODO P14
                # TODO P4

                # Recherche de tous les prédicats de l'entité anlytique
                po_list = g_in.query(f"SELECT * WHERE {{ <{annotation_body}> ?p ?o }}").bindings
                for po in po_list:
                    if str(po["p"]) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                        if str(po["o"]).startswith("http://modality-tonality.huma-num.fr/"):
                            e13 = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "e13_types", po["o"].split("/")[-1], "uuid"], True))
                            g_out.add((e13, RDF.type, crm["E13_Attribute_Assignement"]))
                            g_out.add((e13, crm["P140_assigned_attribute_to"], analytical_entity))
                            g_out.add((e13, crm["P177_assigned_property_of_type"], RDF.type))
                            g_out.add((e13, crm["P141_assigned"], URIRef(po["o"])))
                            g_out.add((e13, sherlockns["has_document_context"], work))
                            g_out.add((e13, crm["P33_used_specific_technique"], theoretical_model_iri))
                    else:
                        # TODO http://modality-tonality.huma-num.fr/analysisOntology#hasOrigin
                        # modéliser ça avec des D14 (software) P106 D14 (fonction)
                        if str(po["p"]) != "http://modality-tonality.huma-num.fr/analysisOntology#hasOrigin":
                            
                            e13 = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "e13_p", po["p"].split("/")[-1], "uuid"], True))
                            g_out.add((e13, RDF.type, crm["E13_Attribute_Assignement"]))
                            g_out.add((e13, crm["P140_assigned_attribute_to"], analytical_entity))
                            g_out.add((e13, crm["P177_assigned_property_of_type"], URIRef(po["p"])))
                            # TODO note_iri = URIRef(work.split("/")[-1] + "_" + note["id"])
                            g_out.add((e13, crm["P141_assigned"], None))  # TODO mettre la note
                            g_out.add((e13, sherlockns["has_document_context"], work))
                            g_out.add((e13, crm["P33_used_specific_technique"], theoretical_model_iri))

                # notes = g_in.query(f"SELECT * WHERE {{ <{a['a']}> ?p ?a . ?a a <{M21NS+'Note'}> . ?a <{M21NS+'id'}> ?id }}").bindings
                # for note in notes:
                #     
                #     # Ajout de la note à la sélection
                #     g_out.add((selection, crm["P106_is_composed_of"], note_iri))
                #     # Création de la cadence

                #     note_e13_iri = URIRef(cache.get_uuid(["analyses", analysis_key, "annotations", annotation_id, "notes", note_iri, "e13", "uuid"], True))
            else:
                pass
                # print(a["p"])

            # annotation_triples = g_in.query(f"SELECT * WHERE {{ <{annotation_body}> ?p ?o }}").bindings
            # for t in annotation_triples:
            #     if (str(t["p"]).startswith("http://modality-tonality.huma-num.fr/") or str(t["o"]).startswith("http://modality-tonality.huma-num.fr/")) and str(t["p"]) != MTNS + "hasOrigin":
            #         o = str(t["o"])
            #         note_id = g_in.query(
            #             f"SELECT * WHERE {{ <{o}> a <http://modality-tonality.huma-num.fr/music21#Note> . <{o}> <http://modality-tonality.huma-num.fr/music21#id> ?note_id }}").bindings
            #         if len(note_id) == 1:
            #             g_out.add((annotation_iri, t["p"], URIRef(str(work)+"_"+note_id[0]["note_id"])))
            #         else:
            #             g_out.add((annotation_iri, t["p"], t["o"]))

################################################################################
# THAT'S ALL FOLKS
################################################################################

cache.bye()
g_out.serialize(format='turtle', destination=args.out_ttl, base=sherlock)
