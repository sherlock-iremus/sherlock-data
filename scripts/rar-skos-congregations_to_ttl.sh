mkdir -p ./caches/referentiels-ancien-regime
python3 ./rdfizers/referentiels-ancien-regime/congregations-skos_to_ttl.py \
    --input_rdf "./sources/referentiels-ancien-regime/thesaurus_congregations.rdf" \
    --output_ttl "./out/ttl/rar-congregations.ttl" \
    --cache_tei "./caches/mercure-galant/cache-tei.yaml" \
    --cache_congregations "./caches/referentiels-ancien-regime/cache-congregations.yaml" \
    --cache_lieux_uuid "./out/rar-lieux-label-uuid.yaml" \
    --situation_geo "./sources/referentiels-ancien-regime/congregations_situation_geohistorique.txt"