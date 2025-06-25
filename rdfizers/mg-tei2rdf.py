import argparse
from lxml import etree
import os
from rdflib import Graph, Literal as l, Namespace, RDF, SKOS, URIRef as u, XSD
import re
import pathlib
from sherlockcachemanagement import Cache
from sherlock_helpers import CRM, SHERLOCK_DATA

# Data constants

EQUIPE_MERCURE_GALANT_UUID = '684b4c1a-be76-474c-810e-0f5984b47921'
TYPE_LIVRAISON = SHERLOCK_DATA['901c2bb5-549d-47e9-bd91-7a21d7cbe49f']
TYPE_ARTICLE = SHERLOCK_DATA['13f43e00-680a-4a6d-a223-48e8d9bbeaae']
TYPE_TEXTE_ORIGINAL = SHERLOCK_DATA['7d7fc017-61ba-4f80-88e1-744f1d00dd60']
CONTENU_TEI = SHERLOCK_DATA['625bc194-d452-4f38-9ba9-83b2e0a79e00']
FICHIER_TEI = SHERLOCK_DATA['62b49ca2-ec73-4d72-aaf3-045da6869a15']
BUSINESS_ID = SHERLOCK_DATA['574ffe9e-525c-42f2-8188-329ba3c7231d']
URI_FICHIER_TEI = SHERLOCK_DATA['f005e36a-4690-4c83-9791-2927f5f823e0']
URI_FICHIER_FORGE = SHERLOCK_DATA["f284ed72-139d-4662-9dce-208bf493a45d"]

# Setup

parser = argparse.ArgumentParser()
parser.add_argument('--tei')
parser.add_argument('--output_ttl')
parser.add_argument('--cache_tei')
args = parser.parse_args()

cache_tei = Cache(args.cache_tei)

iremus_ns = Namespace('http://data-iremus.huma-num.fr/id/')
crm_ns = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
crmdig_ns = Namespace('http://www.ics.forth.gr/isl/CRMdig/')
lrmoo_ns = Namespace('http://iflastandards.info/ns/lrm/lrmoo/')
sherlock_ns = Namespace('http://data-iremus.huma-num.fr/ns/sherlock#')

g = Graph(base=str(iremus_ns))

g.bind('crm', crm_ns)
g.bind('crmdig', crmdig_ns)
g.bind('iremus', iremus_ns)
g.bind('lrm', lrmoo_ns)
g.bind('sherlock', sherlock_ns)

################################################################################
# DONNEES STATIQUES
################################################################################

# F18
F18 = iremus_ns[cache_tei.get_uuid(['Collection', 'F18', 'uuid'], True)]
g.add((F18, RDF.type, lrmoo_ns['F18_Serial_Work']))
g.add((F18, crm_ns['P102_has_title'], l('Mercure Galant')))

# JDDV
jddv = iremus_ns['86f2088f-a2d3-43f7-9bbc-72a2601635cf']
g.add((jddv, RDF.type, crm_ns['E21_Person']))
g.add((jddv, crm_ns['P1_is_identified_by'], l('Jean Donneau de Visé')))
bnf_e42 = u('ark:/12148/cb119003987')
g.add((jddv, crm_ns['P1_is_identified_by'], bnf_e42))
g.add((bnf_e42, RDF.type, crm_ns['E42_Identifier']))
g.add((bnf_e42, crm_ns['P2_has_type'], u('df9f27d6-b08b-46e6-ad67-202259c4cdbd')))  # type lien data.bnf.fr
g.add((bnf_e42, crm_ns['P190_has_symbolic_content'], u('https://data.bnf.fr/ark:/12148/cb119003987')))

# F27
F27_F18 = iremus_ns[cache_tei.get_uuid(['Collection', 'F18', 'F27'], True)]
g.add((F27_F18, RDF.type, lrmoo_ns['F27_Work_Conception']))
g.add((F27_F18, lrmoo_ns['R16_initiated'], F18))
g.add((F27_F18, crm_ns['P14_carried_out_by'], jddv))

tei_ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

for file in os.listdir(args.tei):
    if pathlib.Path(file).suffix != '.xml':
        continue

    try:
        tree = etree.parse(os.path.join(args.tei, file))
    except:
        print('Fichier XML invalide :', file)
        continue

    root = tree.getroot()

    ################################################################################
    # LIVRAISON
    ################################################################################

    # livraison :: F1
    livraison_id = file[3:-4]
    livraison_titre = root.xpath('//tei:titleStmt/tei:title/text()', namespaces=tei_ns)[0]
    livraison_F1 = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'F1'], True)]
    g.add((F18, lrmoo_ns['R10_has_member'], livraison_F1))
    g.add((livraison_F1, RDF.type, lrmoo_ns['F1_Work']))
    g.add((livraison_F1, crm_ns['P102_has_title'], l(livraison_titre)))
    g.add((livraison_F1, CRM['P2_has_type'], TYPE_LIVRAISON))  # Livraison

    # livraison :: originale :: F2
    livraison_F2_originale = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'Expression originale', 'F2'], True)]
    g.add((livraison_F1, lrmoo_ns['R3_is_realised_in'], livraison_F2_originale))
    g.add((livraison_F2_originale, RDF.type, lrmoo_ns['F2_Expression']))
    g.add((livraison_F2_originale, crm_ns['P2_has_type'], TYPE_TEXTE_ORIGINAL))
    g.add((livraison_F2_originale, crm_ns['P2_has_type'], TYPE_LIVRAISON))  # Livraison

    # livraison :: originale :: F3
    livraison_F3 = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'Expression originale', 'F3'], True)]
    g.add((livraison_F3, RDF.type, lrmoo_ns['F3_Manifestation']))
    g.add((livraison_F3, lrmoo_ns['R4_embodies'], livraison_F2_originale))

    # livraison :: originale :: F3 :: F30
    livraison_F3_F30 = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'Expression originale', 'F3_F30'], True)]
    g.add((livraison_F3_F30, RDF.type, lrmoo_ns['F30_Manifestation_Creation']))
    g.add((livraison_F3_F30, lrmoo_ns['R24_created'], livraison_F3))
    livraison_F3_E52 = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'Expression originale', 'F3_E52'], True)]
    g.add((livraison_F3_E52, RDF.type, crm_ns['E52_Time-Span']))
    livraison_F3_date = root.xpath('string(//tei:creation/tei:date/@when)', namespaces=tei_ns)
    # Si la date @when ne comporte pas de mois, on va le chercher dans l'identifiant du fichier TEI
    if len(livraison_F3_date) == 4:
        livraison_F3_date = livraison_id[:7]
    g.add((livraison_F3_E52, crm_ns['P82b_end_of_the_end'], l(livraison_F3_date + '-01T00:00:00', datatype=XSD.dateTime)))
    g.add((livraison_F3_F30, crm_ns['P4_has_time-span'], livraison_F3_E52))

    # livraison :: TEI :: F2
    livraison_F2_tei = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'F2'], True)]
    g.add((livraison_F2_tei, RDF.type, lrmoo_ns['F2_Expression']))
    g.add((livraison_F1, lrmoo_ns['R3_is_realised_in'], livraison_F2_tei))
    g.add((livraison_F2_tei, lrmoo_ns['R76_is_derivative_of'], livraison_F2_originale))
    g.add((livraison_F2_tei, CRM['P2_has_type'], TYPE_LIVRAISON))
    g.add((livraison_F2_tei, crm_ns['P2_has_type'], CONTENU_TEI))

    # livraison :: TEI :: F2 :: E42 identifiant métier
    livraison_F2_tei_E42_business_id = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'F2_E42_business_id'], True)]
    g.add((livraison_F2_tei, crm_ns['P1_is_identified_by'], livraison_F2_tei_E42_business_id))
    g.add((livraison_F2_tei_E42_business_id, RDF.type, crm_ns['E42_Identifier']))
    g.add((livraison_F2_tei_E42_business_id, crm_ns['P190_has_symbolic_content'], l('/mercure-galant/' + livraison_id)))
    g.add((livraison_F2_tei_E42_business_id, crm_ns['P2_has_type'], BUSINESS_ID))

    # livraison :: TEI :: F2 :: E42 URL du fichier TEI
    livraison_F2_tei_E42_tei_file = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'F2_E42_tei_file'], True)]
    g.add((livraison_F2_tei, crm_ns['P1_is_identified_by'], livraison_F2_tei_E42_tei_file))
    g.add((livraison_F2_tei_E42_tei_file, RDF.type, crm_ns['E42_Identifier']))
    g.add((livraison_F2_tei_E42_tei_file, CRM['P2_has_type'], URI_FICHIER_TEI))
    g.add((livraison_F2_tei_E42_tei_file, crm_ns['P190_has_symbolic_content'], u(f'https://raw.githubusercontent.com/sherlock-iremus/mercure-galant-sources/refs/heads/main/tei-edition/MG-{livraison_id}.xml')))

    # livraison :: TEI :: F2 :: E42 URL du fichier TEI sur une forge
    livraison_F2_tei_E42_tei_file_forge = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'F2_E42_tei_file_forge'], True)]
    g.add((livraison_F2_tei, crm_ns['P1_is_identified_by'], livraison_F2_tei_E42_tei_file_forge))
    g.add((livraison_F2_tei_E42_tei_file_forge, RDF.type, crm_ns['E42_Identifier']))
    g.add((livraison_F2_tei_E42_tei_file_forge, CRM['P2_has_type'], URI_FICHIER_FORGE))
    g.add((livraison_F2_tei_E42_tei_file_forge, crm_ns['P190_has_symbolic_content'], u(f'https://github.com/sherlock-iremus/mercure-galant-sources/blob/main/tei-edition/MG-{livraison_id}.xml')))

    # livraison :: TEI :: F2 :: F28
    livraison_F2_tei_F28 = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'F2_F28'], True)]
    g.add((livraison_F2_tei_F28, RDF.type, lrmoo_ns['F28_Expression_Creation']))
    g.add((livraison_F2_tei_F28, lrmoo_ns['R17_created'], livraison_F2_tei))
    g.add((livraison_F2_tei_F28, crm_ns['P16_used_specific_object'], livraison_F2_originale))
    g.add((livraison_F2_tei_F28, crm_ns['P14_carried_out_by'], iremus_ns[EQUIPE_MERCURE_GALANT_UUID]))
    g.add((livraison_F2_tei_F28, crm_ns['P2_has_type'], iremus_ns['5c6fa515-73c1-40ae-a6c1-bfedcc09ab54']))  # Édition critique TEI

    ################################################################################
    # ARTICLES
    ################################################################################

    div = root.xpath('//tei:body//tei:div[@type="article"]', namespaces=tei_ns)
    for article in div:

        article_titre_xpath = article.xpath('./tei:head/child::node()', namespaces=tei_ns)
        article_id = article.attrib['{http://www.w3.org/XML/1998/namespace}id'][3:]
        article_titre = ''
        for node in article_titre_xpath:
            if type(node) == etree._ElementUnicodeResult:
                article_titre += re.sub(r'\s+', ' ', node.replace('\n', ''))
            if type(node) == etree._Element:
                if node.tag == '{http://www.tei-c.org/ns/1.0}hi':
                    article_titre += re.sub(r'\s+', ' ', node.text.replace('\n', ''))

        # article :: originale :: F2
        article_F2_original = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'Expression originale', 'Articles', article_id, 'F2',], True)]
        g.add((article_F2_original, RDF.type, lrmoo_ns['F2_Expression']))
        g.add((article_F2_original, crm_ns['P102_has_title'], l(article_titre)))
        g.add((article_F2_original, crm_ns['P2_has_type'], TYPE_ARTICLE))
        g.add((article_F2_original, crm_ns['P2_has_type'], iremus_ns['7d7fc017-61ba-4f80-88e1-744f1d00dd60']))  # type « Édition originale »
        g.add((livraison_F2_originale, lrmoo_ns['R75_incorporates'], article_F2_original))

        # article :: TEI :: F2
        article_F2_tei = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'Articles', article_id, 'F2',], True)]
        g.add((article_F2_tei, RDF.type, lrmoo_ns['F2_Expression']))
        g.add((livraison_F2_tei, lrmoo_ns['R75_incorporates'], article_F2_tei))
        g.add((article_F2_tei, crm_ns['P102_has_title'], l(article_titre)))
        g.add((article_F2_tei, crm_ns['P2_has_type'], TYPE_ARTICLE))
        g.add((article_F2_tei, crm_ns['P2_has_type'], CONTENU_TEI))
        g.add((article_F2_tei, lrmoo_ns['R76_is_derivative_of'], article_F2_original))

        # article :: TEI :: F2 :: F28
        article_F2_tei_F28 = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'Articles', article_id, 'F2_F28'], True)]
        g.add((livraison_F2_tei_F28, crm_ns['P9_consists_of'], article_F2_tei_F28))
        g.add((article_F2_tei_F28, RDF.type, lrmoo_ns['F28_Expression_Creation']))
        g.add((article_F2_tei_F28, lrmoo_ns['R17_created'], article_F2_tei))
        g.add((article_F2_tei_F28, crm_ns['P16_used_specific_object'], article_F2_original))
        g.add((article_F2_tei_F28, crm_ns['P14_carried_out_by'], iremus_ns[EQUIPE_MERCURE_GALANT_UUID]))
        g.add((article_F2_tei_F28, crm_ns['P2_has_type'], iremus_ns['5c6fa515-73c1-40ae-a6c1-bfedcc09ab54']))

        # Ajout du TEI à la collection
        g.add((iremus_ns['7dd7cb84-ad41-44e6-8044-155827d9ff76'], sherlock_ns['has_member'], article_F2_tei))

        # article :: TEI :: F2 :: E42 identifiant métier
        article_F2_tei_E42_id = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'Articles', article_id, 'F2_E42_fragment_url_projet',], True)]
        g.add((article_F2_tei, crm_ns['P1_is_identified_by'], article_F2_tei_E42_id))
        g.add((article_F2_tei_E42_id, RDF.type, crm_ns['E42_Identifier']))
        g.add((article_F2_tei_E42_id, crm_ns['P2_has_type'], BUSINESS_ID))
        g.add((article_F2_tei_E42_id, crm_ns['P190_has_symbolic_content'], l('/mercure-galant/' + article_id)))

        # article :: TEI :: F2 :: E42 URL du fichier TEI
        article_F3_tei_E42_uri_fichier_tei = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'Articles', article_id, 'F3_E42_uri_fichier_tei'], True)]
        g.add((article_F2_tei, crm_ns['P1_is_identified_by'], article_F3_tei_E42_uri_fichier_tei))
        g.add((article_F3_tei_E42_uri_fichier_tei, RDF.type, crm_ns['E42_Identifier']))
        g.add((article_F3_tei_E42_uri_fichier_tei, CRM['P2_has_type'], URI_FICHIER_TEI))
        g.add((article_F3_tei_E42_uri_fichier_tei, crm_ns['P190_has_symbolic_content'], u(f'https://raw.githubusercontent.com/sherlock-iremus/mercure-galant-sources-sherlock/refs/heads/main/tei/articles/{article_id}.xml')))

        # article :: TEI :: F2 :: E42 URL du fichier TEI forge
        article_F3_tei_E42_uri_fichier_tei_forge = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'Articles', article_id, 'F3_E42_uri_fichier_tei_forge'], True)]
        g.add((article_F2_tei, crm_ns['P1_is_identified_by'], article_F3_tei_E42_uri_fichier_tei_forge))
        g.add((article_F3_tei_E42_uri_fichier_tei_forge, RDF.type, crm_ns['E42_Identifier']))
        g.add((article_F3_tei_E42_uri_fichier_tei_forge, CRM['P2_has_type'], URI_FICHIER_FORGE))
        g.add((article_F3_tei_E42_uri_fichier_tei_forge, crm_ns['P190_has_symbolic_content'], u(f'https://github.com/sherlock-iremus/mercure-galant-sources-sherlock/blob/main/tei/articles/{article_id}.xml')))

        # Récupération des notes éditoriales et création des E13
        notes_editoriales = []
        for element in article.iter('{http://www.tei-c.org/ns/1.0}note'):
            if element.get('resp') == 'editor':
                content = (''.join(element.itertext()).replace('\n', '').replace('\t', ''))
                content = re.sub(' +', ' ', content)
                notes_editoriales.append(content)

        n = 1
        for note in notes_editoriales:
            E13_note_editoriale = iremus_ns[cache_tei.get_uuid(['Collection', 'Livraisons', livraison_id, 'TEI', 'Articles', article_id, f'E13 note éditoriale n°{n}',], True)]
            g.add((E13_note_editoriale, crm_ns['P14_carried_out_by'], iremus_ns[EQUIPE_MERCURE_GALANT_UUID]))
            g.add((E13_note_editoriale, RDF.type, crm_ns['E13_Attribute_Assignement']))
            g.add((E13_note_editoriale, crm_ns['P140_assigned_attribute_to'], article_F2_original))
            g.add((E13_note_editoriale, crm_ns['P141_assigned'], l(note)))
            g.add((E13_note_editoriale, crm_ns['P177_assigned_property_of_type'], sherlock_ns['has_editorial_note']))
            n += 1

#####################################################################################################
# ÉCRITURE DU TTL
#####################################################################################################

g.serialize(destination=args.output_ttl)

cache_tei.bye()
