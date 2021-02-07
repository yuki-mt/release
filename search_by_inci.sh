# 化粧品の成分検索

urlencode () {
  echo "$1" | nkf -WwMQ | tr '\n' % | sed -e "s/=%//g" | sed -e "s/%//g" | tr = %
}

search_by_inci(){
  word=`urlencode $1`
  PHPSESSID=$(curl 'https://www.jcia.org/user/business/ingredients/search' \
    -H 'Connection: keep-alive' \
    -H 'Accept: */*' \
    -H 'X-Requested-With: XMLHttpRequest' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
    -H 'Origin: https://www.jcia.org' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Referer: https://www.jcia.org/user/business/ingredients/namelist' \
    -H 'Accept-Language: ja,en-US;q=0.9,en;q=0.8' \
    --data-raw "search%5Bfreeword%5D=$word" \
    --compressed -i | grep 'Set-Cookie: PHPSESSID=' | cut -d '='  -f2 | cut -d ';' -f1)

  curl 'https://www.jcia.org/user/business/ingredients/list/page/0' \
       -H 'Connection: keep-alive' \
       -H 'Accept: text/plain, */*; q=0.01' \
       -H 'sec-ch-ua-mobile: ?0' \
       -H 'X-Requested-With: XMLHttpRequest' \
       -H 'Sec-Fetch-Site: same-origin' \
       -H 'Sec-Fetch-Mode: cors' \
       -H 'Sec-Fetch-Dest: empty' \
       -H 'Referer: https://www.jcia.org/user/business/ingredients/namelist' \
       -H 'Accept-Language: ja,en-US;q=0.9,en;q=0.8' \
       -H 'Cookie: PHPSESSID='$PHPSESSID';' \
       --compressed
}
search_by_inci "1,10-DECANEDIOL"
