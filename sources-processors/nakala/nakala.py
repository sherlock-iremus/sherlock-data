# TODO : comment une ressource peut-elle être associée à plusieurs fichiers
# TODO : d'abord créer les ressources
# TODO : puis s'occuper des liens à la collection

import argparse
from grist_helpers import records, patch_records, post_attachment
from nakala_helpers import post_datas_uploads, get_users_me, post_datas, empty_collection
from pathlib import Path
from pprint import pprint
import sys
import time

################################################################################
# READ ARGS
################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--files_dir')
parser.add_argument('--grist_api_key')
parser.add_argument('--grist_base')
parser.add_argument('--grist_doc_id')
parser.add_argument('--grist_column_business_id')
parser.add_argument('--grist_column_filenames')
parser.add_argument('--grist_column_filestems')
parser.add_argument('--grist_column_nakala_doi')
parser.add_argument('--grist_column_sherlock_uuid')
parser.add_argument('--grist_table_id')
parser.add_argument('--nakala_api_base')
parser.add_argument('--nakala_api_key')
parser.add_argument('--nakala_collection_doi')
args = parser.parse_args()

################################################################################
# INDEX ALL EXISTING FILES BY STEM
################################################################################

directory = Path(args.files_dir)
filespaths = [str(f.resolve()) for f in directory.iterdir() if f.is_file()]
allfiles = {}
for f in filespaths:
    allfiles[Path(f).stem] = {"path": f}

################################################################################
# FETCH ALL GRIST DATA
################################################################################

grist_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, args.grist_table_id)
pc = 0
i = 0
for row in grist_data['records']:
    i += 1
    bug = False

    business_id = str(row['fields'][args.grist_column_business_id])
    nakala_doi = row['fields'][args.grist_column_nakala_doi]
    filenames = str(row['fields'][args.grist_column_filenames]) if args.grist_column_filenames in row['fields'] else None
    filestems = str(row['fields'][args.grist_column_filestems])
    sherlock_uuid = row['fields'][args.grist_column_sherlock_uuid]

    print("-" * 111)
    print("💬", f"{round(i / len(grist_data['records']) * 100, 2)}%")

    if nakala_doi:
        print('✅', business_id, '=>', nakala_doi)
        continue

    ################################################################################
    # WHICH FILES SHOULD BE UPLOADED WITH THE DATA?
    ################################################################################

    filepaths = []

    if filenames:
        filenames = (filenames).split(';')
        if not filestems:
            filestems = [Path(x).stem for x in filenames]

    if filestems:
        filestems = (filestems).split(';')

    for filestem in filestems:
        try:
            filedata = allfiles[filestem]
            filepaths.append(filedata['path'])
        except:
            print(f"❌ Non existing filestem: {filestem}")
            bug = True

    if bug:
        continue

    if len(filestems) == 0:
        continue

    ################################################################################
    # UPLOAD FILES
    ################################################################################

    files = []

    for filepath in sorted(filepaths):
        print(f"💬 Uploading file: {filepath}")
        r = post_datas_uploads(args.nakala_api_base, args.nakala_api_key, filepath)
        files.append(r)
        print('✅ /datas/uploads =>', r)

    ################################################################################
    # POST DATA
    ################################################################################

    r = post_datas(args.nakala_api_base, args.nakala_api_key, files, sherlock_uuid, business_id)
    print('✅ /datas =>', r)
    nakala_doi = r['payload']['id']
    print('✅', f"https://nakala.fr/{nakala_doi}")

    ################################################################################
    # STORE NAKALA DOI IN GRIST
    ################################################################################

    patch_records(
        args.grist_base,
        args.grist_api_key,
        args.grist_doc_id,
        args.grist_table_id,
        {"records": [{"require": {args.grist_column_business_id: row['fields'][args.grist_column_business_id]}, "fields": {args.grist_column_nakala_doi: f"https://nakala.fr/{nakala_doi}"}}]}
    )

    # empty_collection(args.nakala_api_base, args.nakala_api_key, args.nakala_collection_doi)
