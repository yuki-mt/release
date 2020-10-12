#!/bin/bash
# {"_id": 1}を {}にするとUUIDが自動で割り振られる
curl -X POST -H 'Content-Type: application/json' http://localhost:9200/test_index/_bulk?pretty -d '
{"index": {"_id": 1}}
{"question": "梅酒は水", "answer": "yes"}
{"index": {"_id": 2}}
{"question": "養命酒は水", "answer": "no"}
{"index": {"_id": 3}}
{"question": "私はリンゴが大好きです", "answer": "yes"}
{"index": {"_id": 4}}
{"question": "妹の好物は真っ赤なリンゴです", "answer": "no"}
'
