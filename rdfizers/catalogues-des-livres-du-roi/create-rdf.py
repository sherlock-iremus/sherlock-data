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

data = {}

with open(args.json_file, 'r') as f:
    data = json.load(f)

print("LIVRETS")

for k, v in data["livrets"].items():
    
    # Item
    F5_uri = she(v["sherlock_uuid"])
    t(F5_uri, a, lrm("F5_Item"))
    if v["Cote 1"] != None:
        t(F5_uri, crm("P1_is_identified_by"), l(v["Cote 1"]))
    if v["Cote 2"] != None:
        t(F5_uri, crm("P1_is_identified_by"), l(v["Cote 2"]))
    #if v["Lieu de conservation 1"] != None:
    #    t(F5_uri, crm(""), l(v["Lieu de conservation 1"]))
    if v["Remarques sur les exemplaires"] != None:
        t(F5_uri, crm("P3_has_note"), l(v["Remarques sur les exemplaires"]))
    

#            "Adresse": null,
#            "Description matérielle": "In-4°, [2 bl.]-[2]-34-[2 bl.] p. ; 24 x 17,5 cm. - Sig. [ ]²-A-D⁴ E². ",
#            "Description de la reliure": "Reliure en maroquin olive aux armes royales de France (OHR 2494, n° 8), encadrement d'un triple filet, petits soleils aux angles ; dos à 5 nerfs, entrenerfs marqués d'une fleur de lis. Tranches dorées. Gardes de papier marbré peigné.",
#            "Lieu de conservation 1": "F-Pnlr",
#            
#            "Lieu de conservation 2": null,
#            
    
    # Production de l'item
    F32_uri = she(cache.get_uuid(["livrets", k, "F32", "uuid"], True))
    t(F32_uri, a, lrm("F32_Carrier_Production_Event"))
    t(F32_uri, lrm("R28_produced"), F5_uri)

    # Manifestation
    F3_uri = she(cache.get_uuid(["livrets", k, "F3", "uuid"], True))
    t(F3_uri, a, lrm("F3_Manifestation"))
    t(F5_uri, lrm("R7_is_materialization_of"), F3_uri)
    t(F32_uri, lrm("R27_materialized"), F3_uri)
    if v["Remarques sur l'édition"] != None:
        t(F5_uri, crm("P3_has_note"), l(v["Remarques sur l'édition"]))

    # Creation de la manifestation
    F30_uri = she(cache.get_uuid(["livrets", k, "F30", "uuid"], True))
    t(F30_uri, a, lrm("F30_Manifestation_Creation"))
    t(F30_uri, lrm("R24_created"), F3_uri)
    E52_uri = she(cache.get_uuid(["livrets", k, "F30", "E52", "uuid"], True))
    date = v["Année normalisée"]
    t(E52_uri, crm("P82_at_some_time_within"), l(f"{date}-01T00:00:00Z", datatype=XSD.dateTime))
    t(F30_uri, crm("P4_has_time-span"), E52_uri)

    # Expression
    F2_uri = she(cache.get_uuid(["livrets", k, "F2", "uuid"], True))
    t(F2_uri, a, lrm("F2_Expression"))
    t(F2_uri, crm("P1_is_identified_by"), l(k))
    #"titre_forgé": "1666–
    t(F3_uri, lrm("R4_embodies"), F2_uri)
    E35_uri = she(cache.get_uuid(["livrets", k, "F2", "E35", "uuid"], True))
    t(E35_uri, a, crm("E35_Title"))
    t(E35_uri, RDFS.label, l(v["Titre"]))
    t(F2_uri, crm("P102_has_title"), E35_uri)

    # Creation de l'expression
    F28_uri = she(cache.get_uuid(["livrets", k, "F28", "uuid"], True))
    t(F28_uri, a, lrm("F28_Expression_Creation"))
    t(F28_uri, lrm("R17_created"), F2_uri)

    # Photographie de l'item
    def create_photo(photographie, legende):
        if v[photographie] != None:
            E65_uri = she(cache.get_uuid(["livrets", k, photographie, "E65", "uuid"], True))
            t(E65_uri, a, crm("E65_Creation"))
            t(E65_uri, crm("P16_used_specific_object"), F5_uri)
            t(E65_uri, crm("P14_carried_out_by"), she("710d0c6e-48ed-47b6-b209-00520636d7be"))
            E36_uri = she(cache.get_uuid(["livrets", k, photographie, "E65", "E36", "uuid"], True))
            t(E36_uri, a, crm("E36_Visual_Item"))
            t(E65_uri, crm("P94_has_created"), E36_uri)
            if v[legende] != None:
                t(E36_uri, crm("P102_has_title"), l(v[legende]))  
    
    create_photo("Photo 1", "Légende 1")
    create_photo("Photo 2", "Légende 2")

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

    
    # Ne pas oublier que la photographie représente un E18

#print("MOTETS")

for k, v in data["motets"].items():
    pass

# Sérialisation du graphe
save_graph(args.ttl)

cache.bye()