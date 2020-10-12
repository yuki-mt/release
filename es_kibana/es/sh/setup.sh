#!/bin/bash
curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/test_index?pretty -d '
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "ngram_ja_tokenizer": {
          "type": "nGram",
          "min_gram": 2,
          "max_gram": 3,
          "token_chars": ["letter", "digit"]
        }
      },
      "filter": {
        "katakana_stemmer": {
          "type": "kuromoji_stemmer"
        }
      },
      "analyzer": {
        "ja": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "char_filter": [
            "html_strip",
            "kuromoji_iteration_mark"
          ],
          "filter": [
            "lowercase",
            "cjk_width",
            "katakana_stemmer",
            "kuromoji_part_of_speech"
          ]
        },
        "ja_ngram": {
          "type": "custom",
          "tokenizer": "ngram_ja_tokenizer",
          "char_filter": ["html_strip"],
          "filter": ["cjk_width", "lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "question": {
        "type": "text",
        "analyzer": "ja"
      },
      "answer": {
        "type": "keyword"
      }
    }
  }
}'
