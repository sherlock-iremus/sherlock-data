python3 ./rdfizers/modality-tonality/analysis.py \
   --analysis_ontology "./modal-tonal-ontology/analysisOntology.rdf" \
   --cache "./caches/modality-tonality/analysis.yaml" \
   --mei_cache "./caches/modality-tonality/mei.yaml" \
   --out_ttl "./out/ttl/modality-tonality/analysis.ttl" \
   --historical_models_dir "./modal-tonal-ontology/historicalModels" \
   --researcher_uuid "fccdf69c-4d6b-482e-869c-785551482dc2"

cd ./out/ttl/modality-tonality/
echo "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n$(cat analysis.ttl)" > analysis.ttl
cd -