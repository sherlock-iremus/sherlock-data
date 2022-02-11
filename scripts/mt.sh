################################################################################
# SKOLEMISATION
################################################################################

mkdir -p ./out/ttl/mt/skolemized

# Analyses

f="modal-tonal-ontology/analysisOntology.rdf"
echo "[skolemisation] $f -> out/ttl/mt/skolemized/$(basename $f)"
python3 ./rdfizers/skolemisation/skolemisation.py \
    --inowl "$f" \
    --query "./rdfizers/skolemisation/skolemisation.sparql" \
    --outowl "./out/ttl/mt/skolemized/$(basename $f)" \
    --base ""

# Modèles historiques

for f in modal-tonal-ontology/historicalModels/*.owl
do
  echo "[skolemisation] $f -> out/ttl/mt/skolemized/$(basename $f)"
  python3 ./rdfizers/skolemisation/skolemisation.py \
    --inowl "$f" \
    --query "./rdfizers/skolemisation/skolemisation.sparql" \
    --outowl "./out/ttl/mt/skolemized/$(basename $f)" \
    --base ""
done

# python3 ./rdfizers/mt/zarlino.py \
#     --in_rdf "./modal-tonal-ontology/"

# python3 ./rdfizers/mt/prepare_data.py \
#   --analysis_ontology "./modal-tonal-ontology/analysisOntology.rdf" \
#   --historical_models_dir "./modal-tonal-ontology/historicalModels" \
#   --out_webportal_ttl "./out/ttl/mt-webportal-data.ttl" \
#   --out_skolemized "./out/ttl"