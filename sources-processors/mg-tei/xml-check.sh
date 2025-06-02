for f in $(ls $DIR/*.xml)
do
    xmllint --noout $f
done