mkdir -p ./caches/mercure_galant/
python3 ./rdfizers/mercure_galant/main.py \
    --tei "./mercure-galant/xml" \
    --output_ttl "./out/mg-sources-tei.ttl" \
    --corpus_cache "./caches/mercure_galant/cache_corpus.yaml"
