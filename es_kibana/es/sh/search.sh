#!/bin/bash
curl -X POST -H 'Content-Type: application/json' http://localhost:9200/test_index/_search?pretty -d '
{
  "explain": false,
  "query": {
    "match": {
      "question": "ISMS"
    }
  }
}'
