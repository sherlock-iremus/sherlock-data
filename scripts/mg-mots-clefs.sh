# S'assurer que l'imbrication des mots-clefs est représentée par des multiples de 4 espaces
# Remplacer les tabulations par 4 espace
# Attention aux irrégularités, exemple TS timbale qui était précédé d'un espace et de deux tabulations

python3 ./rdfizers/mercure-galant/mg-mots-clefs.py \
    --txt ./sources/mercure-galant/mots-clefs_2021.04.15.txt \
    --ttl ./out/ttl/mg-mots-clefs.ttl \
    --cache "./caches/mercure-galant/cache-mots-clefs.yaml"