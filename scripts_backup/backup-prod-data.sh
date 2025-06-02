SCRIPTS_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE=$(date '+%Y-%m-%d_%Hh%Mm%Ss')
echo $DATE

BD=$SCRIPTS_DIR/../backups/$DATE
mkdir -p $BD
scp -r tbottini@bases-iremus.huma-num.fr:/home/tbottini/infra/data-* $BD