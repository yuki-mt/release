"""
githubから関係あるPRを取得する

## 手順
- Access Tokenはここから取得: https://github.com/settings/tokens
- config.json.sample を参考にconfig.jsonを作成
- run `python get_prs.py`
"""
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import base64
from typing import List, Dict, MutableSet
import os


CURDIR = os.path.abspath(os.path.dirname(__file__))


def get_basic_auth(username, token):
    basic_user_and_pasword = base64.b64encode(f'{username}:{token}'.encode('utf-8'))
    return {"Authorization": "Basic " + basic_user_and_pasword.decode('utf-8')}


with open(os.path.join(CURDIR, 'config.json')) as f:
    config = json.loads(f.read())

for c in config:
    if c["host"] == 'github.com':
        base_url = 'https://api.github.com/search/issues'
    else:
        # for Gitlab
        base_url = f'https://{c["host"]}/api/v3/search/issues'

    items = []  # type: List[Dict]
    for pr_type in ['mentions', 'review-requested', 'assignee']:
        param = urlencode({'q': f'type:pr state:open {pr_type}:{c["username"]}'})
        req = Request(f'{base_url}?{param}', headers=get_basic_auth(c['username'], c['access_token']))
        with urlopen(req) as res:
            items.extend(json.loads(res.read().decode('utf-8'))['items'])

    showed_up_titles = set()  # type: MutableSet[str]
    for item in items:
        title = item['title']
        if title in showed_up_titles:
            continue
        print('-' * 15)
        print('Repository:', item['repository_url'].split('/')[-1])
        print('Title:', title)
        showed_up_titles.add(title)
