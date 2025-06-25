if [[ -z "${REPOSITORIES}" ]]; then
    >&2 echo "No REPOSITORIES environment variable"
    exit 1
fi

F18_MG_URI="http://data-iremus.huma-num.fr/id/336f0cc6-8eb0-4d5d-b1eb-c27674f8e479"
COLLECTION_URI="http://data-iremus.huma-num.fr/id/7dd7cb84-ad41-44e6-8044-155827d9ff76"


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TEI_FOLDER="$REPOSITORIES/mercure-galant-sources/tei/articles"


QUERY="
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX iremus: <http://data-iremus.huma-num.fr/id/>
PREFIX lrm: <http://iflastandards.info/ns/lrm/lrmoo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?F3_article_tei ?article_mg_identifier
WHERE {
  GRAPH ?g {
    <$F18_MG_URI> lrm:R10_has_member ?F1_livraison .
    ?F1_livraison lrm:R3_is_realised_in ?F2_livraison_tei .
    ?F2_livraison_tei crm:P148_has_component ?F2_article_tei .
	  ?F3_article_tei lrm:R4_embodies ?F2_article_tei .
    ?F3_article_tei crm:P2_has_type iremus:62b49ca2-ec73-4d72-aaf3-045da6869a15 . # E55 Fichier TEI
    ?F3_article_tei crm:P1_is_identified_by ?e42_id .
    ?e42_id crm:P2_has_type iremus:574ffe9e-525c-42f2-8188-329ba3c7231d . # E55 Identifiant mercure
    ?e42_id crm:P190_has_symbolic_content ?article_mg_identifier
  }
}
"

response=$(curl --data-urlencode "query=$QUERY" --location --globoff --request POST 'https://data-iremus.huma-num.fr/sparql')

echo "$response" | jq -c '.results.bindings[]' | while read -r item; do
    # Extract F2_article and article_label values from each binding
    F3_article=$(echo "$item" | jq -r '.F3_article_tei.value')
    article_label=$(echo "$item" | jq -r '.article_mg_identifier.value')

    # Generate JSON for each entry
    # Static values for F18 and E7
    tei_file="$TEI_FOLDER/${article_label##*/}.xml"
    tei_as_txt="$(xsltproc "$SCRIPT_DIR/remove-tags.xslt" "$tei_file")"

    filename="$SCRIPT_DIR/../../../out/mg/json-es/articles/${article_label##*/}.json"

    # Generate JSON for each entry and save it to the appropriate file
    cat <<EOF > "$filename"
{"index": {"_index": "text-index", "_id": "$F3_article"}}
{"F3": "$F3_article", "internal_project_identifier": "${article_label}", "F18": "$F18_MG_URI", "collection": "$COLLECTION_URI","text": "$tei_as_txt"} 
EOF

    echo "Saved JSON entry to $filename"
done