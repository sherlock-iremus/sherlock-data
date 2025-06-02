source ../ENV

source ./my-venv/bin/activate

python3 $ROOT/sources-processors/mg-tei-to-grist.py \
    --tei-articles $REPOSITORIES/mercure-galant-sources-sherlock/tei/articles \
    --tei-livraisons $REPOSITORIES/mercure-galant-sources-sherlock/tei/livraisons \
    --tei-livraisons-headers $REPOSITORIES/mercure-galant-sources-sherlock/tei/livraisons_headers \
    --grist-api-key $GRIST_API_KEY \
    --grist-doc-id 4NmEJA4z9EUB \
    --articles-grist-table-id 18 \
    --livraisons-grist-table-id 19 \
