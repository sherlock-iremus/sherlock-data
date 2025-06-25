import argparse
from grist_helpers import records
from pprint import pprint
from rdflib import RDF, URIRef
from sherlock_helpers import DataParser, CRM, SHERLOCK, SHERLOCK_DATA
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--grist_api_key')
parser.add_argument('--grist_base')
parser.add_argument('--grist_doc_id')
parser.add_argument('--grist_table_id')
parser.add_argument('--rdf_properties_grist_table_id')
parser.add_argument('--project_id')
parser.add_argument('--sherlock_collection')
parser.add_argument('--output_ttl')
parser.add_argument('--e32_uuid')
parser.add_argument('--rdf_type')
parser.add_argument('--P2_has_type')
parser.add_argument('--e13_authors')
parser.add_argument('--grist_e41_e55_table_id')
parser.add_argument('--grist_e42_e55_table_id')
parser.add_argument('--grist_e13_e55_table_id')
parser.add_argument('--grist_p3_e55_table_id')
parser.add_argument('--makerdfslabelfrom')
args = parser.parse_args()

###############################################################################
# FETCH GRIST CRM DATA
###############################################################################

rdf_properties = {}
e41_e55 = {}
e42_e55 = {}
e13_e55 = {}
p3_e55 = {}

rdf_properties_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.rdf_properties_grist_table_id)['records']
for x in rdf_properties_data:
    rdf_properties[x['fields']['Prefix'] + ':' + x['fields']['Local_name']] = x['fields']['URI']

if args.grist_e41_e55_table_id:
    e41_e55_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_e41_e55_table_id)['records']
    for x in e41_e55_data:
        if x['fields']['P1_is_identified_by']:
            e41_e55[x['fields']['Grist_column_code'].strip()] = x['fields']['UUID'].strip()
if args.grist_e42_e55_table_id:
    e42_e55_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_e42_e55_table_id)['records']
    for x in e42_e55_data:
        if x['fields']['P1_is_identified_by']:
            e42_e55[x['fields']['Grist_column_code'].strip()] = x['fields']['UUID'].strip()
if args.grist_e13_e55_table_id:
    e13_e55_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_e13_e55_table_id)['records']
    for x in e13_e55_data:
        if x['fields']['P1_is_identified_by']:
            e13_e55[x['fields']['project_annotation_id'].strip()] = x['fields']['UUID'].strip()
if args.grist_p3_e55_table_id:
    p3_e55_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_p3_e55_table_id)['records']
    for x in p3_e55_data:
        if x['fields']['P1_is_identified_by']:
            p3_e55[x['fields']['Grist_column_code'].strip()] = x['fields']['UUID'].strip()

###############################################################################
# INIT THE DATAPARSER
###############################################################################

dp = DataParser(
    rdf_properties,
    args.project_id,
    args.output_ttl,
    args.e13_authors.split(',') if args.e13_authors else [],
    e41_e55,
    e42_e55,
    e13_e55,
    p3_e55,
    args.makerdfslabelfrom.split(',') if args.makerdfslabelfrom else []
)

###############################################################################
# GO
###############################################################################

grist_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_table_id)

for record in grist_data['records']:
    if 'UUID' in record['fields'].keys() and record['fields']['UUID']:

        # La donnée
        subject = SHERLOCK_DATA[record['fields']['UUID']]

        # Son type
        if args.rdf_type:
            dp.graph.add((subject, RDF.type, URIRef(args.rdf_type)))

        # Ses P2
        if args.P2_has_type:
            types = args.P2_has_type.split(',')
            for x in types:
                dp.graph.add((subject, CRM.P2_has_type, URIRef(x)))

        # Sa collection SHERLOCK
        if args.sherlock_collection:
            dp.graph.add((URIRef(args.sherlock_collection), SHERLOCK.has_member, subject))

        # Son document d'autorité éventuel
        if args.e32_uuid:
            dp.graph.add((SHERLOCK_DATA[args.e32_uuid], CRM.P71_lists, subject))

        # Ses colonnes
        for column_name, column_value in record['fields'].items():
            dp.process_cell(subject, column_name, column_value)

###############################################################################
# THAT'S ALL FOLKS
###############################################################################

dp.log()
del dp
