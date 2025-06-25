# Push an image collection to nakala

Necessary env variable :
- NAKALA_API_KEY 
- REPOSITORIES : root folder containing sources

## Step 1: Create a cache from a local folder

The corresponding python script is `sources-processors/files-to-cache.py`. 
It takes two arguments :
- `file_dir` : path to the directory that contains images to push to nakala 
- `cache` : path to cache

## Step 2 : Upload images from cache data and store doi

The corresponding python script is `sources-processors/cache-to-nakala.py`.
It takes three arguments :
- `file_dir` : path to the directory that contains images to push to nakala 
- `cache` : path to cache
- `collection` : nakala collection identifier -> should be previously generated using nakala webapp

## Euterpe use case : 

```
bash scripts_make/euterpe-files-to-cache.sh
bash scripts_make/euterpe-cache-to-nakala.sh
```

Generated cache ( caches/nakala/euterpe.yaml ) should look like that :

```
1117289.jpg:
  nakala_doi: 10.34847/nkl.b0040n70
1117290.jpg:
  nakala_doi: 10.34847/nkl.09ddfwos
...
```