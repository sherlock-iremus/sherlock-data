import argparse
from grist_helpers import records
from rdflib import RDF, Literal, URIRef
from sherlock_helpers import CRM, SHERLOCK, SHERLOCK_DATA, DataParser

GRIST_BASE = 'https://musicodb.sorbonne-universite.fr/api'

parser = argparse.ArgumentParser()
parser.add_argument('--grist_api_key')
parser.add_argument('--grist_doc_id')
parser.add_argument('--grist_sherlock_projects_table_id')
parser.add_argument('--grist_sherlock_e13_e55_table_id')
parser.add_argument('--grist_sherlock_corpus_table_id')
parser.add_argument('--output_projects_ttl')
parser.add_argument('--output_e13_e55_ttl')
args = parser.parse_args()

sherlock_projects_dp = DataParser('sherlock', args.output_projects_ttl, args.output_projects_ttl, [])
sherlock_e13_e55_dp = DataParser('sherlock', args.output_e13_e55_ttl, args.output_e13_e55_ttl, [])

grist_projects_data = records(GRIST_BASE, args.grist_api_key, args.grist_doc_id, args.grist_sherlock_projects_table_id)
grist_corpus_data = records(GRIST_BASE, args.grist_api_key, args.grist_doc_id, args.grist_sherlock_corpus_table_id)
grist_sherlock_e13_e55_data = records(GRIST_BASE, args.grist_api_key, args.grist_doc_id, args.grist_sherlock_e13_e55_table_id)

for record in grist_corpus_data['records']:
    if 'UUID' in record['fields'].keys() and record['fields']['Projet']:
        subject = SHERLOCK_DATA[record['fields']['UUID']]
        sherlock_projects_dp.graph.add((subject, RDF.type, SHERLOCK.collection))

for record in grist_sherlock_e13_e55_data['records']:
    if 'UUID' in record['fields'].keys() and record['fields']['Projet']:
        subject = SHERLOCK_DATA[record['fields']['UUID']]
        for column_name, column_value in record['fields'].items():
            sherlock_e13_e55_dp.process_cell(subject, column_name, column_value)
        sherlock_e13_e55_dp.graph.add((subject, RDF.type, CRM['E55_Type']))

del sherlock_projects_dp
del sherlock_e13_e55_dp
