# SKOLEMISATION

mkdir -p ./out/ttl/tonalities

for f in modal-tonal-ontology/historicalModels/*.owl
do
  echo "skolemisation $f -> out/ttl/tonalities/$(basename $f)"
  python3 ./rdfizers/skolemisation/skolemisation.py \
    --inowl "$f" \
    --query "./rdfizers/skolemisation/skolemisation.sparql" \
    --outowl "./out/ttl/tonalities/$(basename $f)" \
    --base ""
done

# python3 ./rdfizers/tonalities/zarlino.py \
#     --in_rdf "./modal-tonal-ontology/"

# python3 ./rdfizers/tonalities/prepare_data.py \
#   --analysis_ontology "./modal-tonal-ontology/analysisOntology.rdf" \
#   --historical_models_dir "./modal-tonal-ontology/historicalModels" \
#   --out_webportal_ttl "./out/ttl/tonalities-webportal-data.ttl" \
#   --out_skolemized "./out/ttl"