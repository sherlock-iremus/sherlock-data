source ../ENV

source $ROOT/my-venv/bin/activate

rm -rf $ROOT/out/ttl/grist/sherlock
mkdir -p $ROOT/out/ttl/grist/sherlock

# Projets
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 16 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PROJECTS.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E7_Activity \
    --P2_has_type http://data-iremus.huma-num.fr/id/58c38fd3-ca35-476a-aa39-9cc815ee2dab \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \

# Collections
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 17 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-COLLECTIONS.ttl \
    --rdf_type http://data-iremus.huma-num.fr/ns/sherlock#Collection \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \

# Fichiers des projets
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 35 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E31_Document \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PROJECTS-FILES.ttl \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \

# E41 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 32 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E41-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \

# E42 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 29 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E42-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \

# E13 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 15 \
    --e32_uuid 3abbb495-7105-4066-89fe-9d4b0474e492 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E13-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \

# P3 E55
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_base https://musicodb.sorbonne-universite.fr/api \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 30 \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-P3-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    --rdf_properties_grist_table_id 34 \
    --grist_e42_e55_table_id 29 \