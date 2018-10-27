# Date: 27 Oct 2018
# Author: Ray LI
""" Manage gists """

from flask import Blueprint
from flask import jsonify

gist_api = Blueprint('gist_api', __name__)

@gist_api.route("/<gist_id>", methods=["GET"])
def getGistDetail(gist_id):
    """
        Retrieving the gist detail with the id
    """
    try:
        print("Testing")
    except Error as e:
        return jsonify(error=e.message)
    return jsonify(success=True)

@gist_api.route("/", methods=["GET"])
def getGistList():
    """
        Retrieving the gist list
    """
    try:
        print("Testing")
    except Error as e:
        return jsonify(error=e.message)
    return jsonify(success=True)

@gist_api.route("/", methods=["POST"])
def createGist():
    """
        Post a new gist list
    """
    try:
        print("Testing")
    except Error as e:
        return jsonify(error=e.message)
    return jsonify(success=True)
