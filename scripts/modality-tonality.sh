# Analyses

f="modal-tonal-ontology/analysisOntology.rdf"

python3 ./rdfizers/modality-tonality/analysis.py \
   --analysis_ontology "./modal-tonal-ontology/analysisOntology.rdf" \
   --cache "./caches/modality-tonality_analysis.yaml" \
   --out_ttl "./out/ttl/modality-tonality/analysis.ttl" \
   --historical_models_dir "./modal-tonal-ontology/historicalModels" \
   --researcher_uuid "fccdf69c-4d6b-482e-869c-785551482dc2"