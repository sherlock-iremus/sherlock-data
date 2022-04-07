import argparse
import os
import sys
import yaml
import json
from pprint import pprint
from sherlockcachemanagement import Cache

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--json_file")
parser.add_argument("--ttl")
parser.add_argument("--cache")
args = parser.parse_args()

# Cache
cache = Cache(args.cache)

# Helpers RDF
sys.path.append(os.path.abspath(os.path.join('./rdfizers/', '')))
from helpers_rdf import *

# Graphe RDF
init_graph()

# Fonctions
def make_E13(path, subject, predicate, object):
    E13_uri = she(cache.get_uuid(path, True))
    t(E13_uri, a, crm("E13_Attribute_Assignement"))
    t(E13_uri, crm("P14_carried_out_by"), she(
        "710d0c6e-48ed-47b6-b209-00520636d7be"))
    t(E13_uri, crm("P140_assigned_attribute_to"), subject)
    t(E13_uri, crm("P141_assigned"), object)
    t(E13_uri, crm("P177_assigned_property_type"), predicate)

# Lecture du fichier JSON
data = {}

with open(args.json_file, 'r') as f:
    data = json.load(f)

print("LIVRETS")

for k, v in data["livrets"].items():

    # Expression
    F2_uri = she(v["sherlock_uuid"])
    t(F2_uri, a, lrm("F2_Expression"))
    t(F2_uri, crm("P2_has_type"), she("7dfb4b03-b284-48bb-8958-786388c0c489"))
    t(F2_uri, crm("P1_is_identified_by"), l(k))
    #"titre_forgé": "1666–
    E35_uri = she(cache.get_uuid(["livrets", k, "F2", "E35", "uuid"], True))
    t(E35_uri, a, crm("E35_Title"))
    t(E35_uri, RDFS.label, l(v["Titre"]))
    t(F2_uri, crm("P102_has_title"), E35_uri)

    # Creation de l'expression
    F28_uri = she(cache.get_uuid(["livrets", k, "F28", "uuid"], True))
    t(F28_uri, a, lrm("F28_Expression_Creation"))
    t(F28_uri, lrm("R17_created"), F2_uri)

    # Manifestation
    F3_uri = she(cache.get_uuid(["livrets", k, "F3", "uuid"], True))
    t(F3_uri, a, lrm("F3_Manifestation"))
    t(F3_uri, lrm("R4_embodies"), F2_uri)
    if v["Remarques sur l'édition"] != None:
        make_E13(["livrets", k, "F3", "E13 Remarques sur l'édition"], F3_uri, she("df01a210-394a-47b1-b7a4-74c700f7f675"), l(v["Remarques sur l'édition"]))
    # TODO Adresse

    # Creation de la manifestation
    F30_uri = she(cache.get_uuid(["livrets", k, "F30", "uuid"], True))
    t(F30_uri, a, lrm("F30_Manifestation_Creation"))
    t(F30_uri, lrm("R24_created"), F3_uri)
    E52_uri = she(cache.get_uuid(["livrets", k, "F30", "E52", "uuid"], True))
    date = v["Année normalisée"]
    t(E52_uri, crm("P82b_end_of_the_end"), l(f"{date}-01T00:00:00Z", datatype=XSD.dateTime))
    t(F30_uri, crm("P4_has_time-span"), E52_uri)
    # TODO Carried out by E39?
 
    # Exemplaires : création d'un F5/E78 par exemplaire
    def F5_info(n, item):
        t(item, a, lrm("F5_Item"))
        t(item, a, crm("E78_Curated_Holding"))
        t(item, lrm("R7_is_materialization_of"), F3_uri)

        # Production de l'item
        F32_uri = she(cache.get_uuid(["livrets", k, "examplaires", n, "F32"], True))
        t(F32_uri, a, lrm("F32_Carrier_Production_Event"))
        t(F32_uri, lrm("R28_produced"), item)
        t(F32_uri, lrm("R27_materialized"), F3_uri)

        if v["Description matérielle"] != None:
            make_E13(["livrets", k, "examplaires", n, "E13 Description matérielle"], item, she("0f475362-c20e-4172-8d96-a55855b15ac6"), l(v["Description matérielle"]))
        if v["Description de la reliure"] != None:
            make_E13(["livrets", k, "examplaires", n, "E13 Description de la reliure"], item, she("fc375ac0-dbda-4a02-9644-b3e5e020b30d"), l(v["Description matérielle"]))
        if v["Remarques sur les exemplaires"] != None:
            make_E13(["livrets", k, "examplaires", n, "E13 Remarques sur les exemplaires"], item, she("7432ae29-7f76-4b3e-83eb-c548b874a480"), l(v["Remarques sur les exemplaires"]))

    if v["Cote 1"] != None:
        F5_uri = she(cache.get_uuid(["livrets", k, "examplaires", "1", "uuid"], True))
        F5_info(1, F5_uri)
        t(F5_uri, crm("P1_is_identified_by"), l(v["Cote 1"]))        
        if v["Lieu de conservation 1"] != None:
            try:
                E39_uri = she(cache.get_uuid(["lieux_de_conservation", v["Lieu de conservation 1"], "uuid"]))
            except:
                E39_uri = she(cache.get_uuid(["lieux_de_conservation", v["Lieu de conservation 1"], "uuid"], True))
            t(E39_uri, a, crm("E39_Actor"))
            t(F5_uri, crm("P109_has_current_or_former_curator"), E39_uri)

    
    if v["Cote 2"] != None:
        F5_uri = she(cache.get_uuid(["livrets", k, "examplaire", "2", "uuid"], True))
        F5_info(2, F5_uri)
        t(F5_uri, crm("P1_is_identified_by"), l(v["Cote 2"]))
        if v["Lieu de conservation 1"] != None:
            try:
                E39_uri = she(cache.get_uuid(["lieux_de_conservation", v["Lieu de conservation 1"], "uuid"]))
            except:
                E39_uri = she(cache.get_uuid(["lieux_de_conservation", v["Lieu de conservation 1"], "uuid"], True))
            t(E39_uri, a, crm("E39_Actor"))
            t(F5_uri, crm("P109_has_current_or_former_curator"), E39_uri)   

    # Photographie de l'item
    # def create_photo(photographie, legende):
    #     if v[photographie] != None:
    #         E65_uri = she(cache.get_uuid(["livrets", k, photographie, "E65", "uuid"], True))
    #         t(E65_uri, a, crm("E65_Creation"))
    #         t(E65_uri, crm("P16_used_specific_object"), F5_uri)
    #         t(E65_uri, crm("P14_carried_out_by"), she("710d0c6e-48ed-47b6-b209-00520636d7be"))
    #         E36_uri = she(cache.get_uuid(["livrets", k, photographie, "E65", "E36", "uuid"], True))
    #         t(E36_uri, a, crm("E36_Visual_Item"))
    #         t(E65_uri, crm("P94_has_created"), E36_uri)
    #         if v[legende] != None:
    #             t(E36_uri, crm("P102_has_title"), l(v[legende]))  
    
    # create_photo("Photo 1", "Légende 1")
    # create_photo("Photo 2", "Légende 2")

    # Les sections du livret
    for p, n  in v["parties"].items():
        pages = []
        for motet in n["instanciations"]:
            pages.append(motet["Page"])
            F2_section_uri = she(cache.get_uuid(["livrets", k, "F2", p, "uuid"], True))
            t(F28_uri, a, lrm("F2_Expression"))
            t(F2_section_uri, crm("P2_has_type"), she("074edf95-c72f-45a0-80c9-d9140b5bd7cd"))
            t(F2_uri, crm("P165_has_component"), F2_section_uri) 

            # Contenu de la section
            E33_uri = she(cache.get_uuid(["livrets", k, "F2", p, "E33", "uuid"], True))
            t(E33_uri, a, crm("E33_Linguistic_Object"))
            t(F2_section_uri, crm("P165_incorporates"), E33_uri)
            # Référence au motet
            t(E33_uri, crm("P67_refers_to"), she(motet["motet_sherlock_uuid"]))

            # Matérialité de la section (pages)
            E18_uri = she(cache.get_uuid(["livrets", k, "F2", p, "E18", "uuid"], True))
            t(E18_uri, a, crm("E18_Physical_Object"))
            t(E18_uri, crm("P2_has_type"), she("f1d79248-5147-4b6a-ac4f-6fc727a2c16a"))
            t(E18_uri, crm("P128_carries"), E33_uri)
            #t(E18_uri, fab("has_ending_page"))
            #t(E18_uri, fab("has_starting_page"))


print("MOTETS")

for k, v in data["motets"].items():
    pass

# Sérialisation du graphe
save_graph(args.ttl)

cache.bye()