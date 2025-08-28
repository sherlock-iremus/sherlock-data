import argparse
from grist_helpers import records
from pprint import pprint
from rdflib import Literal, RDF, URIRef
from sherlock_helpers import DataParser, CRM, SHERLOCK, SHERLOCK_DATA
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--grist_api_key')
parser.add_argument('--grist_base')
parser.add_argument('--grist_doc_id')
parser.add_argument('--grist_e13_e55_table_id')
parser.add_argument('--grist_e35_e55_table_id')
parser.add_argument('--grist_e41_e55_table_id')
parser.add_argument('--grist_e42_e55_table_id')
parser.add_argument('--grist_p3_e55_table_id')
parser.add_argument('--grist_projects_table_id')
parser.add_argument('--grist_rdf_properties_table_id')

parser.add_argument('--e13_authors')
parser.add_argument('--e32_uuid')
parser.add_argument('--grist_table_id')
parser.add_argument('--makerdfslabelfrom')
parser.add_argument('--output_ttl')
parser.add_argument('--p2_has_type')
parser.add_argument('--project_id')
parser.add_argument('--rdf_type')
parser.add_argument('--sherlock_collection')
args = parser.parse_args()

####################################################################################################
# FETCH GRIST CRM DATA
####################################################################################################

GRIST_METADATA = {}

for key in ['e35_e55', 'e41_e55', 'e42_e55', 'p3_e55', 'rdf_properties', 'e13_e55', 'projects']:
    key_arg = 'grist_' + key + '_table_id'
    if key not in GRIST_METADATA:
        GRIST_METADATA[key] = {}
    if (getattr(args, key_arg)):
        data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, getattr(args, key_arg))['records']
        match key:
            case 'projects':
                for datum in data:
                    GRIST_METADATA[key][datum['fields']['E42_business_id'].strip()] = datum['fields']['UUID'].strip()
            case 'e13_e55':
                for datum in data:
                    GRIST_METADATA[key][datum['fields']['project_annotation_id'].strip()] = datum['fields']['UUID'].strip()
            case 'rdf_properties':
                for datum in data:
                    GRIST_METADATA[key][datum['fields']['Prefix'] + ':' + datum['fields']['Local_name']] = datum['fields']['URI']
            case _:
                for datum in data:
                    GRIST_METADATA[key][datum['fields']['Grist_column_code'].strip()] = datum['fields']['UUID'].strip()

if args.project_id:
    project_uuid = GRIST_METADATA['projects'][args.project_id]

####################################################################################################
# INIT THE DATAPARSER
####################################################################################################

dp = DataParser(
    rdf_properties=GRIST_METADATA['rdf_properties'],
    project_id=args.project_id,
    project_uuid=project_uuid,
    out_ttl=args.output_ttl,
    e13_authors=args.e13_authors.split(',') if args.e13_authors else [],
    e35_e55=GRIST_METADATA['e35_e55'],
    e41_e55=GRIST_METADATA['e41_e55'],
    e42_e55=GRIST_METADATA['e42_e55'],
    e13_e55=GRIST_METADATA['e13_e55'],
    p3_e55=GRIST_METADATA['p3_e55'],
    makerdfslabelfrom=args.makerdfslabelfrom.split(',') if args.makerdfslabelfrom else []
)

####################################################################################################
# GO
####################################################################################################

grist_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_table_id)

for record in grist_data['records']:
    if 'UUID' in record['fields'].keys() and record['fields']['UUID']:

        subject = SHERLOCK_DATA[record['fields']['UUID']]

        if args.rdf_type:
            dp.graph.add((subject, RDF.type, URIRef(args.rdf_type)))

        if args.p2_has_type:
            types = args.p2_has_type.split(',')
            for x in types:
                dp.graph.add((subject, CRM.P2_has_type, URIRef(x)))

        if args.sherlock_collection:
            dp.graph.add((URIRef(args.sherlock_collection), SHERLOCK.has_member, subject))

        if args.e32_uuid:
            dp.graph.add((SHERLOCK_DATA[args.e32_uuid], CRM.P71_lists, subject))

        if project_uuid:
            dp.graph.add((subject, SHERLOCK['hasContextProject'], URIRef(project_uuid)))

        for column_name, column_value in record['fields'].items():
            dp.process_cell(subject, column_name, column_value)

####################################################################################################
# THAT'S ALL FOLKS
####################################################################################################

dp.log()
del dp
