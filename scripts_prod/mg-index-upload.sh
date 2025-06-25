if [[ -z "${REPOSITORIES}" ]]; then
    >&2 echo "No REPOSITORIES environment variable"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATA_DIR="$SCRIPT_DIR/../out/mg/json-es/articles/"

output_file="mg.json"
> "$output_file"

for json_file in "$DATA_DIR"/*.json; do
  if [ -f "$json_file" ]; then
    cat "$json_file" >> "$output_file"
    echo "" >> "$output_file"  # Add a newline after each JSON content
  fi
done

ssh tbottini@data-iremus.huma-num.fr "rm /home/tbottini/sherlock/es-data/mg.json"
scp $output_file tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/es-data/mg.json
rm $output_file
# ssh bash home/tbottini/elastic-search/upload-index.sh