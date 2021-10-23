Requêter le SPARQL endpoint http://data-iremus.huma-num.fr/sparql/ (par exemple, avec https://yasgui.triply.cc/).

Obtenir toutes les annotations signées par Kenza (http://data-iremus.huma-num.fr/id/e4e038d3-1417-4c7a-b2f7-e688615f2f15) :

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
BASE <http://data-iremus.huma-num.fr/id/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?sha1 ?mime ?tag_label
WHERE {
  GRAPH <http://data-iremus.huma-num.fr/graph/ceres> {
    ?e13 rdf:type crm:E13_Attribute_Assignment .
    ?e13 crm:P140_assigned_attribute_to ?media .
    ?e13 crm:P14_carried_out_by <e4e038d3-1417-4c7a-b2f7-e688615f2f15> .
    ?media dcterms:format ?mime .
    ?media crm:P1_is_identified_by ?e42_sha1 .
    ?e42_sha1 crm:P2_has_type <01de41ec-850f-473b-bd7f-268a18afc6a3> .
    ?e42_sha1 rdfs:label ?sha1 .
    ?e13 crm:P141_assigned/crm:P1_is_identified_by ?tag_label . 
  }
}
```

Consulter le vocabulaire de Kenza : http://data-iremus.huma-num.fr/id/4d90cb1b-4f16-4c31-8927-5faef7e74998