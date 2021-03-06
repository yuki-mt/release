"""
Githubをpythonから操作するサンプルコード

Access Tokenはここから取得: https://github.com/settings/tokens

pip install -U pip && pip install pygithub
"""
from github import Github
from github.GithubException import GithubException
import sys


WORKING_BRANCH = 'feature/test'
TARGET_BRANCH = 'master'
BASE_URL = 'https://github.com/api/v3'
ACCESS_TOKEN = 'xxx'
ORG = 'yuki-mt'
REPO_NAME = 'scripts'

IS_SUCCESS_KEY = 'success'
SUCCESS_RESULT = {IS_SUCCESS_KEY: True}


def main():
    """
    git_token.conf should be like:
    -----------------
    [default]
    access_token=YOUR_GIT_ACCESS_TOKEN
    -----------------
    """
    repo_path = f"{ORG}/{REPO_NAME}"

    try:
        g = Github(ACCESS_TOKEN, base_url=BASE_URL)
        # git checkout
        repo = g.get_repo(repo_path)
    except GithubException as e:
        print(type(e.data))
        msg = "Failed to get branch\n{0}(err={1})".format(e.data, e.status)
        sys.stderr.write(msg)
        return -1

    print(delete_file(repo, 'sample.txt'))
    print(edit_file(repo, 'sample.txt', 'aaafea'))
    print(merge(repo))


def edit_file(repo, path, content, comment='update a file'):
    if not path.startswith('/'):
        path = '/' + path

    try:
        current_content = repo.get_file_contents(path, WORKING_BRANCH).content
    except GithubException:
        current_content = False

    try:
        if not current_content:
            result = repo.create_file(path, comment, content, WORKING_BRANCH)
        else:
            blob = repo.create_git_blob(current_content, 'base64')
            result = repo.update_file(path, comment, content, blob.sha, WORKING_BRANCH)

        result.update(SUCCESS_RESULT)
        return result
    except GithubException as e:
        msg = "Failed to update file\n{0}(err={1})".format(e.data, e.status)
        sys.stderr.write(msg)
        return get_error_json(msg)


def delete_file(repo, path, comment='delete a file'):
    if not path.startswith('/'):
        path = '/' + path
    try:
        current_content = repo.get_file_contents(path, WORKING_BRANCH).content
        blob = repo.create_git_blob(current_content, 'base64')
        result = repo.delete_file(path, comment, blob.sha, WORKING_BRANCH)
        result.update(SUCCESS_RESULT)
        return result
    except GithubException as e:
        msg = "Failed to delete file\n{0}(err={1})".format(e.data, e.status)
        sys.stderr.write(msg)
        return get_error_json(msg)


def merge(repo):
    try:
        commit = repo.merge(TARGET_BRANCH, WORKING_BRANCH)
        result = {'commit': commit.sha}
        result.update(SUCCESS_RESULT)
        return result
    except GithubException as e:
        msg = "Failed to merge\n{0}(err={1})".format(e.data, e.status)
        sys.stderr.write(msg)
        return get_error_json(msg)


def get_error_json(msg):
    return {'message': msg, IS_SUCCESS_KEY: False}


if __name__ == "__main__":
    main()
