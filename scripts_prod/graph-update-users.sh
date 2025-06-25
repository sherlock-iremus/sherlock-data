source ../ENV

DATE=$(date '+%Y-%m-%d_%Hh%Mm%Ss')

mkdir -p $ROOT/out/ttl/users/

ssh tbottini@data-iremus.huma-num.fr "mkdir -p /home/tbottini/sherlock/ttl"


python3 $ROOT/rdfizers/orcid-user2rdf.py \
    --output_ttl $ROOT/out/ttl/users/users.ttl \
    --output_backup_ttl $ROOT/out/ttl/users/users.backup.$DATE.ttl

if [ $? -eq  0 ]
then
    # DELETE OBSOLETE USER GRAPH
    ssh tbottini@data-iremus.huma-num.fr "curl -X DELETE -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/users"

    # POST GENERATED USER DATA
    scp "$SCRIPTS_DIR/../out/ttl/users/users.ttl" tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/ttl
    ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/sherlock/ttl/users.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/users"
fi