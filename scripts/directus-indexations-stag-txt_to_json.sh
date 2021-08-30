python3 ./directus/mg-indexations-stagiaires/indexations-stagiaires-txt_to_json.py \
    --txt "./sources/mercure-galant/indexation-stagiaires/" \
    --cache_personnes "./caches/referentiels-ancien-regime/cache-personnes.yaml" \
    --cache_lieux "./caches/referentiels-ancien-regime/cache-lieux.yaml" \
    --cache_congregations "./caches/referentiels-ancien-regime/cache-congregations.yaml" \
    --cache_mots_clefs "./caches/mercure-galant/cache-mots-clefs.yaml" \
    --json_indexations_personnes "./temp/mercure-galant/directus/indexations-stagiaires-personnes.json" \
    --json_indexations_lieux "./temp/mercure-galant/directus/indexations-stagiaires-lieux.json" \
    --json_indexations_congregations "./temp/mercure-galant/directus/indexations-stagiaires-congregations.json" \
    --json_indexations_mots_clefs "./temp/mercure-galant/directus/indexations-stagiaires-mots-clefs.json"
