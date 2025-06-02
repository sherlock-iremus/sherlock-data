SCRIPTS_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE=$(date '+%Y-%m-%d_%Hh%Mm%Ss')
echo $DATE

BD=$SCRIPTS_DIR/../backups/TTL-$DATE
mkdir -p $BD

ssh tbottini@data-iremus.huma-num.fr 'curl --data-urlencode "query=CONSTRUCT { ?s ?p ?o } WHERE { GRAPH <http://data-iremus.huma-num.fr/graph/users> { ?s ?p ?o } }" http://localhost:3030/iremus/sparql' > $BD/users.ttl