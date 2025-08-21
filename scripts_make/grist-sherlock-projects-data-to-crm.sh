source ../ENV

source $ROOT/my-venv/bin/activate

rm -rf $ROOT/out/ttl/grist/sherlock
mkdir -p $ROOT/out/ttl/grist/sherlock

# E21 Personnes
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_PERSONNES \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PERSONNES.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# Projets
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_PROJETS \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PROJECTS.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E7_Activity \
    --P2_has_type http://data-iremus.huma-num.fr/id/58c38fd3-ca35-476a-aa39-9cc815ee2dab \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# Collections
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_COLLECTIONS \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-COLLECTIONS.ttl \
    --rdf_type http://data-iremus.huma-num.fr/ns/sherlock#Collection \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# Fichiers des projets
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_PROJETS_FICHIERS \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E31_Document \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PROJECTS-FILES.ttl \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# E41 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_E41 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E41-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# E42 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_E42 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E42-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# E13 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_E13 \
    --e32_uuid 3abbb495-7105-4066-89fe-9d4b0474e492 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E13-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \

# P3 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id SHERLOCK_P3 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-P3-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --grist_e42_e55_table_id SHERLOCK_E42 \
    --rdf_properties_grist_table_id SHERLOCK_RDF_PREDICATS \
