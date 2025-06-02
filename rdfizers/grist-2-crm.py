import argparse
from grist_helpers import records
from rdflib import Graph, Literal, RDF, URIRef
from sherlock_helpers import DataParser, CRM, SHERLOCK, SHERLOCK_DATA

GRIST_BASE = 'https://musicodb.sorbonne-universite.fr/api'

parser = argparse.ArgumentParser()
parser.add_argument('--grist_api_key')
parser.add_argument('--grist_doc_id')
parser.add_argument('--grist_table_id')
parser.add_argument('--sherlock_project_code')
parser.add_argument('--sherlock_corpus')
parser.add_argument('--sherlock_e13_e55_ttl')
parser.add_argument('--output_ttl')
parser.add_argument('--e32_uuid')
parser.add_argument('--rdf_type')
parser.add_argument('--e13_authors')
args = parser.parse_args()

dp = DataParser(args.sherlock_project_code, args.output_ttl, args.sherlock_e13_e55_ttl, args.e13_authors.split(','))

###############################################################################
# GO
###############################################################################

grist_data = records(GRIST_BASE, args.grist_api_key, args.grist_doc_id, args.grist_table_id)

for record in grist_data['records']:
    if 'UUID' in record['fields'].keys():
        # La donnée
        subject = SHERLOCK_DATA[record['fields']['UUID']]

        # Son type
        dp.graph.add((subject, RDF.type, URIRef(args.rdf_type)))

        # Sa collection SHERLOCK
        dp.graph.add((URIRef(args.sherlock_corpus), SHERLOCK.has_member, subject))

        # Son document d'autorité éventuel
        if args.e32_uuid:
            dp.graph.add((SHERLOCK_DATA[args.e32_uuid], CRM.P71_lists, subject))

        # Ses colonnes
        for column_name, column_value in record['fields'].items():
            dp.process_cell(subject, column_name, column_value)

###############################################################################
# THAT'S ALL FOLKS
###############################################################################

del dp
