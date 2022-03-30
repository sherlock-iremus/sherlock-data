python3 ./rdfizers/catalogues-des-livres-du-roi/create-json.py \
    --xlsx1 "./sources/catalogues-des-livres-du-roi/Fichier livrets-1660-1714-V11.xlsx" \
    --xlsx2 "./sources/catalogues-des-livres-du-roi/Fichier livrets-1725-1792-V11.xlsx" \
    --photos "./sources/catalogues-des-livres-du-roi/photos" \
    --cache ./caches/catalogues-des-livres-du-roi/cache-json.yaml \
    --json ./out/catalogues-des-livres-du-roi.json