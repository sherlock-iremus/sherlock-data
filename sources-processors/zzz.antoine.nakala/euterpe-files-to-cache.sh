source ../ENV

python3 sources-processors/files-to-cache.py \
    --file_dir $REPOSITORIES/euterpe-data/images/ \
    --cache $ROOT/caches/nakala/euterpe.yaml