import helpers_excel
from directus_graphql_helpers import graphql_query
from sherlockcachemanagement import Cache
import argparse
import json
from pprint import pprint
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
import re
import requests
from slugify import slugify
import uuid
import yaml

# Data constants

INDEXATION_ESTAMPE_ANALYTICAL_PROJECT_UUID = "756aa164-0cde-46ac-bc3a-a0ea83a08e2d"
EQUIPE_MERCURE_GALANT_UUID = "684b4c1a-be76-474c-810e-0f5984b47921"
ESTAMPE_MG_E55_UUID = "1317e1ac-50c8-4b97-9eac-c4d902b7da10"
IDENTIFIANT_IIIF_3_E55_UUID = "19073c4a-0ef7-4ac4-a51a-e0810a596773"
IDENTIFIANT_GALLICA_E55_UUID = "f4262bac-f72c-40e2-aa51-ae352da5a35c"
PERSONNE_ASSOCIEE_E55_UUID = "909049a0-99c3-49a8-b9d6-c4c3517859fb"

# Revers_de_médaille      ="226e7258-2b03-4f46-8815-8415095287fb"
# Avers_de_médaille       ="74773744-7d22-41f5-b504-61486e1f5057"
# Titre_sur_l'image       ="01a07474-f2b9-4afd-bb05-80842ecfb527"
# Titre_dans_le_péritexte ="ded9ea93-b400-4550-9aa8-e5aac1d627a0"
# Thématique              ="f2d9b792-2cfd-4265-a2c5-e0a69ce01536"
# Titre_descriptif/forgé  ="58fb99dd-1ffb-4e00-a16f-ef6898902301"
# Type_de_représentation  ="0205f283-a73a-47e3-81bf-d0c67501fc22"
# Technique_de_gravure    = "f8914e8f-c1f1-4e1b-90e6-591bcb75ea95"
# Identifiant_BnF         = "15c5867f-f612-4a00-b9f3-17b57e566b8c"
# Invenit                 = "4d57ac14-247f-4b0e-90ca-0397b6051b8b"
# Sculpsit                = "f39eb497-5559-486c-b5ce-6a607f615773"

# Regex

pattern_article = re.compile("MG-[0-9]{4}-[0-9]{2}[a-zA-Z]?_[0-9]{3}")
pattern_livraison = re.compile("[0-9]{4}-[0-9]{2}[a-zA-Z]?")
pattern_lieu_opentheso = re.compile("^[0-9]{1,6}$")
pattern_lien = re.compile("(https?[^ ]+)")

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--xlsx")
parser.add_argument("--opentheso_id")
parser.add_argument("--cache_estampes")
parser.add_argument("--cache_tei")
parser.add_argument("--directus_secret")
args = parser.parse_args()

# Directus secret
file = open(args.directus_secret)
secret = yaml.full_load(file)

# Caches
cache_estampes = Cache(args.cache_estampes)
if args.cache_tei:
    cache_tei = Cache(args.cache_tei)

# Initialisation du graphe
iremus_ns = Namespace("http://data-iremus.huma-num.fr/id/")
crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmdig_ns = Namespace("http://www.ics.forth.gr/isl/CRMdig/")
lrmoo_ns = Namespace("http://iflastandards.info/ns/lrm/lrmoo/")
opentheso_ns = Namespace("https://opentheso.huma-num.fr/opentheso/")
sherlock_ns_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

g = Graph(base=str(iremus_ns))

g.bind("crm", crm_ns)
g.bind("crmdig", crmdig_ns)
g.bind("iremus", iremus_ns)
g.bind("lrmoo", lrmoo_ns)
g.bind("opentheso", opentheso_ns)
g.bind("sherlock", sherlock_ns_ns)

print('-' * 80)
personnes_directus = graphql_query("""
query {
  personnes(limit: -1) {
    id
  } 
}
""", secret)["data"]["personnes"]

print(f"{len(personnes_directus)} personnes dans Directus")

lieux_directus = graphql_query("""
query {
  lieux(limit: -1) {
    id
    opentheso_id
  }
}""", secret)["data"]["lieux"]

print(f"{len(lieux_directus)} lieux dans Directus")

r = requests.get(f"https://opentheso.huma-num.fr/opentheso/api/all/theso?id={args.opentheso_id}&format=jsonld", stream=True)
skos_data = json.loads(r.text)
concept_uris_list = [concept["@id"] for concept in skos_data]

print(f"{len(concept_uris_list)} concepts dans OpenTheso")
print('-' * 80)


def make_E13(cache_key, p140, p177, p141, document_context=None):
    e13 = iremus_ns[cache_estampes.get_uuid(cache_key, True)]
    g.add((e13, RDF.type, crm_ns["E13_Attribute_Assignment"]))
    g.add((e13, crm_ns["P14_carried_out_by"], iremus_ns[EQUIPE_MERCURE_GALANT_UUID]))
    g.add((e13, crm_ns["P140_assigned_attribute_to"], p140))
    g.add((e13, crm_ns["P141_assigned"], p141))
    g.add((e13, crm_ns["P177_assigned_property_of_type"], p177))
    g.add((iremus_ns[INDEXATION_ESTAMPE_ANALYTICAL_PROJECT_UUID], crm_ns["P9_consists_of"], e13))
    if document_context:
        g.add((e13, sherlock_ns_ns["has_document_context"], iremus_ns[document_context]))

    return e13


def opth(concept, thesaurus_id):
    return URIRef(f"https://opentheso.huma-num.fr/opentheso/?idc={concept}&idt={thesaurus_id}")

#######################################################################################################
# HELPERS
#######################################################################################################


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

#######################################################################################################
# TRAITEMENT DES ESTAMPES
#######################################################################################################


sheets = helpers_excel.get_xlsx_rows_as_dicts(args.xlsx)
for sheet_title, rows in sheets.items():
    for row in rows:
        if row["ID estampe"] is not None:
            id_livraison = pattern_livraison.search(row["ID estampe"]).group(0)

            # Dans le cas où la livraison n'aurait jamais été transcrite en TEI, on se donne le droit de la référencer dans le cache
            livraison_F2_originale = iremus_ns[cache_tei.get_uuid(["Collection", "Livraisons", id_livraison, "Expression originale", "F2"], True)]

            concepts_used = []
            personnes_used = []
            lieux_used = []
            id = row["ID estampe"]

            # region E36: Estampe
            estampe = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E36_uuid"], True)]
            g.add((estampe, RDF.type, crm_ns["E36_Visual_Item"]))
            g.add((iremus_ns["a96bdf72-695a-4c34-aa4e-43e75adc839e"], sherlock_ns_ns["has_member"], estampe))
            g.add((estampe, crm_ns["P2_has_type"], iremus_ns[ESTAMPE_MG_E55_UUID]))
            # endregion

            # region E42: Identifiant Mercure Galant de l'estampe
            E42_uuid = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E42_mercure_uuid"], True)]
            g.add((E42_uuid, RDF.type, crm_ns["E42_Identifier"]))
            g.add((E42_uuid, crm_ns["P2_has_type"], iremus_ns["574ffe9e-525c-42f2-8188-329ba3c7231d"]))
            g.add((E42_uuid, crm_ns["P190_has_symbolic_content"], Literal('/mercure-galant/' + id)))
            g.add((estampe, crm_ns["P1_is_identified_by"], E42_uuid))
            # endregion

            # region E42: Identifiant IIIF de l'estamp
            E42_iiif = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E42_IIIF_humanum_uuid"], True)]
            g.add((E42_iiif, RDF.type, crm_ns["E42_Identifier"]))
            g.add((E42_iiif, crm_ns["P2_has_type"], iremus_ns[IDENTIFIANT_IIIF_3_E55_UUID]))
            g.add((E42_iiif, crm_ns["P190_has_symbolic_content"], URIRef(f"https://api.nakala.fr/iiif/NAKALA_ID/full/max/0/default.jpg")))
            g.add((estampe, crm_ns["P1_is_identified_by"], E42_iiif))
            # endregion

            # region F2: Rattachement à la livraison ou à l'article
            if row["ID article OBVIL"]:
                match = pattern_article.search(row["ID article OBVIL"])
                if match:
                    try:
                        id_article = match.group(0)[3:]
                        article_F2_original = iremus_ns[cache_tei.get_uuid(["Collection", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"])]
                        article_F2_TEI = iremus_ns[cache_tei.get_uuid(["Collection", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"])]
                        g.add((article_F2_original, crm_ns["P148_has_component"], estampe))
                        g.add((article_F2_TEI, crm_ns["P148_has_component"], estampe))
                    except:
                        print("ERREUR [Colonne ID article OBVIL] Article TEI inexistant : " + id_article)
                else:
                    try:
                        livraison_F2_TEI = iremus_ns[cache_tei.get_uuid(["Collection", "Livraisons", id_livraison, "Expression TEI", "F2"])]
                        g.add((livraison_F2_originale, crm_ns["P148_has_component"], estampe))
                        g.add((livraison_F2_TEI, crm_ns["P148_has_component"], estampe))
                    except:
                        print("WARNING [Colonne ID estampe] Livraison TEI inexistante : " + id_livraison)
            # endregion

            # region F2: Article annexe à la gravure
            if row["ID OBVIL article lié"]:
                match = pattern_article.search(row["ID OBVIL article lié"])
                if match:
                    id_article_lie = match.group(0)[3:]
                    id_livraison = pattern_livraison.search(id_article_lie).group(0)
                    try:
                        article_F2_TEI = iremus_ns[cache_tei.get_uuid(["Collection", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article_lie, "F2"])]
                        e13 = make_E13(["estampes", id, "seeAlso", "E13_uuid"], estampe, RDFS.seeAlso, article_F2_TEI, estampe)
                        if row["Commentaire ID article lié OBVIL"]:
                            g.add((e13, crm_ns["P3_has_note"], Literal(row["Commentaire ID article lié OBVIL"])))
                    except:
                        print("ERREUR [Colonne ID OBVIL article lié] Article TEI inexistant : " + id_article_lie)
            # endregion

            # region seeAlso: Lien vers le texte en ligne
            cell_content = (row["Lien vers le texte [ou l'image] en ligne"] or "").strip()
            if cell_content:
                matches = re.findall(pattern_lien, cell_content)
                for url in matches:
                    if url.startswith("https://gallica.bnf.fr/"):
                        E42_gallica = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E42_gallica_uuid"], True)]
                        g.add((E42_gallica, RDF.type, crm_ns["E42_Identifier"]))
                        g.add((E42_gallica, crm_ns["P190_has_symbolic_content"], URIRef(url)))
                        g.add((E42_gallica, crm_ns["P2_has_type"], iremus_ns[IDENTIFIANT_GALLICA_E55_UUID]))
                        g.add((estampe, RDFS.seeAlso, E42_gallica))
                    else:
                        g.add((estampe, RDFS.seeAlso, URIRef(url)))

                # on crée une note si la cellule ne se résume pas à une URL
                if not matches or matches[0] != cell_content:
                    g.add((estampe, crm_ns["P3_has_note"], Literal(cell_content)))
            # endregion

            # region E13: Titre sur l'image
            if row["Titre sur l'image"]:
                make_E13(["estampes", id, "E13_titre_sur_l_image_uuid"], estampe, iremus_ns["01a07474-f2b9-4afd-bb05-80842ecfb527"], Literal(row["Titre sur l'image"]), estampe)
            # endregion

            # region E13: Titre descriptif/forgé
            if row["[titre descriptif forgé]* (Avec Maj - accentuées]"]:
                titre = row["[titre descriptif forgé]* (Avec Maj - accentuées]"].replace("[", "").replace("]", "").replace("*", "")
                make_E13(["estampes", id, "E13_titre_forgé_uuid"], estampe, iremus_ns["58fb99dd-1ffb-4e00-a16f-ef6898902301"], Literal(titre), estampe)
            # endregion

            # region E13: Titre dans le péritexte
            if row["[Titre dans le péritexte: Avis, article…]"]:
                titre = row["[Titre dans le péritexte: Avis, article…]"].replace("[", "").replace("]", "").replace("*", "")
                make_E13(["estampes", id, "E13_titre_péritexte_uuid"], estampe, iremus_ns["ded9ea93-b400-4550-9aa8-e5aac1d627a0"], Literal(titre), estampe)
            # endregion

            # region E13: Lieux associés
            if row["Lieux/Etats associés"]:
                lieux = row["Lieux/Etats associés"]
                for lieu_label in lieux.split(";"):
                    lieu = lieu_label.lstrip().split(' ')[0]
                    if (lieu == ''):
                        continue
                    match = pattern_lieu_opentheso.search(lieu)
                    # Transformer ID opentheso en uuid directus
                    if (match):
                        lieu = next((x["id"] for x in lieux_directus if x["opentheso_id"] == int(match.group(0))), None)
                    if (not lieu):
                        print(f"Aucun lieu trouvé dans Directus pour : {lieu_label}")
                        continue
                    make_E13(["collection", id, "lieux associés", lieu, "E13_uuid"], estampe, iremus_ns["413f7969-406b-4be6-a042-09a800197e8f"], iremus_ns[lieu], estampe)
                    lieux_used.append(lieu)
            # endregion

            # region E13-P138: Lieux représentés
            if row["Lieux représentés"]:
                lieux = row["Lieux représentés"]
                for lieu_label in lieux.split(";"):
                    lieu = lieu_label.lstrip().split(' ')[0]
                    if (lieu == ''):
                        continue
                    match = pattern_lieu_opentheso.search(lieu)
                    # Transformer ID opentheso en uuid directus
                    if (match):
                        lieu = next((x["id"] for x in lieux_directus if x["opentheso_id"] == int(match.group(0))), None)
                    if (not lieu):
                        print(f"Aucun lieu trouvé dans Directus pour : {lieu_label}")
                        continue

                    estampe_fragment = iremus_ns[cache_estampes.get_uuid(["estampes", id, "lieux représentés", lieu, "E36_fragment", "uuid"], True)]
                    estampe_fragment_e42_iiif = iremus_ns[cache_estampes.get_uuid(["estampes", id, "lieux représentés", lieu, "E36_fragment", "E42_IIIF_humanum_uuid"], True)]

                    g.add((estampe_fragment, RDF.type, crm_ns["E36_Visual_Item"]))
                    g.add((estampe_fragment, crm_ns["P106i_forms_part_of"], estampe))
                    g.add((estampe_fragment_e42_iiif, crm_ns["P2_has_type"], iremus_ns[IDENTIFIANT_IIIF_3_E55_UUID]))
                    g.add((estampe_fragment_e42_iiif, RDF.type, crm_ns["E42_Identifier"]))

                    make_E13(["estampes", id, "lieux représentés", lieu, "E36_fragment", "E13_IIIF_uuid"], estampe_fragment, crm_ns["P1_is_identified_by"], estampe_fragment_e42_iiif, estampe)
                    make_E13(["estampes", id, "lieux représentés", lieu, "E36_fragment", "E13_P138_uuid"], estampe_fragment, crm_ns["P138_represents"], iremus_ns[lieu], estampe)
                    lieux_used.append(lieu)
            # endregion

            # region E13: Thématique de la gravure
            if row["Thématique [Avec Maj et au pl.]"]:
                thématiques = row["Thématique [Avec Maj et au pl.]"].split(";")
                for thématique in thématiques:
                    thématique = thématique.strip().replace("’", "'")
                    if thématique == "" or thématique == " ":
                        continue
                    thématique_uri = opth(slugify(thématique), args.opentheso_id)
                    concepts_used.append(thématique_uri)
                    make_E13(["collection", id, "thématiques", thématique, "E13_uuid"], estampe, iremus_ns["f2d9b792-2cfd-4265-a2c5-e0a69ce01536"], thématique_uri, estampe)
            # endregion

            # region E13-P138: Objet représenté
            if row["Objets représentés"]:
                objets = row["Objets représentés"].split(";")
                for objet in objets:
                    objet = objet.strip().replace("’", "'")
                    if objet == "" or objet == " ":
                        continue

                    objet_type_uri = opth(slugify(objet), args.opentheso_id)
                    concepts_used.append(objet_type_uri)

                    estampe_fragment = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "uuid"], True)]
                    estampe_fragment_e42_iiif = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "E42_IIIF_humanum_uuid"], True)]
                    e18_objet = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "E18_uuid"], True)]

                    g.add((estampe_fragment, RDF.type, crm_ns["E36_Visual_Item"]))
                    g.add((estampe_fragment, crm_ns["P106i_forms_part_of"], estampe))
                    g.add((estampe_fragment_e42_iiif, crm_ns["P2_has_type"], iremus_ns[IDENTIFIANT_IIIF_3_E55_UUID]))
                    g.add((estampe_fragment_e42_iiif, RDF.type, crm_ns["E42_Identifier"]))
                    g.add((e18_objet, RDF.type, crm_ns["E18_Physical_Thing"]))
                    g.add((e18_objet, crm_ns["P2_has_type"], objet_type_uri))

                    make_E13(["estampes", id, "objets", objet, "E36_fragment", "E13_IIIF_uuid"], estampe_fragment, crm_ns["P1_is_identified_by"], estampe_fragment_e42_iiif, estampe)
                    make_E13(["estampes", id, "objets", objet, "E36_fragment", "E13_P138_uuid"], estampe_fragment, crm_ns["P138_represents"], e18_objet, estampe)

                    # Si l'objet est une médaille et comporte une inscription
                    if objet == "médaille" and (row["Médailles: avers"] or row["Médailles: revers"]):
                        if row["Médailles: avers"]:
                            estampe_fragment_avers = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "E36_uuid"], True)]
                            estampe_fragment_avers_e42_iiif = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "E42_IIIF_humanum_uuid"], True)]
                            e18_avers = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "E18_uuid"], True)]
                            e34_inscription = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "inscription", "uuid"], True)]

                            g.add((estampe_fragment_avers, RDF.type, crm_ns["E36_Visual_Item"]))
                            g.add((estampe_fragment_avers, crm_ns["P106i_forms_part_of"], estampe_fragment))
                            g.add((e18_avers, RDF.type, crm_ns["E18_Physical_Thing"]))
                            g.add((e18_avers, crm_ns["P2_has_type"], iremus_ns["74773744-7d22-41f5-b504-61486e1f5057"]))
                            g.add((estampe_fragment_avers_e42_iiif, crm_ns["P2_has_type"], iremus_ns[IDENTIFIANT_IIIF_3_E55_UUID]))
                            g.add((estampe_fragment_avers_e42_iiif, RDF.type, crm_ns["E42_Identifier"]))
                            g.add((e34_inscription, RDF.type, crm_ns["E34_Inscription"]))
                            g.add((e34_inscription, RDF.type, crm_ns["E33_Linguistic_Object"]))

                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "E42_IIIF_humanum_uuid"], estampe_fragment_avers, crm_ns["P1_is_identified_by"], estampe_fragment_avers_e42_iiif, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "E13_P138_uuid"], estampe_fragment_avers, crm_ns["P138_represents"], e18_avers, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "E13_P165_uuid"], estampe_fragment_avers, crm_ns["P165_incorporates"], e34_inscription, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "médaille_physique", "E13_P46_E18_uuid"], e18_objet, crm_ns["P46_is_composed_of"], e18_avers, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "médaille_physique", "E13_P46_E34_uuid"], e18_avers, crm_ns["P46_is_composed_of"], e34_inscription, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_avers", "inscription", "E13_uuid"], e34_inscription, crm_ns["P190_has_symbolic_content"], Literal(row["Médailles: avers"]), estampe)

                        # Si la médaille comporte une inscription sur son revers (E13)
                        if row["Médailles: revers"]:
                            estampe_fragment_revers = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "E36_uuid"], True)]
                            estampe_fragment_revers_e42_iiif = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "E42_IIIF_humanum_uuid"], True)]
                            e18_revers = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "E18_uuid"], True)]
                            e34_inscription = iremus_ns[cache_estampes.get_uuid(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "inscription", "uuid"], True)]

                            g.add((estampe_fragment_revers, RDF.type, crm_ns["E36_Visual_Item"]))
                            g.add((estampe_fragment_revers, crm_ns["P106i_forms_part_of"], estampe_fragment))
                            g.add((e18_revers, RDF.type, crm_ns["E18_Physical_Thing"]))
                            g.add((e18_revers, crm_ns["P2_has_type"], iremus_ns["226e7258-2b03-4f46-8815-8415095287fb"]))
                            g.add((estampe_fragment_revers_e42_iiif, crm_ns["P2_has_type"], iremus_ns[IDENTIFIANT_IIIF_3_E55_UUID]))
                            g.add((estampe_fragment_revers_e42_iiif, RDF.type, crm_ns["E42_Identifier"]))
                            g.add((e34_inscription, RDF.type, crm_ns["E34_Inscription"]))
                            g.add((e34_inscription, RDF.type, crm_ns["E33_Linguistic_Object"]))

                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "E42_IIIF_humanum_uuid"], estampe_fragment_revers, crm_ns["P1_is_identified_by"], estampe_fragment_revers_e42_iiif, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "E13_P138_uuid"], estampe_fragment_revers, crm_ns["P138_represents"], e18_revers, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "E13_P165_uuid"], estampe_fragment_revers, crm_ns["P165_incorporates"], e34_inscription, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "médaille_physique", "E13_P46_E18_uuid"], e18_objet, crm_ns["P46_is_composed_of"], e18_revers, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "médaille_physique", "E13_P46_E34_uuid"], e18_revers, crm_ns["P46_is_composed_of"], e34_inscription, estampe)
                            make_E13(["estampes", id, "objets", objet, "E36_fragment", "médaille_revers", "inscription", "E13_uuid"], e34_inscription, crm_ns["P190_has_symbolic_content"], Literal(row["Médailles: revers"]), estampe)
            # endregion

            # region E13-P138: Personnes représentées
            if row["Personnes représentées"]:
                personnes = row["Personnes représentées"].split(";")
                for personne in personnes:
                    personne = personne.strip().replace("’", "'")
                    if personne == "" or personne == " ":
                        continue
                    estampe_fragment = iremus_ns[cache_estampes.get_uuid(["estampes", id, "personnes représentées", personne, "E36_fragment", "uuid"], True)]
                    estampe_fragment_e42_iiif = iremus_ns[cache_estampes.get_uuid(["estampes", id, "personnes représentées", personne, "E36_fragment", "E42_IIIF_humanum_uuid"], True)]
                    e21_personne = iremus_ns[personne]

                    personnes_used.append(personne)
                    make_E13(["estampes", id, "personnes représentées", personne, "E36_fragment", "E13_IIIF_uuid"], estampe_fragment, crm_ns["P1_is_identified_by"], estampe_fragment_e42_iiif, estampe)
                    make_E13(["estampes", id, "personnes représentées", personne, "E36_fragment", "E13_P138_uuid"], estampe_fragment, crm_ns["P138_represents"], e21_personne, estampe)
            # endregion

            # region E13: Personnes associées
            if row["Personnes associées"]:
                personnes = row["Personnes associées"].split(";")
                for personne in personnes:
                    personne = personne.strip().replace("’", "'")
                    if personne == "" or personne == " ":
                        continue
                    if not is_valid_uuid(personne):
                        print("WARNING [Personnes associées] UUID invalide : " + personne)
                    else:
                        personnes_used.append(personne)
                        make_E13(["estampes", id, "personnes associées", personne, "E13_uuid"], estampe, iremus_ns[PERSONNE_ASSOCIEE_E55_UUID], iremus_ns[personne], estampe)
            # endregion

            # region E65: Production de l'estampe
            if row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"] or row[
                    "Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]:
                estampe_E65 = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E65", "uuid"], True)]
                g.add((estampe_E65, RDF.type, crm_ns["E65_Creation"]))
                g.add((estampe_E65, crm_ns["P94_has_created"], estampe))
            # endregion

            # region sous-E65: Invenit (concepteur de l'estampe)
            if row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"]:
                estampe_invenit = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E65", "E65_invenit", "uuid"], True)]
                g.add((estampe_invenit, RDF.type, crm_ns["E65_Creation"]))
                g.add((estampe_invenit, crm_ns["P2_has_type"], iremus_ns["4d57ac14-247f-4b0e-90ca-0397b6051b8b"]))
                g.add((estampe_E65, crm_ns["P9_consists_of"], estampe_invenit))

                # Lien entre conception de l'estampe et concepteur (E13)
                concepteur_uuid = row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"].strip().lower()
                make_E13(["estampes", id, "E65", "E65_invenit", "E13_P14_uuid"], estampe_invenit, crm_ns["P14_carried_out_by"], iremus_ns[concepteur_uuid], estampe)
            # endregion

            # region sous-E65: Sculpsit (graveur de l'estampe)
            if row["Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]:
                estampe_sculpsit = iremus_ns[cache_estampes.get_uuid(["estampes", id, "E65", "E65_sculpsit", "uuid"], True)]
                g.add((estampe_sculpsit, RDF.type, crm_ns["E65_Creation"]))
                g.add((estampe_sculpsit, crm_ns["P2_has_type"], iremus_ns["f39eb497-5559-486c-b5ce-6a607f615773"]))
                g.add((estampe_E65, crm_ns["P9_consists_of"], estampe_sculpsit))

                # Lien entre la gravure de l'estampe et son graveur (E13)
                graveur_uuid = row["Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"].strip().lower()
                make_E13(["estampes", id, "E65", "E65_sculpsit", "E13_P14_uuid"], estampe_sculpsit, crm_ns["P14_carried_out_by"], iremus_ns[graveur_uuid], estampe)
            # endregion

            # region E13: Type de représentation
            if row["Types de représentation"]:
                types = row["Types de représentation"].split(";")
                for type_label in types:
                    if type_label == "" or type_label == " ":
                        continue
                    slug = slugify(type_label.strip().replace("’", "'"))
                    type_uri = opth(slug, args.opentheso_id)
                    concepts_used.append(type_uri)
                    make_E13(["estampes", id, "types de représentation", slug, "E13_uuid"], estampe, iremus_ns["0205f283-a73a-47e3-81bf-d0c67501fc22"], type_uri, estampe)
            # endregion

            # region E13: Technique de gravure
            if row["Technique de la gravure"]:
                techniques = row["Technique de la gravure"].split(",")
                for technique_label in techniques:
                    if technique_label == "" or technique_label == " ":
                        continue
                    slug = slugify(technique_label.strip().replace("’", "'"))
                    technique_uri = opth(slug, args.opentheso_id)
                    concepts_used.append(technique_uri)
                    make_E13(["estampes", id, "technique de la gravure", slug, "E13_uuid"], estampe, iremus_ns["f8914e8f-c1f1-4e1b-90e6-591bcb75ea95"], technique_uri, estampe)
            # endregion

            # region E13-P70: Bibliographie relative à l'estampe
            if row["BIBLIO [y compris liens] relative à la gravure et aux artistes"]:
                make_E13(["estampes", id, "bibliographie", "E13_P70_uuid"], estampe, iremus_ns["bffeb363-05ee-449c-a666-bb16eafde48c"], Literal(row["BIBLIO [y compris liens] relative à la gravure et aux artistes"]), estampe)
            # endregion

            # region Exemplaire physique
            livraison_F3_consultation = iremus_ns[cache_estampes.get_uuid(["livraisons", id_livraison, "F3_consultation_uuid"], True)]
            livraison_F5_consultation = iremus_ns[cache_estampes.get_uuid(["livraisons", id_livraison, "F5_consultation_uuid"], True)]
            E24_feuille = iremus_ns[cache_estampes.get_uuid(["livraisons", id_livraison, "E24_feuille_uuid"], True)]

            g.add((livraison_F3_consultation, lrmoo_ns["R4_embodies"], livraison_F2_originale))
            g.add((livraison_F2_originale, lrmoo_ns["R4i_is_embodied_in"], livraison_F3_consultation))
            g.add((livraison_F5_consultation, lrmoo_ns['R7_is_materialization_of'], livraison_F3_consultation))
            g.add((livraison_F3_consultation, lrmoo_ns['R7i_is_materialized_in'], livraison_F5_consultation))
            g.add((livraison_F5_consultation, crm_ns["P46_is_composed_of"], E24_feuille))
            g.add((E24_feuille, crm_ns["P46i_forms_part_of"], livraison_F5_consultation))
            g.add((E24_feuille, crm_ns["P65_shows_visual_item"], estampe))

            # Provenance cliché (identifiant BnF)
            if row["Provenance cliché"]:
                E42_provenance = iremus_ns[cache_estampes.get_uuid(["livraisons", id_livraison, "E42_provenance_uuid"], True)]
                g.add((E42_provenance, RDF.type, crm_ns["E42_Identifier"]))
                g.add((E42_provenance, crm_ns["P2_has_type"], iremus_ns["15c5867f-f612-4a00-b9f3-17b57e566b8c"]))
                g.add((E42_provenance, crm_ns["P190_has_symbolic_content"], Literal(row["Provenance cliché"])))
                g.add((livraison_F5_consultation, crm_ns["P1_is_identified_by"], E42_provenance))

            # Format
            if row["Format (H x L en cm)"]:
                format = row["Format (H x L en cm)"].split("x")
                hauteur_uri = iremus_ns[cache_estampes.get_uuid(["livraisons", id_livraison, id, "E54_hauteur", "uuid"], True)]
                g.add((hauteur_uri, RDF.type, crm_ns["E54_Dimension"]))
                g.add((hauteur_uri, crm_ns["P2_has_type"], URIRef("http://vocab.getty.edu/page/aat/300055644")))
                g.add((hauteur_uri, crm_ns["P90_has_value"], Literal(format[0].strip().replace("’", "'"))))
                g.add((hauteur_uri, crm_ns["P91_has_unit"], URIRef("http://vocab.getty.edu/page/aat/300379098")))
                make_E13(["livraisons", id_livraison, id, "E54_hauteur", "E13_P43_dimension_uuid"], E24_feuille, crm_ns["P43_has_dimension"], hauteur_uri)

                largeur_uri = iremus_ns[cache_estampes.get_uuid(["livraisons", id_livraison, id, "E54_largeur", "uuid"], True)]
                g.add((largeur_uri, RDF.type, crm_ns["E54_Dimension"]))
                g.add((largeur_uri, crm_ns["P2_has_type"], URIRef("http://vocab.getty.edu/page/aat/300055647")))
                g.add((largeur_uri, crm_ns["P90_has_value"], Literal(format[1].replace("cm", "").strip().replace("’", "'"))))
                g.add((largeur_uri, crm_ns["P91_has_unit"], URIRef("http://vocab.getty.edu/page/aat/300379098")))
                make_E13(["livraisons", id_livraison, id, "E54_largeur", "E13_P43_dimension_uuid"], E24_feuille, crm_ns["P43_has_dimension"], largeur_uri)
            # endregion

            # region TESTS
            for concept in concepts_used:
                if (str(concept) not in concept_uris_list):
                    print(f"ERREUR [Concept manquant] {concept[45:][:-10]} ({row['ID estampe']})")
            for personne_uuid in personnes_used:
                if (not next((x for x in personnes_directus if x["id"] == personne_uuid), None)):
                    print(f"ERREUR [Personne manquante] {personne_uuid} ({row['ID estampe']})")
            for lieu_uuid in lieux_used:
                if (not next((x for x in lieux_directus if x["id"] == lieu_uuid), None)):
                    print(f"ERREUR [Lieu manquant] {lieu_uuid} ({row['ID estampe']})")
            # endregion

###########################################################################################################
# THAT’S ALL FOLKS
###########################################################################################################

cache_estampes.bye()
cache_tei.bye()

g.serialize(destination=args.ttl)

# # TODO ROADBLOACKED INSTITUTIONS : en attente de la saisie des institutions dans directus (stagiaire printemps 2023)
# # TODO sherlock data constants
