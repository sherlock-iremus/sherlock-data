source ../ENV

ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl/mg"
scp "$ROOT/out/ttl/mg/estampes.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/mg/estampes.ttl
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/mg/estampes.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/mg-estampes"