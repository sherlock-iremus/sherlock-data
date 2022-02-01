mkdir -p ./caches/referentiels-ancien-regime
python3 ./rdfizers/referentiels-ancien-regime/personnes.py \
  --inputrdf "./sources/referentiels-ancien-regime/thesaurus_personnes.rdf" \
  --output_ttl "./out/ttl/rar-personnes.ttl" \
  --cache_tei "./caches/mercure-galant/cache-tei.yaml" \
  --cache_personnes "./caches/referentiels-ancien-regime/cache-personnes.yaml"