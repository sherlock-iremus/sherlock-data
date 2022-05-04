import argparse
import sys
import os
from pprint import pprint
import requests
import yaml

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
from helpers_rdf import *
from sherlockcachemanagement import Cache
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--xlsx")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")
parser.add_argument("--cache_personnes")
parser.add_argument("--cache_lieux")
parser.add_argument("--vocab_estampes")
args = parser.parse_args()

# Caches
cache = Cache(args.cache)
if args.cache_tei:
    cache_tei = Cache(args.cache_tei)
if args.cache_personnes:
    cache_personnes = Cache(args.cache_personnes)
if args.cache_lieux:
    cache_lieux = Cache(args.cache_lieux)

# Initialisation du graphe
init_graph()

def make_E13(path, subject, predicate, object):
    global E13_uri
    E13_uri = she(cache.get_uuid(path, True))
    t(E13_uri, a, crm("E13_Attribute_Assignement"))
    t(E13_uri, crm("P14_carried_out_by"), she("846ef057-41d5-48e1-bd7f-2299b2faaf00"))
    t(E13_uri, crm("P140_assigned_attribute_to"), subject)
    t(E13_uri, crm("P141_assigned"), object)
    t(E13_uri, crm("P177_assigned_property_type"), predicate)

#######################################################################################################
# Récupération du vocabulaire d'indexation des estampes
#######################################################################################################

with open(args.vocab_estampes, "r+") as f:
    concepts_uuid = yaml.safe_load(f)

#######################################################################################################
# Traitement des estampes
#######################################################################################################

rows = get_xlsx_rows_as_dicts(args.xlsx)

collection = she("759d110d-fd68-47bb-92fd-341bb63dbcae")

for row in rows:
    if row["ID estampe"] is not None:
        id = row["ID estampe"]

        # L'estampe (E36)
        estampe = she(cache.get_uuid(["estampes", id, "E36", "uuid"], True))
        print("\n" + id)
        t(estampe, a, crm("E36_Visual_Item"))
        t(collection, crm("P165_has_component"), estampe)
        t(estampe, crm("P2_has_type"), she("1317e1ac-50c8-4b97-9eac-c4d902b7da10"))
        
        # Identifiant Mercure Galant de l'estampe (E42)
        estampe_id_MG = she(cache.get_uuid(["estampes", id, "E36", "identifiant MG"], True))
        t(estampe_id_MG, a, crm("E42_Identifier"))
        t(estampe_id_MG, crm("P2_has_type"), she("92c258a0-1e34-437f-9686-e24322b95305"))
        t(estampe_id_MG, RDFS.label, l(id))
        t(estampe, crm("P1_is_identified_by"), estampe_id_MG)

        # Identifiant IIIF de l'estampe (E42)
        estampe_id_iiif = she(cache.get_uuid(["estampes", id, "E36", "identifiant iiif"], True))
        t(estampe_id_iiif, a, crm("E42_Identifier"))
        t(estampe_id_iiif, crm("P2_has_type"), she("19073c4a-0ef7-4ac4-a51a-e0810a596773"))
        t(estampe_id_iiif, RDFS.label, u(f"https://ceres.huma-num.fr/iiif/3/mercure-galant-estampes--{id.replace(' ', '%20')}/full/max/0/default.jpg"))
        t(estampe, crm("P1_is_identified_by"), estampe_id_iiif)

        # Provenance cliché (identifiant BnF) (E42)
        if row["Provenance cliché"]:
            estampe_id_provenance = she(cache.get_uuid(["estampes", id, "E36", "provenance"], True))
            t(estampe_id_provenance, a, crm("E42_Identifier"))
            t(estampe_id_provenance, crm("P2_has_type"), she("15c5867f-f612-4a00-b9f3-17b57e566b8c"))
            t(estampe_id_provenance, RDFS.label, l(row["Provenance cliché"]))
            t(estampe, crm("P1_is_identified_by"), estampe_id_provenance)

        # Rattachement à la livraison ou à l'article OBVIL
        # Si l'article n'est pas précisé:
        if not row["ID article OBVIL"]:
            id_image = id
            id_livraison = id[0:-4]
            if id_livraison.endswith("_"):
                id_livraison = id_livraison[0:-1]
            try:
                # Livraison originale
                livraison_F2_originale = she(
                    cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression originale", "F2"]))
                t(livraison_F2_originale, crm("P165_has_component"), estampe)

                # Livraison TEI
                livraison_F2_TEI = she(
                    cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression TEI", "F2"]))
                t(livraison_F2_TEI, crm("P165_has_component"), estampe)
            except:
                print("ID article OBVIL : La livraison " + id_livraison + " est introuvable")
        # Si l'article est précisé:
        else:
            id_article = row["ID article OBVIL"][3:]
            id_livraison = id_article[0:11]
            try:
                if id_livraison.endswith("_"):
                    id_livraison = id_livraison[0:-1]
                # Article original
                article_F2_original = she(cache_tei.get_uuid(
                    ["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
                t(article_F2_original, crm("P165_has_component"), estampe)
                # Article TEI
                article_F2_TEI = she(cache_tei.get_uuid(
                    ["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
                t(article_F2_TEI, crm("P165_has_component"), estampe)
            except:
                print("ID OBVIL article : l'article " + str(row["ID article OBVIL"]) + " est introuvable dans les fichiers TEI")

        # Article annexe à la gravure
        if row["ID OBVIL article lié"]:
            id_article = row["ID OBVIL article lié"][3:]
            id_livraison = id_article[0:10]
            try:
                article_F2_TEI = she(cache_tei.get_uuid(
                    ["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
                make_E13(["estampes", id, "E36", "seeAlso", "E13"], estampe, RDFS.seeAlso, article_F2_TEI)
                # Commentaire décrivant le lien entre la gravure et l'article
                if row["Commentaire ID article lié OBVIL"]:
                    make_E13(["estampes", id, "E36", "seeAlso", "note", "E13"], article_F2, crm("P3_has_note"), l(row["Commentaire ID article lié OBVIL"]))
            except:
                print("ID OBVIL article lié : l'article " + str(row["ID OBVIL article lié"]) + " est introuvable dans les fichiers TEI")

        # Lien vers le texte en ligne
        if row["Lien vers le texte [ou l'image] en ligne"]:
            lien = row["Lien vers le texte [ou l'image] en ligne"]
            if lien[:3] != "http":
                make_E13(["estampes", id, "E36", "note sur le texte en ligne", lien, "E13"], estampe, crm("P3_has_note"), l(lien))
            else:
                print(lien[:3])
                try:
                    lien = u(row["Lien vers le texte [ou l'image] en ligne"])
                    t(lien, crm("P2_has_type"), she("e73699b0-9638-4a9a-bfdd-ed1715416f02"))
                    make_E13(["estampes", id, "E36", "lien vers le texte en ligne", lien, "E13"], estampe, RDFS.seeAlso, lien)
                except:
                    print("Le lien vers le texte" + row["Lien au texte [ou à l'image] en ligne"] + "' n'est pas une URL valide")

        # Titre sur l'image (E13)
        if row["Titre sur l'image"]:
            titre = row["Titre sur l'image"].replace("[", "").replace("]", "").replace("*", "")
            make_E13(["estampes", id, "E36", "titre sur l'image"], estampe, she("01a07474-f2b9-4afd-bb05-80842ecfb527"), l(titre))

        # Titre descriptif/forgé (E13)
        if row["[titre descriptif forgé]* (Avec Maj - accentuées]"]:
            titre = row["[titre descriptif forgé]* (Avec Maj - accentuées]"].replace("[", "").replace("]", "").replace("*", "")
            make_E13(["estampes", id, "E36", "titre forgé"], estampe, she("58fb99dd-1ffb-4e00-a16f-ef6898902301"), l(titre))

        # Titre dans le péritexte (E13)
        if row["[Titre dans le péritexte: Avis, article…]"]:
            titre = row["[Titre dans le péritexte: Avis, article…]"].replace("[", "").replace("]", "").replace("*", "")
            make_E13(["estampes", id, "E36", "titre péritexte"], estampe, she("ded9ea93-b400-4550-9aa8-e5aac1d627a0"), l(titre))

        # Lieu représenté
        if row["Lieux représentés"]:
            lieu = row["Lieux représentés"]
            # Zone de l'image comportant la représentation du lieu (E13)
            estampe_zone_img = she(cache.get_uuid(["estampes", id, "E36", "lieux", lieu, "zone de l'objet (E36)", "uuid"], True))
            t(estampe_zone_img, a, crm("E36_Visual_Item"))
            make_E13(["estampes", id, "E36", "lieux", lieu, "zone de l'objet (E36)", "E13"], estampe, crm("P106_is_composed_of"), estampe_zone_img)
            # Recherche d'UUID dans le référentiel des lieux
            try:
                lieu_uuid = she(cache_lieux.get_uuid(["lieux", str(lieu), "E93", "uuid"]))
                if lieu_uuid:
                    make_E13(["estampes", id, "E36", "lieux", lieu, "zone de l'objet (E36)", "lieu représenté"], estampe_zone_img, crm("P138_represents"), lieu_uuid)
            except:
                make_E13(["collection", id, "E36", "lieux", lieu, "zone de l'objet (E36)", "lieu représenté"], estampe_zone_img, crm("P138_represents"), l(lieu))

        # Thématique de la gravure
        if row["Thématique [Avec Maj et au pl.]"]:
            thématiques = row["Thématique [Avec Maj et au pl.]"].split(";")
            for thématique in thématiques:
                thématique = thématique.strip()
                if thématique == "" or thématique == " ":
                    continue
                try:
                    thématique_uuid = she(concepts_uuid[thématique])
                    make_E13(["collection", id, "E36", "thématique", thématique, "E13"], estampe, she("f2d9b792-2cfd-4265-a2c5-e0a69ce01536"), thématique_uuid)
                except:
                    print("La thématique", thématique,
                        "est introuvable dans le vocabulaire d'indexation d'estampes")

        # Objet représenté (E13)
        if row["Objets représentés"]:
            objets = row["Objets représentés"].split(";")
            for objet in objets:
                objet = objet.strip()
                if objet == "" or objet == " ":
                    continue
                
                # Zone de l'image représentant l'objet (E13)
                estampe_zone_img = she(
                    cache.get_uuid(["estampes", id, "E36", "objets", objet, "zone de l'objet (E36)", "uuid"], True))
                t(estampe_zone_img, a, crm("E36_Visual_Item"))
                make_E13(["estampes", id, "E36", "objets", objet, "zone de l'objet (E36)", "E13"], estampe, crm("P106_is_composed_of"), estampe_zone_img)
                try:
                    # Recherche de l'UUID de l'objet dans le vocabulaire des estampes
                    objet_uuid = she(concepts_uuid[objet])
                    make_E13(["estampes", id, "E36", "objets", objet, "zone de l'objet (E36)", "représentation de l'objet (E13)"], estampe_zone_img, crm("P138_represents"), objet_uuid)
                except:
                    make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "représentation de l'objet (E13)"], estampe_zone_img, crm("P138_represents"), l(objet))
                    print("L'objet", objet,
                        "est introuvable dans le vocabulaire d'indexation d'estampes")
                    
                # Si l'objet est une médaille et comporte une inscription
                if objet == "médaille" and row["Médailles: avers"] or row["Médailles: revers"]:
                    if row["Médailles: avers"]:
                        médaille_zone_inscrip = she(cache.get_uuid(
                            ["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)",
                            "avers", "uuid"], True))
                        t(médaille_zone_inscrip, a, crm("E36_Visual_Item"))
                        make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)",
                                "zone d'inscription (médaille)", "avers", "E13"], estampe_zone_img, crm("P106_is_composed_of"), médaille_zone_inscrip)
                        médaille_inscrip = she(
                            cache.get_uuid(
                                ["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)",
                                "avers", "inscription", "uuid"], True))
                        t(médaille_inscrip, a, crm("E33_Linguistic_Object"))
                        make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)", 
                                "avers", "inscription", "E13"], médaille_zone_inscrip, crm("P165_incorporates"), médaille_inscrip)
                        t(E13_uri, she_ns("sheP_position_du_texte_par_rapport_à_la_médaille"), she("fc229531-0999-4499-ab0b-b45e18e8196f"))
                        # Contenu de l'inscription
                        make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)",
                                "inscription",
                                "avers", "inscription", "contenu (E13)"], médaille_inscrip, crm("P190_has_symbolic_content"), l(row["Médailles: avers"]))
                    
                    # Si la médaille comporte une inscription sur son revers (E13)
                    if row["Médailles: revers"]:
                        médaille_zone_inscrip = she(cache.get_uuid(
                            ["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)",
                            "revers", "uuid"], True))
                        t(médaille_zone_inscrip, a, crm("E36_Visual_Item"))
                        make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)",
                                "zone d'inscription (médaille)", "revers", "E13"], estampe_zone_img, crm("P106_is_composed_of"), médaille_zone_inscrip)
                        médaille_inscrip = she(cache.get_uuid(
                            ["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)",
                            "revers", "inscription", "uuid"], True))
                        t(médaille_inscrip, a, crm("E33_Linguistic_Object"))
                        make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)",
                                "revers", "inscription", "E13"], médaille_zone_inscrip, crm("P165_incorporates"), médaille_inscrip)
                        t(E13_uri, she_ns("sheP_position_du_texte_par_rapport_à_la_médaille"), she("357a459f-4f27-4d46-b5ac-709a410bce04"))
                        # Contenu de l'inscription
                        make_E13(["collection", id, "E36", "objets", objet, "zone de l'objet (E36)", "zone d'inscription (médaille)",
                                "revers", "inscription", "contenu (E13)"], médaille_inscrip, crm("P190_has_symbolic_content"), l(row["Médailles: revers"]))
                    
        # Personnes représentées
        if row["Personnes représentées"]:
            personnes = row["Personnes représentées"].split(";")
            for personne in personnes:
                personne = personne.strip()
                if personne == "" or personne == " ":
                    continue
                make_E13(["collection", id, "E36", "personnes", personne, "zone de l'objet (E36)", "personne représentée"], estampe_zone_img, crm("P138_represents"), she(personne))

        # TODO institutions associées
        # TODO lieux associés
        # TODO personnes associées

        # Production (E12) de l'estampe
        if row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"] or row[
                "Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]:
            estampe_E12 = she(cache.get_uuid(["estampes", id, "E36", "E12", "uuid"], True))
            t(estampe_E12, a, crm("E12_Production"))
            t(estampe_E12, crm("P108_has_produced"), estampe)

        # Invenit (concepteur de l'estampe) (sous-E12)
        if row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"]:
            estampe_invenit = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "uuid"], True))
            t(estampe_invenit, a, crm("E12_Production"))
            t(estampe_invenit, crm("P2_has_type"), she("4d57ac14-247f-4b0e-90ca-0397b6051b8b"))
            t(estampe_E12, crm("P9_consists_of"), estampe_invenit)

            # Lien entre conception de l'estampe et concepteur (E13)
            estampe_invenit_auteur = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "auteur"], True))
            t(estampe_invenit_auteur, a, crm("E21_Person"))
            t(estampe_invenit_auteur, RDFS.label,
            l(row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"]))
            make_E13(["estampes", id, "E36", "E12", "invenit", "E13"], estampe_invenit, crm("P14_carried_out_by"), estampe_invenit_auteur)

        # Sculpsit (graveur de l'estampe) (sous-E12)
        if row["Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]:
            estampe_sculpsit = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "uuid"], True))
            t(estampe_sculpsit, a, crm("E12_Production"))
            t(estampe_sculpsit, crm("P2_has_type"), she("f39eb497-5559-486c-b5ce-6a607f615773"))
            t(estampe_E12, crm("P9_consists_of"), estampe_sculpsit)

            # Lien entre la gravure de l'estampe et son graveur (E13)
            estampe_sculpsit_auteur = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "auteur"], True))
            t(estampe_sculpsit_auteur, a, crm("E21_Person"))
            t(estampe_sculpsit_auteur, RDFS.label, l(row["Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]))
            make_E13(["estampes", id, "E36", "E12", "sculpsit", "E13"], estampe_sculpsit, crm("P14_carried_out_by"), estampe_sculpsit_auteur)

        # Type de représentation (E13)
        if row["Type de représentation"]:
            types = row["Type de représentation"].split(";")
            for x in types:
                if x == "" or x == " ":
                    continue
                try:
                    type_uuid = she(concepts_uuid[x])
                    make_E13(["estampes", id, "E36", "types de représentation", x], estampe, she("0205f283-a73a-47e3-81bf-d0c67501fc22"), type_uuid)
                except:
                    print("Le type de représentation", x, "n'existe pas dans le vocabulaire des estampes")

        # Technique de gravure (E13)
        if row["Technique de la gravure (et format)"]:
            techniques = row["Technique de la gravure (et format)"].split(";")
            for x in techniques:
                if x == "" or x == " ":
                    continue
                try:
                    technique_uuid = she(concepts_uuid[x])
                    make_E13(["estampes", id, "E36", "types de représentation", x], estampe, she("f8914e8f-c1f1-4e1b-90e6-591bcb75ea95"), technique_uuid)
                except:
                    print("La technique de gravure", x, "n'existe pas dans le vocabulaire des estampes")

        # Notes sur la provenance de la gravure
        if row["Note éditoriale [provenance, texte afférent, etc.]"]:
            note_editoriale = row["Note éditoriale [provenance, texte afférent, etc.]"]
            make_E13(["estampes", id, "E36", "notes", "E13"], estampe, crm("P3_has_note"), l(note_editoriale))

        # Autres liens externes
        # TODO Réparer les erreurs URL
        """
        if row["Concordances [autres tirages en ligne ; hypothèse sur les modèles]"]:
            try:
                lien_externe = u(row["Concordances [autres tirages en ligne ; hypothèse sur les modèles]"])
                make_E13(["estampes", id, "E36", "lien externe", "E13"], estampe, RDFS.seeAlso, lien_externe)
            except:
                print("Estampe", id, ": 'Liens : " + row["Concordances [autres tirages en ligne ; hypothèse sur les modèles]"] + "' n'est pas une URL valide")
        """

        # Bibliographie relative à l'estampe
        if row["BIBLIO [y compris liens] relative à la gravure et aux artistes"]:
            biblio = she(cache.get_uuid(["estampes", id, "E36", "bibliographie", "uuid"], True))
            t(biblio, a, crm("E31_Document"))
            t(biblio, RDFS.label, l(row["BIBLIO [y compris liens] relative à la gravure et aux artistes"]))
            make_E13(["estampes", id, "E36", "bibliographie", "E13"], estampe, crm("P70_documents"), biblio)


###########################################################################################################
# Création du graphe et du cache
###########################################################################################################

cache.bye()
save_graph(args.ttl)

# TODO note sur l'attribution