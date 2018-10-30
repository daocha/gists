# Date: 30 Oct 2018
# Author: Ray LI
""" HTTP(s) Request utils """

from dcha.security import aes
from flask import request
from urllib import parse
import json
import logging


def get_form_data():
    """
        get JSON data from request
    """
    return request.get_json(force=True)


def get_access_token():
    """
        read access-token from header and decrypt it
    """
    logger = logging.getLogger(__name__)
    cipher_access_token = request.headers.get('access-token')
    decoded_access_token = parse.unquote(cipher_access_token).replace(' ', '+')
    logger.debug("cipher_access_token: %s" % cipher_access_token)
    logger.debug("decoded_cipher_access_token: %s" % decoded_access_token)
    access_token = aes.decryptAES(decoded_access_token)
    return access_token
