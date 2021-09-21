mkdir -p ./temp/referentiels-ancien-regime/directus/personnes/
python3 ./directus/referentiels-ancien-regime/personnes-insert_json.py \
    --json_concepts "./temp/referentiels-ancien-regime/directus/personnes/personnes.json" \
    --json_index "./temp/referentiels-ancien-regime/directus/personnes/personnes-indexation.json"