source ../ENV

SOURCES=$REPOSITORIES/mercure-galant-sources/
SHERLOCK=$REPOSITORIES/mercure-galant-sources-sherlock/
cd $SOURCES
git pull origin main
cd ../..

rm $SHERLOCK/tei/log.txt
touch $SHERLOCK/tei/log.txt

SAXONJAR=$REPOSITORIES/SaxonHE12-4J/saxon-he-12.4.jar \
TEI_LIVRAISONS=$SHERLOCK/tei/livraisons \
TEI_LIVRAISONS_HEADERS=$SHERLOCK/tei/livraisons_headers \
TEI_ARTICLES=$SHERLOCK/tei/articles \
MGGHXML=$SOURCES/tei-edition \
sh $ROOT/sources-processors/mg-tei/mg-process-tei.sh

cd $SHERLOCK
git add --all ; git commit -m "🌴" ; git push -u origin main