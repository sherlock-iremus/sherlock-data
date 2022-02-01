clear

echo "1. TEI"
$(pwd)/scripts/mg-sources-tei.sh

echo "2. INDEXATION STAGIAIRES"
$(pwd)/scripts/mg-indexations-stagiaires.sh

echo "3. VOCABULAIRE ESTAMPES  — ⚠️ Ne pas oublier de télécharger : https://docs.google.com/spreadsheets/d/1wS9punldFYlqZpkRgEsDXUSPRH1CDhdPKJYwjMXq_sw"
$(pwd)/scripts/mg-vocabulaire-estampes.sh

echo "4. ESTAMPES              — ⚠️ Ne pas oublier de télécharger : https://docs.google.com/spreadsheets/d/1xI4XzA_PTOOz1rsHCpJMwxj5sNZQsJtDGr2ZcGEht4g"
$(pwd)/scripts/mg-sources-estampes.sh

echo "5. GRAVURES MUSIQUE      — ⚠️ git submodule update --remote --merge"
$(pwd)/scripts/mg-sources-musique.sh

echo "6. INDEXATION MUSIQUE    — ⚠️ Ne pas oublier de télécharger : https://docs.google.com/spreadsheets/d/1-yGC85Wq-cj4WSkNOb2pvHsxYJk0aHbYxMkupNKc2-M"
$(pwd)/scripts/mg-indexation-musicale.sh

echo "7. MOTS CLEFS            — ⚠️ Ne pas oublier de télécharger le fichier SKOS OpenTheso"
# $(pwd)/scripts/mg-mots-clefs.sh