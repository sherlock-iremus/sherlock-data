for f in ./Zarlino_1558/meiOldClefsAnalyse/*.mei
do
    python3 ./rdfizers/modality-tonality/mei2rdf/main.py \
        --input_mei_file $f \
        --cache ./caches/modality-tonality/mei.yaml \
        --output_mei_folder ./out/mei/modality-tonality/ \
        --output_ttl_folder ./out/ttl/modality-tonality/mei/
done