SCRIPTDIR=$(realpath $(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd))

trap "exit" INT

file_name () {
	filename=$(basename "$1")
	extension="${filename##*.}"
	filename="${filename%.*}"

	echo $filename
}

format_xml_file () {
  xmllint --format --noblanks $1 | tr -d '\n\r\t' | sed 's/  */ /g' > $1.f
  mv $1.f $1
  xmllint --format $1 > $1.f
  mv $1.f $1
  
  echo $1
}

rm -rf $TEI_LIVRAISONS
mkdir -p $TEI_LIVRAISONS
rm -rf $TEI_LIVRAISONS_HEADERS
mkdir -p $TEI_LIVRAISONS_HEADERS
rm -rf $TEI_ARTICLES
mkdir -p $TEI_ARTICLES

for f in $(ls $MGGHXML/*.xml)
do
  livraison_id=$(file_name $f)
  livraison_id="${livraison_id/MG-/}"
  echo $livraison_id

  # COPIE DE TRAVAIL DE LA LIVRAISON
  f_temp=$TEI_LIVRAISONS/$livraison_id.temp.xml
  cp $f $f_temp

  # FORMATAGE DES LIVRAISONS
  formatted_file=$(format_xml_file $f_temp)

  # RÉÉCRITURE DES LIVRAISONS
  java -jar $SAXONJAR -s:$f_temp -xsl:"$SCRIPTDIR"/extract-text.xslt -o:$TEI_LIVRAISONS/$livraison_id.xml
  
  # EXTRACTION DES HEADERS
  java -jar $SAXONJAR -s:$f_temp -xsl:"$SCRIPTDIR"/extract-header.xslt -o:$TEI_LIVRAISONS_HEADERS/$livraison_id.header.xml
  
  # FRAGMENTATION DES FICHIERS TEI
  java -jar $SAXONJAR -s:$f_temp -xsl:"$SCRIPTDIR"/extract-articles.xslt -o:$TEI_ARTICLES/TOKILL.xml
  rm $TEI_ARTICLES/TOKILL.xml

  rm $f_temp

  # RENOMMAGE ET FORMATAGE DES ARTICLES TEI
  for f in $(ls $TEI_ARTICLES/MG-$livraison_id*)
  do
    dir=$(dirname "$f")
    base=$(basename "$f")
    newbase="${base/MG-/}"
    mv "$f" "$dir/$newbase"
    f="$dir/$newbase"
    x=$(format_xml_file $f)
    echo "  " $(basename -s .xml $newbase)
  done
done