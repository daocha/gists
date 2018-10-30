# Date: 29 Oct 2018
# Author: Ray LI
""" Calling Github API """

from dcha.endpoints import request
import requests
import json


def call_github_gist_delete(gist_id):
    """
        Call github API to delete gist
    """
    access_token = request.get_access_token()
    params = {
        'access_token': access_token
    }
    gist_url = "https://api.github.com/gists/%s" % gist_id
    res = requests.delete(gist_url, params=params)
    return res


def call_github_gist_get():
    """
        Call github API to retrieve gist
    """
    access_token = request.get_access_token()
    params = {
        'access_token': access_token
    }
    gist_list_url = "https://api.github.com/gists"
    res = requests.get(gist_list_url, params=params)
    return res


def call_github_gist_post(submit_content):
    """
        Call github API to create gist
    """
    access_token = request.get_access_token()
    create_gist_url = "https://api.github.com/gists"
    params = {
        'access_token': access_token
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(create_gist_url, params=params,
                        data=json.dumps(submit_content),
                        headers=headers)
    return res


def call_github_comment_post(gist_id, submit_comment):
    """
        Call github API to create comment
    """
    access_token = request.get_access_token()
    create_comment_url = "https://api.github.com/gists/%s/comments" % gist_id
    params = {
        'access_token': access_token
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(create_comment_url, params=params,
                        data=json.dumps(submit_comment),
                        headers=headers)
    return res


def call_github_comment_get(gist_id):
    """
        Call github API to get comment list
    """
    access_token = request.get_access_token()
    comment_list_url = "https://api.github.com/gists/%s/comments" % gist_id
    params = {
        'access_token': access_token
    }
    res = requests.get(comment_list_url, params=params)
    return res


def call_github_comment_delete(gist_id, comment_id):
    """
        Call github API to delete comment
    """
    access_token = request.get_access_token()
    comment_url = "https://api.github.com/gists/%s/comments/%s" % (
        gist_id, comment_id)
    params = {
        'access_token': access_token
    }
    res = requests.delete(comment_url, params=params)
    return res
