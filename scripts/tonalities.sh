# TODO skolemisation des ontologies

# python3 ./rdfizers/tonalities/zarlino.py \
#     --in_rdf "./modal-tonal-ontology/"

python3 ./rdfizers/tonalities/mto2webportal.py \
  --analysis_ontology "./modal-tonal-ontology/analysisOntology.rdf" \
  --historical_models_dir "./modal-tonal-ontology/historicalModels" \
  --out_ttl "./out/ttl/tonalities-webportal-data.ttl"