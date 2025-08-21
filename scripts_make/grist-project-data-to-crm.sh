source ../ENV

mkdir -p $ROOT/out/ttl/grist/projects/

case "$1" in
    "aam")
        python3 $ROOT/rdfizers/grist-2-crm.py \
            --grist_base https://musicodb.sorbonne-universite.fr/api \
            --grist_api_key $GRIST_API_KEY \
            --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
            --grist_table_id 8 \
            --project_id aam \
            --sherlock_collection c583a908-30da-4d05-b0b1-dec8d3401a1e \
            --output_ttl $ROOT/out/ttl/grist/projects/aam.ttl \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object \
            --e13_authors 447b85ae-53c6-4787-8f63-4c9118023c92,4b310d11-24e4-41b6-b8e3-4fa223ff8fae \
            --rdf_properties_grist_table_id 34 \
            --grist_e13_e55_table_id 15 \
            --grist_e41_e55_table_id 32 \
            --grist_e42_e55_table_id 29 \
            --grist_p3_e55_table_id 30 \
            --makerdfslabelfrom aam::nom,aam::prenom,aam::qualite \
        ;;
    "euterpe-oeuvres")
        python3 $ROOT/rdfizers/grist-2-crm.py \
            --grist_base https://musicodb.sorbonne-universite.fr/api \
            --grist_api_key $GRIST_API_KEY \
            --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
            --grist_table_id 5 \
            --project_id euterpe \
            --sherlock_collection b77c7bb2-25e7-4003-8d6d-8b12a722c30b \
            --output_ttl $ROOT/out/ttl/grist/projects/euterpe-oeuvres.ttl \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E36_Visual_Item \
            --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
            --rdf_properties_grist_table_id 34 \
            --grist_e13_e55_table_id 15 \
            --grist_e42_e55_table_id 29 \
            --grist_e41_e55_table_id 32 \
            --grist_p3_e55_table_id 30 \
        ;;
    "euterpe-personnes")
        python3 $ROOT/rdfizers/grist-2-crm.py \
            --grist_base https://musicodb.sorbonne-universite.fr/api \
            --grist_api_key $GRIST_API_KEY \
            --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
            --grist_table_id 31 \
            --project_id euterpe \
            --sherlock_collection 48e1830b-f181-4cc6-8ab2-55cbf621e210 \
            --output_ttl $ROOT/out/ttl/grist/projects/euterpe-personnes.ttl \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
            --rdf_properties_grist_table_id 34 \
            --grist_e13_e55_table_id 15 \
            --grist_e42_e55_table_id 29 \
            --grist_e41_e55_table_id 32 \
            --grist_p3_e55_table_id 30 \
        ;;
    "mg-livraisons")
        python3 $ROOT/rdfizers/grist-2-crm.py \
            --grist_base https://musicodb.sorbonne-universite.fr/api \
            --grist_api_key $GRIST_API_KEY \
            --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
            --grist_table_id 19 \
            --project_id mg-tei \
            --sherlock_collection f252113e-7480-43dd-a48f-0f4d07176eab \
            --output_ttl $ROOT/out/ttl/grist/projects/mg-livraisons.ttl \
            --rdf_type http://iflastandards.info/ns/lrm/lrmoo/F2_Expression \
            --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
            --rdf_properties_grist_table_id 34 \
            --grist_e13_e55_table_id 15 \
            --grist_e42_e55_table_id 29 \
            --grist_e41_e55_table_id 32 \
            --grist_p3_e55_table_id 30 \
        ;;
    "refar-personnes")
        python3 $ROOT/rdfizers/grist-2-crm.py \
            --grist_base https://musicodb.sorbonne-universite.fr/api \
            --grist_api_key $GRIST_API_KEY \
            --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
            --grist_table_id 1 \
            --project_id refar-personnes \
            --output_ttl $ROOT/out/ttl/grist/projects/refar-personnes.ttl \
            --e32_uuid 81366968-0fc8-43f6-9a32-9609c19a33c0 \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
            --rdf_properties_grist_table_id 34 \
            --grist_e13_e55_table_id 15 \
            --grist_e41_e55_table_id 32 \
            --grist_e42_e55_table_id 29 \
            --grist_p3_e55_table_id 30 \
        ;;
    *)
        echo "Unknown project code: \"$1\""
        ;;
esac

# # AAAD
# python3 $ROOT/rdfizers/grist-2-crm.py \
#     --grist_api_key $GRIST_API_KEY \
#     --grist_doc_id 4NmEJA4z9EUBK2vYu2epCi \
#     --grist_table_id 10 \ti
#     --sherlock_project_code aaad \
#     --output_ttl $ROOT/out/ttl/grist/projects/aaad.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object \
#     --e13_authors 447b85ae-53c6-4787-8f63-4c9118023c92,4b310d11-24e4-41b6-b8e3-4fa223ff8fae