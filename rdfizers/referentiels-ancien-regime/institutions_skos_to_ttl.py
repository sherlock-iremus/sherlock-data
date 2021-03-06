import argparse
import hashlib
import os
from pathlib import Path, PurePath
from types import prepare_class
from rdflib import Graph, Literal, Namespace, DCTERMS, RDF, RDFS, SKOS, URIRef, URIRef as u, Literal as l
import re
import sys
import uuid
import yaml
from sherlockcachemanagement import Cache

parser = argparse.ArgumentParser()
parser.add_argument("--inputrdf")
parser.add_argument("--output_ttl")
parser.add_argument("--cache_institutions")
parser.add_argument("--cache_tei")
args = parser.parse_args()

# CACHE

cache_tei = Cache(args.cache_tei)
cache_institutions = Cache(args.cache_institutions)

################################################################################
# Initialisation des graphes
################################################################################

input_graph = Graph()
input_graph.load(args.inputrdf)

output_graph = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmdig_ns = Namespace("http://www.ics.forth.gr/isl/CRMdig/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
sherlock_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")
lrmoo_ns = Namespace("http://www.cidoc-crm.org/lrmoo/")
sdt_ns = Namespace("http://data-iremus.huma-num.fr/datatypes/")

output_graph.bind("crm", crm_ns)
output_graph.bind("crmdig", crmdig_ns)
output_graph.bind("dcterms", DCTERMS)
output_graph.bind("lrmoo", lrmoo_ns)
output_graph.bind("sdt", sdt_ns)
output_graph.bind("skos", SKOS)
output_graph.bind("she_ns", sherlock_ns)

a = RDF.type


def crm(x):
    return URIRef(crm_ns[x])


def dig(x):
    return URIRef(crmdig_ns[x])


def lrm(x):
    return URIRef(lrmoo_ns[x])


def she(x):
    return URIRef(iremus_ns[x])


def she_ns(x):
    return URIRef(sherlock_ns[x])


def t(s, p, o):
    output_graph.add((s, p, o))


def ro(s, p):
    try:
        return list(input_graph.objects(s, p))[0]
    except:
        return None


def ro_list(s, p):
    try:
        return list(input_graph.objects(s, p))
    except:
        return None

####################################################################################
# DONNEES STATIQUES
####################################################################################


indexation_regexp = r"MG-[0-9]{4}-[0-9]{2}[a-zA-Z]?_[0-9]{1,3}[a-zA-Z]?"
indexation_regexp_livraison = r"MG-[0-9]{4}-[0-9]{2}[a-zA-Z]?"

E32_noms_instit_corpo_uri = URIRef(iremus_ns["8a29e857-3faf-49f1-969b-91572e77218e"])
t(E32_noms_instit_corpo_uri, a, crm("E32_Authority_Document"))
t(E32_noms_instit_corpo_uri, crm("P1_is_identified_by"), Literal("Noms d'institutions et de corporations"))

###########################################################################################################
## INSTITUTIONS
###########################################################################################################

for opentheso_institution_uri, p, o in input_graph.triples((None, RDF.type, SKOS.Concept)):
    identifier = ro(opentheso_institution_uri, DCTERMS.identifier)
    E74_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "uuid"], True))
    E41_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "E41"], True))
    t(E74_uri, a, crm("E74_Group"))
    t(E32_noms_instit_corpo_uri, crm("P71_lists"), E74_uri)
    t(E74_uri, crm("P1_is_identified_by"), E41_uri)
    t(E41_uri, a, crm("E41_Appellation"))
    t(E41_uri, crm("P2_has_type"), SKOS.prefLabel)
    t(E41_uri, RDFS.label, ro(opentheso_institution_uri, SKOS.prefLabel))
    altLabels = ro_list(opentheso_institution_uri, SKOS.altLabel)
    if len(altLabels) > 0:
        for altLabel in altLabels:
            E41_alt_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "E41_alt", altLabel], True))
            t(E41_alt_uri, a, crm("E41_Appellation"))
            t(E41_alt_uri, RDFS.label, altLabel)
            t(E74_uri, crm("P1_is_identified_by"), E41_alt_uri)
            t(E41_alt_uri, crm("P2_has_type"), SKOS.altLabel)

    t(E74_uri, DCTERMS.created, ro(opentheso_institution_uri, DCTERMS.created))
    t(E74_uri, DCTERMS.modified, ro(opentheso_institution_uri, DCTERMS.modified))

    def process_note(p):
        values = ro_list(opentheso_institution_uri, p)
        for v in values:
            if "##id##" in v:
                v = v.split("##id##")
                for v in v:
                    if v:
                        m = re.search(indexation_regexp, v)
                        m_livraison = re.search(indexation_regexp_livraison, v)
                        if m:
                            clef_mercure_livraison = m_livraison.group()[3:]
                            clef_mercure_article = m.group()[3:]
                            try:
                                F2_article_uri = she(cache_tei.get_uuid(["Corpus", "Livraisons", clef_mercure_livraison, "Expression TEI", "Articles", clef_mercure_article, "F2"]))
                                E13_index_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "indexation", "E13"], True))
                                t(E13_index_uri, a, crm("E13_Attribute_Assignement"))
                                t(E13_index_uri, DCTERMS.created, ro(opentheso_institution_uri, DCTERMS.created))
                                t(E13_index_uri, crm("P14_carried_out_by"),
                                  she("899e29f6-43d7-4a98-8c39-229bb20d23b2"))
                                t(E13_index_uri, crm("P14_carried_out_by"),
                                  she("82476bac-cd8a-4bdc-a695-cf90444c9432"))
                                t(E13_index_uri, crm("P140_assigned_attribute_to"), F2_article_uri)
                                t(E13_index_uri, crm("P141_assigned"), E74_uri)
                                t(E13_index_uri, crm("P177_assigned_property_type"), crm("P67_refers_to"))

                            except:
                                print(identifier, ": l'article", clef_mercure_article, "n'existe pas")

            elif "##" in v:
                v = v.split("##")
                for v in v:
                    if v:
                        m = re.search(indexation_regexp, v)
                        m_livraison = re.search(indexation_regexp_livraison, v)
                        if m:
                            clef_mercure_livraison = m_livraison.group()[3:]
                            clef_mercure_article = m.group()[3:]
                            try:
                                F2_article_uri = she(cache_tei.get_uuid(
                                    ["Corpus", "Livraisons", clef_mercure_livraison, "Expression TEI", "Articles",
                                     clef_mercure_article, "F2"]))
                                E13_index_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "indexation", "E13"], True))
                                t(E13_index_uri, a, crm("E13_Attribute_Assignement"))
                                t(E13_index_uri, DCTERMS.created, ro(opentheso_institution_uri, DCTERMS.created))
                                t(E13_index_uri, crm("P14_carried_out_by"),
                                  she("899e29f6-43d7-4a98-8c39-229bb20d23b2"))
                                t(E13_index_uri, crm("P14_carried_out_by"),
                                  she("82476bac-cd8a-4bdc-a695-cf90444c9432"))
                                t(E13_index_uri, crm("P140_assigned_attribute_to"), F2_article_uri)
                                t(E13_index_uri, crm("P141_assigned"), E74_uri)
                                t(E13_index_uri, crm("P177_assigned_property_type"), crm("P67_refers_to"))

                            except:
                                print(identifier, ": l'article", clef_mercure_article, "n'existe pas")

            else:
                note_sha1_object = hashlib.sha1(v.encode())
                note_sha1 = note_sha1_object.hexdigest()
                E13_note_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "note", "E13"], True))
                t(E13_note_uri, a, crm("E13_Attribute_Assignement"))
                t(E13_note_uri, DCTERMS.created, ro(opentheso_institution_uri, DCTERMS.created))
                t(E13_note_uri, crm("P14_carried_out_by"), she("899e29f6-43d7-4a98-8c39-229bb20d23b2"))
                t(E13_note_uri, crm("P14_carried_out_by"),
                  she("82476bac-cd8a-4bdc-a695-cf90444c9432"))
                t(E13_note_uri, crm("P140_assigned_attribute_to"), E74_uri)
                note_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "note", note_sha1], True))
                t(note_uri, RDFS.label, Literal(v))
                t(E13_note_uri, crm("P141_assigned"), note_uri)
                t(E13_note_uri, crm("P177_assigned_property_type"), crm("P3_has_note"))

    for note in [SKOS.note]:
        process_note(note)

    narrower = ro(opentheso_institution_uri, SKOS.narrower)
    if narrower:
        identifier = ro(narrower, DCTERMS.identifier)
        E74_narrower_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "uuid"], True))
        t(E74_uri, crm("P107_has_current_or_former_member"), E74_narrower_uri)

    broader = ro(opentheso_institution_uri, SKOS.broader)
    if broader:
        identifier = ro(broader, DCTERMS.identifier)
        E74_broader_uri = she(cache_institutions.get_uuid(["institutions et corporations", identifier, "uuid"], True))
        t(E74_broader_uri, crm("P107_has_current_or_former_member"), E74_uri)

    exactMatches = ro_list(opentheso_institution_uri, SKOS.exactMatch)
    for exactMatch in exactMatches:
        if exactMatch == "https://opentheso3.mom.fr/opentheso3/index.xhtml":
            continue
        t(E74_uri, SKOS.exactMatch, exactMatch)

serialization = output_graph.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.output_ttl, "w+") as f:
    f.write(serialization)

cache_institutions.bye()