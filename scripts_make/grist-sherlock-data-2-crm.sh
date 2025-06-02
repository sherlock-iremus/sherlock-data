source ../ENV

python3 $ROOT/rdfizers/grist-sherlock-data-2-crm.py \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_sherlock_projects_table_id 16 \
    --grist_sherlock_e13_e55_table_id 15 \
    --grist_sherlock_corpus_table_id 17 \
    --output_projects_ttl $ROOT/out/ttl/grist/sherlock-projects.ttl \
    --output_e13_e55_ttl $ROOT/out/ttl/grist/sherlock-e13-e55.ttl \