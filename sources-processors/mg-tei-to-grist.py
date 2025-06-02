# TODO catégorie de livraisons : extraordinaires, affaires du temps, volumes avec titres propres
# TODO précision sur la date : Achevé d'imprimer daté du 15 mai 1678.

import argparse
from grist_helpers import put_record, records_by_column
import html
from lxml import etree
from pathlib import Path
import re

################################################################################
# CONSTANTS
################################################################################

GRIST_BASE = 'https://musicodb.sorbonne-universite.fr/api'
TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}

################################################################################
# ARGS
################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--tei-articles')
parser.add_argument('--tei-livraisons')
parser.add_argument('--tei-livraisons-headers')
parser.add_argument('--grist-api-key')
parser.add_argument('--grist-doc-id')
parser.add_argument('--articles-grist-table-id')
parser.add_argument('--livraisons-grist-table-id')
args = parser.parse_args()

################################################################################
# HELPERS
################################################################################


def make_parts():
    return {
        'date': '',
        'leftovers': '',
        'tei_text': '',
        'publisher': '',
        'subtitle': '',
        'tei': '',
        'title': '',
        'tome': ''
    }


def clean_text(s):
    s = s.replace('<title xmlns="http://www.tei-c.org/ns/1.0">', '')
    s = s.replace('<title xmlns="http://www.tei-c.org/ns/1.0" type="desc">', '')
    s = s.replace('<title xmlns="http://www.tei-c.org/ns/1.0" type="sub">', '')
    s = s.replace('</title>', '')
    s = s.replace('<head xmlns="http://www.tei-c.org/ns/1.0" xmlns:tei="http://www.tei-c.org/ns/1.0">', '')
    s = s.replace('</head>', '')
    s = s.replace('<hi rend="i">', '')
    s = s.replace('</hi>', '')
    s = s.replace('[<biblScope unit="volume">.</biblScope>]', '')
    s = s.replace('(<biblScope unit="volume"></biblScope>)', '')
    s = s.replace('[<biblScope unit="volume"></biblScope>]', '')

    s = s.replace(', ,', ', ')
    s = s.replace(' ,', ',')
    s = s.replace(', [', ' [')
    s = s.replace('()', '')
    if s == ',' or s == ', ,':
        s = ''

    # Dealing with strange characters
    s = s.strip()
    for trailing_character in ['.', ',', '[']:
        if s.endswith(trailing_character):
            s = s[:-1]

    s = re.sub(r'\s+', ' ', s).strip()

    return s


def deal_with_title(s):
    s = s.replace('Galant', 'galant')
    for a in ['Le Mercure galant', 'Le Nouveau Mercure galant', 'Extraordinaire du Mercure galant', 'Nouveau Mercure', 'Mercure galant']:
        if a in s:
            s = s.replace(a, f"*{a}*")
            break

    return s


def extract_livraison_title_parts_from_xml_element(livraison_id, tei_zone, elements):
    x = make_parts()
    x['tei_text'] = re.sub(r'\s+', ' ', ''.join([''.join(e.itertext()) for e in elements])).strip()
    x['tei'] = re.sub(r'\s+', ' ', ''.join([etree.tostring(e, encoding='unicode') for e in elements])).strip()

    for i in range(0, len(elements), 1):
        e = elements[i]

        # Title
        if i == 0:
            s = etree.tostring(e, encoding='unicode')

            s = s.replace('<bibl xmlns="http://www.tei-c.org/ns/1.0">', '')
            s = s.replace('</bibl>', '')

            # Extraction de la date
            date_patterns = [r"<date>(.*)</date>", r"((quartier d.*)?(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) \d{4})"]
            for date_pattern in date_patterns:
                date_match = re.search(date_pattern, s)
                if date_match:
                    x['date'] = date_match.group(1).strip()
                    s = re.sub(date_pattern, '', s)
                    break

            # Extraction du publisher
            publisher_pattern = r"<publisher>(.*)</publisher>"
            publisher_match = re.search(publisher_pattern, s)
            if publisher_match:
                x['publisher'] = publisher_match.group(1).strip()
                s = re.sub(publisher_pattern, '', s)

            # Extraction du tome
            for tome_pattern in [r"\(tome ([0123456789IVX]*)\)", r"\[tome ([0123456789IVX]*)\]", r"tome ([0123456789IVX]*)"]:
                tome_match = re.search(tome_pattern, s)
                if tome_match:
                    x['tome'] = tome_match.group(1).strip()
                    s = re.sub(tome_pattern, '', s)

            # Extraction du titre
            title_pattern = r"<title .*>(.*)</title>"
            title_match = re.search(title_pattern, s)
            if title_match:
                x['title'] = deal_with_title(clean_text(title_match.group(1))).strip()
                s = re.sub(title_pattern, '', s)

            # x['leftovers'] = clean_text(s)

        # Subtitle
        elif i == 1:
            s1 = etree.tostring(e, encoding='unicode')

            # Extraction du sous-titre
            title_pattern = r"<title .*>(.*)</title>"
            title_match = re.search(title_pattern, s1)
            if title_match:
                x['subtitle'] = title_match.group(1)
                s1 = re.sub(title_pattern, '', s1)

    return x


################################################################################
# DATA
################################################################################

livraisons = {}
articles = {}

################################################################################
# COLLECT LIVRAISONS HEADERS TITLES
################################################################################

for file in sorted(Path(args.tei_livraisons_headers).iterdir()):
    title_from_fileDesc = None
    title_from_sourceDesc = None

    # Check if .xml file
    if Path(file).suffix != '.xml':
        continue

    # Parse XML
    tree = etree.parse(file)
    root = tree.getroot()

    # Extract livraison id
    livraison_id_from_file = Path(file).stem.replace('.header', '')
    if livraison_id_from_file not in livraisons:
        livraisons[livraison_id_from_file] = {}

    # Extract livraison title from fileDesc
    livraisons[livraison_id_from_file]['fileDesc'] = extract_livraison_title_parts_from_xml_element(livraison_id_from_file, 'fileDesc', root.xpath('//tei:fileDesc/tei:titleStmt/tei:title', namespaces=TEI_NS))

    # Extract livraison title from sourceDesc
    livraisons[livraison_id_from_file]['sourceDesc'] = extract_livraison_title_parts_from_xml_element(livraison_id_from_file, 'sourceDesc', root.xpath('//tei:sourceDesc/tei:bibl', namespaces=TEI_NS))

################################################################################
# COLLECT LIVRAISONS BIDY TITLES
################################################################################

for file in sorted(Path(args.tei_livraisons).iterdir()):
    # Check if .xml file
    if Path(file).suffix != '.xml':
        continue

    # Parse XML
    tree = etree.parse(file)
    root = tree.getroot()

    # Extract livraison id
    livraison_id_from_file = Path(file).stem
    if livraison_id_from_file not in livraisons:
        livraisons[livraison_id_from_file] = {}

    # Extract livraison title
    livraisons[livraison_id_from_file]['body'] = extract_livraison_title_parts_from_xml_element(livraison_id_from_file, 'body', root.xpath('//tei:text/tei:body/tei:head', namespaces=TEI_NS))

################################################################################
# LIVRAISONS TITLES -> GRIST
################################################################################

for livraion_id, v in livraisons.items():
    continue
    fields = {}
    for k in make_parts().keys():
        for zone in ['fileDesc', 'sourceDesc', 'body']:
            if livraisons[livraion_id][zone][k]:
                fields[f"{zone}_{k}"] = livraisons[livraion_id][zone][k]
                print(livraion_id.ljust(10), zone.ljust(12), k.ljust(12), livraisons[livraion_id][zone][k])
    r = put_record(
        GRIST_BASE,
        args.grist_api_key,
        args.grist_doc_id,
        args.livraisons_grist_table_id,
        {"records": [{"require": {"E42_business_id": livraion_id}, "fields": fields}]}
    )

################################################################################
# ARTICLES
################################################################################

for file in sorted(Path(args.tei_articles).iterdir()):
    # Check if .xml file
    if not file.is_file() or Path(file).suffix != '.xml':
        continue

    # Parse XML
    tree = etree.parse(file)
    root = tree.getroot()

    # Extract article id
    article_id_from_file = Path(file).stem.replace('MG-', '')
    article_id_from_tei = root.get('{http://www.w3.org/XML/1998/namespace}id').replace('MG-', '')
    if article_id_from_file != article_id_from_tei:
        print('Discrépance dans les identifiants', file)
        continue
    else:
        article_id = article_id_from_file

    # Extract article title
    head = root.find('{http://www.tei-c.org/ns/1.0}head')
    print(etree.tostring(head, encoding='unicode'))
    continue

    # PUT Grist
    # r = put_record(GRIST_BASE, args.grist_api_key, args.grist_doc_id, args.articles_grist_table_id, {"records": [{"require": {"E42_business_id": article_id}, "fields": {"P102_has_title": article_title}}]})

    print(article_id, article_title)
