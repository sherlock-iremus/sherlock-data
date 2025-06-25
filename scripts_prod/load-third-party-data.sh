source ../ENV

ssh-add

ssh tbottini@data-iremus.huma-num.fr "rm -rf /home/tbottini/sherlock/rdf/third-party"
rm -rf $ROOT/out/rdf/third-party
mkdir -p $ROOT/out/rdf/third-party
ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/rdf/third-party/"
ssh tbottini@data-iremus.huma-num.fr "curl -X DELETE -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/third-party"
cd $ROOT/out/rdf/third-party

# https://github.com/philharmoniedeparis/mimo

ssh tbottini@data-iremus.huma-num.fr "cd /home/tbottini/sherlock/rdf/third-party && wget https://github.com/philharmoniedeparis/mimo/raw/master/our_data/03_skos/keywords_skos.rdf"
ssh tbottini@data-iremus.huma-num.fr "curl -X POST -H Content-Type:application/rdf+xml -T /home/tbottini/sherlock/rdf/third-party/keywords_skos.rdf -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/third-party"
curl -X POST -d "query=SELECT (COUNT(*) as ?c) WHERE { GRAPH <http://data-iremus.huma-num.fr/graph/third-party> { ?s ?p ?o } }" https://data-iremus.huma-num.fr/sparql

ssh tbottini@data-iremus.huma-num.fr "cd /home/tbottini/sherlock/rdf/third-party && wget https://github.com/philharmoniedeparis/mimo/raw/master/our_data/03_skos/hs_skos.rdf"
ssh tbottini@data-iremus.huma-num.fr "curl -X POST -H Content-Type:application/rdf+xml -T /home/tbottini/sherlock/rdf/third-party/hs_skos.rdf -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/third-party"
curl -X POST -d "query=SELECT (COUNT(*) as ?c) WHERE { GRAPH <http://data-iremus.huma-num.fr/graph/third-party> { ?s ?p ?o } }" https://data-iremus.huma-num.fr/sparql