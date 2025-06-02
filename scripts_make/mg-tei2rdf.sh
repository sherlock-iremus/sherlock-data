source ../ENV

cd $REPOSITORIES/mercure-galant-sources/
git pull origin main
cd ../..

mkdir -p $ROOT/out/ttl/mg/

python3 $ROOT/rdfizers/mg-tei2rdf.py \
    --tei $REPOSITORIES/mercure-galant-sources/tei-edition \
    --output_ttl $ROOT/out/ttl/mg/tei.ttl \
    --cache_tei $ROOT/caches/mg/tei.yaml