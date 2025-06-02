source ../ENV

python3 sources-processors/cache-to-nakala.py \
    --file_dir $REPOSITORIES/euterpe-data/images/ \
    --cache $ROOT/caches/nakala/euterpe.yaml \
    --collection 10.34847/nkl.b58fc012
