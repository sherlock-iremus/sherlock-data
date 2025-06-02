source ../ENV
ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl/refar"
scp "$ROOT/out/ttl/grist/refar-personnes.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/refar/personnes.ttl
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/refar/personnes.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/refar-personnes"