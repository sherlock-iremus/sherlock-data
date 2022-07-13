mkdir -p ./caches/mercure-galant/
python3 ./rdfizers/mercure-galant/mg-sources-tei.py \
    --tei "./mercure-galant/xml" \
    --output_ttl "./out/ttl/mg-sources-tei.ttl" \
    --cache_tei "./caches/mercure-galant/cache-tei.yaml"
