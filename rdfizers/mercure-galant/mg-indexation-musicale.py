import argparse
from openpyxl import load_workbook
import sys, os
from pprint import pprint

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
from helpers_rdf import *
from sherlockcachemanagement import Cache
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

######################################################################################
# CACHES
######################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("--xlsx")
parser.add_argument("--ttl")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")
args = parser.parse_args()

cache = Cache(args.cache)
cache_tei = Cache(args.cache_tei)

######################################################################################
# INITIALISATION DU GRAPHE
######################################################################################

g = Graph()

crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmdig_ns = Namespace("http://www.ics.forth.gr/isl/CRMdig/")
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
lrmoo_ns = Namespace("http://www.cidoc-crm.org/lrmoo/")
sdt_ns = Namespace("http://data-iremus.huma-num.fr/datatypes/")
sherlock_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

g.bind("crm", crm_ns)
g.bind("dcterms", DCTERMS)
g.bind("lrm", lrmoo_ns)
g.bind("sdt", sdt_ns)
g.bind("skos", SKOS)
g.bind("crmdig", crmdig_ns)
g.bind("she_ns", sherlock_ns)
g.bind("she", iremus_ns)

######################################################################################
# FONCTIONS RDF
######################################################################################

a = RDF.type

def crm(x):
    return crm_ns[x]

def crmdig(x):
    return crmdig_ns[x]

def lrm(x):
    return lrmoo_ns[x]

def she(x):
    return iremus_ns[x]

def she_ns(x):
    return sherlock_ns[x]

def t(s, p, o):
    g.add((s, p, o))


def make_E13(path, subject, predicate, object):
    E13_uri = she(cache.get_uuid(path, True))
    t(E13_uri, a, crm("E13_Attribute_Assignement"))
    t(E13_uri, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
    t(E13_uri, crm("P140_assigned_attribute_to"), subject)
    t(E13_uri, crm("P141_assigned"), object)
    t(E13_uri, crm("P177_assigned_property_type"), predicate)


#######################################################################################
# RECUPERATION DES DONNEES
#######################################################################################

# Fichier Excel
sheet = load_workbook(args.xlsx).active

rows = get_xlsx_sheet_rows_as_dicts(sheet)

for row in rows[1:]:
    id = row["id"]

    #------------------------------------------------------------------------------------
    #  Air (F2)
    #------------------------------------------------------------------------------------

    F2_air_uuid = she(cache.get_uuid([id, "F2 air", "uuid"], True))
    t(F2_air_uuid, a, lrm("F2_Expression"))
    # Incipit textuel principal
    F2_air_incipit_principal = she(cache.get_uuid([id, "F2 air", "incipit textuel (E41)", "principal", "uuid"], True))
    t(F2_air_incipit_principal, a, crm("E41_Appellation"))
    t(F2_air_incipit_principal, a, crm("E33_Linguistic_Object"))
    t(F2_air_uuid, crm("P1_is_identified_by"), F2_air_incipit_principal)
    t(F2_air_incipit_principal, crm("P2_has_type"), she("5891daa1-81be-494a-8bf9-9055574f0530"))

    make_E13([id, "F2 air", "incipit textuel (E41)", "principal", "E13"], F2_air_incipit_principal, crm("P190_has_symbolic_content"), l(row["Incipit principal ou premier"]))    

    
    #crm:P1_is_identified_by <b1fc3882-ec63-438c-8f69-3d97f5f2b1de>;
    #crm:P2_has_type <a9d51926-c0ff-4304-b49d-9a18aff02d7e>; # pièce musicale
    #lrm:R75_incorporates <066f3c51-0671-479d-946f-ceb656e88f0b>; 
    ##E13 crm:P3_has_note "sol mineur, 3, forme binaire (les barres de mesure ont été omises)." ; # Colonne AA
    ##E13 P177 "genre musical" (E55) P140 E55 (transformer les concepts en E55) ;
    ## E13 forme musicale (créer E32)


#######################################################################################
# CREATION DU GRAPHE ET DU CACHE
#######################################################################################

cache.bye()

serialization = g.serialize(format="turtle", base="http://data-iremus.huma-num.fr/id/")
with open(args.ttl, "w+") as f:
    f.write(serialization)
