query="SELECT average(duration) FROM PageView"
key="YOUR_KEY"
ACCOUNT="YOUR_ACCOUNT_NUM"

urlencode () {
  echo "$@" | nkf -WwMQ | tr '\n' % | sed -e "s/=%//g" | sed -e "s/%//g" | tr = %
}

curl -H "Accept: application/json" \
  -H "X-Query-Key: $key" \
  "https://insights-api.newrelic.com/v1/accounts/{YOUR_ACCOUNT_NUM}/query?nrql=$(urlencode $query)"
