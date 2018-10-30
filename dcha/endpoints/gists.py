# Date: 28 Oct 2018
# Author: Ray LI
""" Endpoints for managing github gists """

from flask import Blueprint, jsonify
from dcha.endpoints import github
from dcha.endpoints import request
import json
import logging

gist_api = Blueprint('gist_api', __name__)


@gist_api.route("/<gist_id>", methods=["DELETE"])
def delete_gist(gist_id):
    """
        Deleting one gist with id
    """
    logger = logging.getLogger(__name__)
    try:
        res = github.call_github_gist_delete(gist_id)
        logger.debug(res.text)
        return jsonify(res.text)
    except ValueError as e:
        errorMsg = "Error occurs when deleting a gist"
        logger.error("%s: %s" % (errorMsg, e.message))
        return jsonify(error=errorMsg)


@gist_api.route("", methods=["GET"])
def get_gist_list():
    """
        Retrieving the gist list
    """
    logger = logging.getLogger(__name__)
    try:
        res = github.call_github_gist_get()
        return jsonify(res.text)
    except ValueError as e:
        errorMsg = "Error occurs when retrieving gists list"
        logger.error("%s: %s" % (errorMsg, e.message))
        return jsonify(error=errorMsg)


@gist_api.route("", methods=["POST"])
def create_gist():
    """
        Post a new gist list
    """
    logger = logging.getLogger(__name__)
    try:
        data = request.get_form_data()
        content = data.get('gist_content')
        description = data.get('gist_description')
        filename = data.get('gist_filename')
        logger.debug('description: %s \nfilename: %s \ncontent: %s'
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
        if content is not None:
            logger.debug(json.dumps(submit_content))
            res = github.call_github_gist_post(submit_content)
            success = res.status_code == 201
            logger.debug(res.text)
        return jsonify(success=success), res.status_code
    except ValueError as e:
        errorMsg = "Error occurs when creating a new gist"
        logger.error("%s: %s" % (errorMsg, e.message))
        return jsonify(error=errorMsg)


@gist_api.route("/<gist_id>/comments", methods=["POST"])
def create_comment(gist_id):
    """
        Post a new comment to a gist
    """
    logger = logging.getLogger(__name__)
    try:
        data = request.get_form_data()
        comment = data.get('gist_comment')
        logger.debug('comment: %s' % comment)
        submit_comment = {
            "body": comment
        }
        if comment is not None:
            logger.debug(json.dumps(submit_comment))
            res = github.call_github_comment_post(
                gist_id, submit_comment)
            success = res.status_code == 201
            logger.debug(res.text)
        return jsonify(success=success), res.status_code
    except ValueError as e:
        errorMsg = "Error occurs when creating a comment"
        logger.error("%s: %s" % (errorMsg, e.message))
        return jsonify(error=errorMsg)


@gist_api.route("/<gist_id>/comments", methods=["GET"])
def get_comments_list(gist_id):
    """
        Retrieving comments of the specific gist
    """
    logger = logging.getLogger(__name__)
    try:
        res = github.call_github_comment_get(gist_id)
        return jsonify(res.text)
    except ValueError as e:
        errorMsg = "Error occurs when retrieving comments list"
        logger.error("%s: %s" % (errorMsg, e.message))
        return jsonify(error=errorMsg)


@gist_api.route("/<gist_id>/comments/<comment_id>", methods=["DELETE"])
def delete_comment(gist_id, comment_id):
    """
        Deleting one gist with id
    """
    logger = logging.getLogger(__name__)
    try:
        res = github.call_github_comment_delete(
            gist_id, comment_id)
        logger.debug(res.text)
        return jsonify(res.text)
    except ValueError as e:
        errorMsg = "Error occurs when deleting comment"
        logger.error("%s: %s" % (errorMsg, e.message))
        return jsonify(error=errorMsg)
