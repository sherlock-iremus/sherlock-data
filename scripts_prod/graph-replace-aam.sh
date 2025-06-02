source ../ENV

ssh-add

ssh tbottini@data-iremus.huma-num.fr "curl -X DELETE -G http://localhost:3030/iremus/ --data-urlencode graph=http://data-iremus.huma-num.fr/graph/aam"

ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl/aam"
scp "$ROOT/out/ttl/grist/aam.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/aam/aam.ttl
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/aam/aam.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/aam"