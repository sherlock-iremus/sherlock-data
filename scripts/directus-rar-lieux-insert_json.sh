mkdir -p ./temp/referentiels-ancien-regime/directus/lieux/
python3 ./directus/referentiels-ancien-regime/lieux-insert_json.py \
    --json_concepts "./temp/referentiels-ancien-regime/directus/lieux/lieux.json" \
    --json_index "./temp/referentiels-ancien-regime/directus/lieux/lieux-indexation.json"