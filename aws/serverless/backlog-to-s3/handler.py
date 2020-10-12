import os
from urllib.parse import urlparse
import shutil
import json
import base64

import boto3
from dulwich import porcelain
from dulwich import index

TARGET = '/tmp/my-repo'
TARGET_BRANCH = 'master'
GIT_USERNAME = os.environ['USER_NAME']
GIT_PW = os.environ['PASSWORD']
S3_BUCKET = os.environ['BUCKET_NAME']
S3_PREFIX = os.environ['S3_PREFIX']
BASIC_USERNAME = os.environ['BASIC_USERNAME']
BASIC_PW = os.environ['BASIC_PASSWORD']

def git_clone(repo_url):
    print('repo URL:', repo_url)
    parsed_url = urlparse(repo_url)
    src = f'{parsed_url.scheme}://{GIT_USERNAME}:{GIT_PW}@{parsed_url.netloc}{parsed_url.path}.git'

    if not os.path.isdir(TARGET):
        os.mkdir(TARGET)
    else:
        shutil.rmtree(TARGET)
    return porcelain.clone(src, TARGET, depth=1)

def git_checkout(local_repo, commit):
    print('commit sha:', commit)
    local_repo[b"HEAD"] = commit.encode()
    index_file = local_repo.index_path()
    tree = local_repo[b"HEAD"].tree
    index.build_index_from_tree(local_repo.path, index_file, local_repo.object_store, tree)

def zip_files():
    print('zip repository files')
    shutil.make_archive(TARGET, 'zip', TARGET)

def upload_to_s3():
    print('upload the zip file to S3')
    filename = TARGET.split('/')[-1]
    s3 = boto3.client('s3')
    s3.upload_file(f'{TARGET}.zip', S3_BUCKET, os.path.join(S3_PREFIX, f'{filename}.zip'))

def pass_basic_auth(auth_header: str) -> bool:
    encoded_value = base64.b64encode(f"{BASIC_USERNAME}:{BASIC_PW}".encode('utf-8'))
    check_value = "Basic {}".format(encoded_value.decode(encoding='utf-8'))
    return auth_header == check_value

def lambda_handler(event, context):
    payload = json.loads(event['body']['payload'])

    if not payload["ref"].endswith(TARGET_BRANCH):
        return {'statusCode': 400}
    if not pass_basic_auth(event['headers']['Authorization']):
        return {'statusCode': 401}

    repo = git_clone(payload['repository']['url'])
    git_checkout(repo, payload['after'])
    zip_files()
    upload_to_s3()

    return {'statusCode': 200}
