for i in `seq 8`
do
  curl -u ymatoba:$TOKEN https://api.github.com/orgs/$ORG/repos\?page\=$i | jq -r '.[].name' >> repo.json
done
