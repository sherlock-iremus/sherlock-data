mkdir -p ./caches/referentiels-ancien-regime
python3 ./rdfizers/referentiels-ancien-regime/lieux.py \
  --inputrdf "./sources/referentiels-ancien-regime/thesaurus_lieux.rdf" \
  --output_ttl "./out/ttl/rar-lieux.ttl" \
  --cache_tei "./caches/mercure-galant/cache-tei.yaml" \
  --cache_lieux "./caches/referentiels-ancien-regime/cache-lieux.yaml" \
  --label_uuid "./out/rar-lieux-label-uuid.yaml"