mkdir -p ./temp/referentiels-ancien-regime/directus/indexations/
python3 ./directus/referentiels-ancien-regime/indexations-directus_to_ttl.py \
    --json "./temp/referentiels-ancien-regime/directus/indexations/directus_export_indexations.json" \
    --ttl "./out/ttl/rar-directus-indexations.ttl" \
    --cache_tei "./caches/mercure-galant/cache_tei.yaml" \
    --cache "./caches/referentiels-ancien-regime/indexations.yaml"
