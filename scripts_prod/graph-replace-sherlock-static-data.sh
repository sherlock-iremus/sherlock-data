source ../ENV

rm $ROOT/out/ttl/sherlock-static-data.ttl
cat $ROOT/data-ttl/*.ttl $ROOT/out/ttl/grist/sherlock-e13-e55.ttl $ROOT/out/ttl/grist/sherlock-projects.ttl > $ROOT/out/ttl/sherlock-static-data.ttl

scp "$ROOT/out/ttl/sherlock-static-data.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/sherlock-static-data.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/sherlock-static-data"

rm $ROOT/out/ttl/sherlock-static-data.ttl