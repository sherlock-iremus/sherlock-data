source ../ENV

ssh-add

ssh tbottini@data-iremus.huma-num.fr "curl -X DELETE -G http://localhost:3030/iremus/ --data-urlencode graph=http://data-iremus.huma-num.fr/graph/mercure-galant-tei"

ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl/mg"
scp "$ROOT/out/ttl/mg/tei.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/mg/tei.ttl
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/mg/tei.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/mercure-galant-tei"