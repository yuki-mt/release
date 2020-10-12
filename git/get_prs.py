"""
githubから関係あるPRを取得する

## 手順
- Access Tokenはここから取得: https://github.com/settings/tokens
- config.json.sample を参考にconfig.jsonを作成
- run file
    - 普通に結果をoutput: `python get_prs.py`
    - 定期的に取得して新しいものがあれば通知: `nohup python get_prs.py --cron &`
"""
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import base64
from typing import List, Dict, MutableSet
import os
import argparse
from time import sleep
import subprocess


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cron', action='store_true',
                        help="set the option if read PRs periodically")
    parser.add_argument('--period', '-p', default=600, type=int,
                        help='period to read PRs')  # in seconds
    return parser.parse_args()


def get_items(config) -> List[Dict]:
    def get_basic_auth(username, token):
        basic_user_and_pasword = base64.b64encode(f'{username}:{token}'.encode('utf-8'))
        return {"Authorization": "Basic " + basic_user_and_pasword.decode('utf-8')}

    result = []
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

        showed_up_ids = set()  # type: MutableSet[int]
        for item in items:
            if item['id'] in showed_up_ids:
                continue
            showed_up_ids.add(item['id'])
            item['id'] = f"{c['host']}-{item['id']}"
            result.append(item)
    return result


def notify(current_ids: MutableSet[str], items: List[Dict]):
    contents = []
    for item in items:
        if item['id'] not in current_ids:
            contents.append(item['title'])
    if contents:
        content = '\n'.join(contents)
        app_command = f'display notification "{content}" with title "New Pull Requests"'
        command = f"osascript -e '{app_command}'"
        subprocess.call(command, shell=True)


def print_item(item: Dict):
    print('-' * 15)
    print('Repository:', item['repository_url'].split('/')[-1])
    print('Title:', item['title'])


def main():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')) as f:
        config = json.loads(f.read())
    args = get_args()
    if args.cron:
        current_ids = set()  # type: MutableSet[str]
        while True:
            items = get_items(config)
            notify(current_ids, items)
            current_ids = set(item['id'] for item in items)
            sleep(args.period)
    else:
        for item in get_items(config):
            print_item(item)


if __name__ == '__main__':
    main()
