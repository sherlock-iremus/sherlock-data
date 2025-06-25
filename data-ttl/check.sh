for i in $(find . -name "*.ttl")
do
  echo $i $(ttl $i) | grep -v "0 errors"
done
