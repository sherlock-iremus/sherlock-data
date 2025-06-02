curl -sX POST http://localhost:3030/iremus/update --data-urlencode 'update=
DELETE WHERE {
  GRAPH <http://data-iremus.huma-num.fr/graph/sherlock> {
    ?s ?p ?o
  }
}
'

# curl -X POST -d "query=SELECT (COUNT(*) as ?c) ?g WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g" https://data-iremus.huma-num.fr/sparql