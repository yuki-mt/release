## Build simple local server

```
cd server
npm install
npm install -g nodemon
npm run dev
```

## Sample Requests

```
$ curl http://localhost:3000/check\?hoge\=fuga
{
  "query_string": {
    "hoge": "fuga"
  },
  "reqest_headers": {
    "host": "localhost:3000",
    "user-agent": "curl/7.54.0",
    "accept": "*/*"
  }
}

$ curl -H 'Content-Type:application/json'  -d '{"token": "hoge"}' http://localhost:3000/check
{
  "body_or_form": {
    "token": "hoge"
  },
  "reqest_headers": {
    "host": "localhost:3000",
    "user-agent": "curl/7.54.0",
    "accept": "*/*",
    "content-type": "application/json",
    "content-length": "17"
  }
}

$ curl http://localhost:3000/json/users
[
  {
    "id": 1,
    "name": "test"
  },
  {
    "id": 2,
    "name": "sample"
  }
]
```

[detail for JSON Server](https://qiita.com/futoase/items/2859a60c8b240da70572)

## Build simple server to Heroku
