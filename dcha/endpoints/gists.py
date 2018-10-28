# Date: 27 Oct 2018
# Author: Ray LI
""" Manage gists """

from flask import Blueprint, jsonify, request
from dcha.security import aes
from urllib import parse
import requests
import json

gist_api = Blueprint('gist_api', __name__)

@gist_api.route("/<gist_id>", methods=["DELETE"])
def deleteGist(gist_id):
    """
        Deleting one gist with id
    """
    gist_url = "https://api.github.com/gists/%s" % gist_id
    access_token = decryptAccessToken()
    params = {
        'access_token': access_token
    }
    res = requests.delete(gist_url, params=params)
    print(res.text)
    return jsonify(res.text)

@gist_api.route("", methods=["GET"])
def getGistList():
    """
        Retrieving the gist list
    """
    gist_list_url = "https://api.github.com/gists"
    access_token = decryptAccessToken()
    params = {
        'access_token': access_token
    }
    res = requests.get(gist_list_url, params=params)
    return jsonify(res.text)

@gist_api.route("", methods=["POST"])
def createGist():
    """
        Post a new gist list
    """
    access_token = decryptAccessToken()
    create_gist_url = "https://api.github.com/gists"
    data = request.get_json(force=True)
    content = data.get('gist_content')
    description = data.get('gist_description')
    filename = data.get('gist_filename')
    print('description: %s \nfilename: %s \ncontent: %s'
           % (description, filename, content))
    submit_content = {
      "description": description,
      "public": True,
      "files": {
        filename: {
          "content": content
        }
      }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'access_token': access_token
    }
    if content is not None:
        print(json.dumps(submit_content))
        res = requests.post(create_gist_url, params=params,
                            data=json.dumps(submit_content),
                            headers=headers)
        print(res)
    return jsonify(success=True)

@gist_api.route("/<gist_id>/comment", methods=["POST"])
def createComment(gist_id):
    """
        Post a new comment to a gist
    """
    access_token = decryptAccessToken()
    create_comment_url = "https://api.github.com/gists/%s/comments" % gist_id
    data = request.get_json(force=True)
    comment = data.get('gist_comment')
    print('comment: %s' % comment)
    submit_comment = {
      "body": comment
    }
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'access_token': access_token
    }
    if comment is not None:
        print(json.dumps(submit_comment))
        res = requests.post(create_comment_url, params=params,
                            data=json.dumps(submit_comment),
                            headers=headers)
        print(res)
    return jsonify(success=True)

@gist_api.route("/<gist_id>/comments", methods=["GET"])
def getCommentsList(gist_id):
    """
        Retrieving comments of the specific gist
    """
    comment_list_url = "https://api.github.com/gists/%s/comments" % gist_id
    access_token = decryptAccessToken()
    params = {
        'access_token': access_token
    }
    res = requests.get(comment_list_url, params=params)
    return jsonify(res.text)

@gist_api.route("/<gist_id>/comment/<comment_id>", methods=["DELETE"])
def deleteComment(gist_id, comment_id):
    """
        Deleting one gist with id
    """
    comment_url = "https://api.github.com/gists/%s/comments/%s" % (gist_id, comment_id)
    access_token = decryptAccessToken()
    params = {
        'access_token': access_token
    }
    res = requests.delete(comment_url, params=params)
    print(res.text)
    return jsonify(res.text)

def decryptAccessToken():
    """
        read access-token from header and decrypt it
    """
    cipher_access_token = request.headers.get('access-token')
    decoded_access_token = parse.unquote(cipher_access_token).replace(' ','+')
    print("cipher_access_token", cipher_access_token)
    print("decoded_access_token", decoded_access_token)
    access_token = aes.decryptAES(decoded_access_token)
    return access_token
