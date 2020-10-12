#!/bin/bash
csv_file=$1
result=''
while IFS=, read -r col1 col2
do
  result=$result"{\"index\": {}}\n{\"question\": \"$col1\", \"answer\": \"$col2\"}\n"
done < $csv_file

echo -e "$result" > bulk.json

curl -X POST -H 'Content-Type: application/json' http://localhost:9200/test_index/_bulk?pretty --data-binary @bulk.json

rm bulk.json
