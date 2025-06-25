curl -sX POST http://localhost:3030/iremus/update --data-urlencode 'update=
DELETE {
  GRAPH <http://data-iremus.huma-num.fr/graph/mei> { ?s ?p ?o }
}
WHERE {
  GRAPH <http://data-iremus.huma-num.fr/graph/mei> {
    {
      SELECT ?s ?p ?o
      WHERE {
        ?s ?p ?o .
      }
      LIMIT 950000
    }
  }
}
'