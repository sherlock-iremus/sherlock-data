source ../ENV

python3 $ROOT/sources-processors/nakala/nakala.py \
    --files_dir $REPOSITORIES/euterpe-images \
    --grist_api_key $GRIST_API_KEY \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_column_business_id E42_old_db_id \
    --grist_column_filenames filenames \
    --grist_column_nakala_doi E42_nakala_doi \
    --grist_column_sherlock_uuid UUID \
    --grist_table_id 5 \
    --nakala_collection_doi 10.34847/nkl.d5adcfmy \
    --nakala_api_base api.nakala.fr \
    --nakala_api_key 6af9fa2e-edf3-d7ac-b78e-173463d44d21 \
    --delete_all_files 1 \

    # nakala_api_key_test f41f5957-d396-3bb9-ce35-a4692773f636