source ../ENV

ssh-add

mkdir -p $ROOT/out/ttl/concatenated
rm $ROOT/out/ttl/concatenated/euterpe.ttl
cat $ROOT/out/ttl/grist/projects/euterpe-*.ttl > $ROOT/out/ttl/concatenated/euterpe.ttl

ssh tbottini@data-iremus.huma-num.fr "curl -X DELETE -G http://localhost:3030/iremus/ --data-urlencode graph=http://data-iremus.huma-num.fr/graph/euterpe"

ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl/euterpe"
scp "$ROOT/out/ttl/concatenated/euterpe.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl/euterpe/euterpe.ttl
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/euterpe/euterpe.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/euterpe"