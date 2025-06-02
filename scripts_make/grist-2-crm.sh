source ../ENV

mkdir -p $ROOT/caches/mg

# ReFAR::Personnes
# python3 $ROOT/rdfizers/grist-2-crm.py \
#     --grist_api_key $GRIST_API_KEY \
#     --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
#     --grist_table_id 1 \
#     --sherlock_project_code refar \
#     --output_ttl $ROOT/out/ttl/grist/refar-personnes.ttl \
#     --e32_uuid 81366968-0fc8-43f6-9a32-9609c19a33c0 \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person

# # AAAD
# python3 $ROOT/rdfizers/grist-2-crm.py \
#     --grist_api_key $GRIST_API_KEY \
#     --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
#     --grist_table_id 10 \
#     --sherlock_project_code aaad \
#     --output_ttl $ROOT/out/ttl/grist/aaad.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object \
#     --e13_authors 447b85ae-53c6-4787-8f63-4c9118023c92,4b310d11-24e4-41b6-b8e3-4fa223ff8fae

# AAM
python3 $ROOT/rdfizers/grist-2-crm.py \
    --grist_api_key $GRIST_API_KEY \
    --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
    --grist_table_id 8 \
    --sherlock_project_code aam \
    --sherlock_corpus c583a908-30da-4d05-b0b1-dec8d3401a1e \
    --sherlock_e13_e55_ttl $ROOT/out/ttl/grist/sherlock-e13-e55.ttl \
    --output_ttl $ROOT/out/ttl/grist/aam.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object \
    --e13_authors 447b85ae-53c6-4787-8f63-4c9118023c92,4b310d11-24e4-41b6-b8e3-4fa223ff8fae