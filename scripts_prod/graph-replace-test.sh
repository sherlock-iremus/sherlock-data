source ../ENV

ssh-add

ssh tbottini@data-iremus.huma-num.fr "curl -X DELETE -G http://localhost:3030/iremus/ --data-urlencode graph=http://data-iremus.huma-num.fr/graph/test"

ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl/test"
scp "$ROOT/data-ttl/test.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/test/test.ttl
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/test/test.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/test"