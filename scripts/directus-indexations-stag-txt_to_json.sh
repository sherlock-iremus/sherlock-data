python3 ./directus/mg-indexations-stagiaires/indexations-stagiaires-txt_to_json.py \
    --txt "./sources/mercure-galant/indexation-stagiaires/" \
    --cache_personnes "./caches/referentiels-ancien-regime/cache-personnes.yaml" \
    --cache_lieux "./caches/referentiels-ancien-regime/cache-lieux.yaml" \
    --cache_institutions "./caches/referentiels-ancien-regime/cache-institutions.yaml" \
    --cache_congrégations "./caches/referentiels-ancien-regime/cache-congregations.yaml" \
    --cache_mots_clés "./caches/mercure-galant/cache-mots-clefs.yaml" \
    --json_indexations_personnes "./temp/mercure-galant/directus/indexations-stagiaires-personnes.json" \
