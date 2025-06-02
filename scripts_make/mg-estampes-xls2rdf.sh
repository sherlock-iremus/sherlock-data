source ../ENV

mkdir -p $ROOT/out/ttl/mg/

python3 $ROOT/rdfizers/mg-estampes-xls2rdf.py \
    --cache_estampes $ROOT/caches/mg/estampes.yaml \
    --cache_tei $ROOT/caches/mg/tei.yaml \
    --directus_secret $ROOT/secret/directus.refar.yaml \
    --opentheso_id th391 \
    --ttl $ROOT/out/ttl/mg/estampes.ttl \
    --xlsx $ROOT/in/mercure-galant-sources-github/indexation-estampes.xlsx \