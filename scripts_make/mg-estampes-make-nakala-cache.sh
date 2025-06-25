source ../ENV

mkdir -p $ROOT/caches/mg

python3 $ROOT/sources-processors/mg-estampes-make-nakala-cache.py \
    --cache_estampes caches/mg/estampes.yaml \
    --cache_nakala caches/mg/id.yaml \