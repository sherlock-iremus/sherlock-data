clear

echo "1. PERSONNES"
$(pwd)/scripts/rar-directus-personnes_to_ttl.sh

echo "2. TOPONYMES"
$(pwd)/scripts/rar-directus-lieux_to_ttl.sh

echo "3. INDEXATION"
$(pwd)/scripts/rar-directus-indexations_to_ttl.sh