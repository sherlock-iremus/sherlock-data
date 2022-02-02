clear

echo "1. PERSONNES"
$(pwd)/scripts/rar-directus-personnes_to_ttl.sh

echo "2. TOPONYMES"
$(pwd)/scripts/rar-directus-lieux_to_ttl.sh