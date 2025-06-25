source ../ENV

scp "$ROOT/repositories/polifonia/tonalities_pilot/scripts/meihead-parser/tonalities-sherlock-projects.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/tonalities-sherlock-projects.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/tonalities-projects-and-corpuses"