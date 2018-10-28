# Date: 27 Oct 2018
# Author: Ray LI
""" GitHub authentication """
from flask import Flask, redirect, request, Blueprint, jsonify
from dcha.security import aes
import requests
import json

client_id = "e506af0c5bf4efc48819"
client_secret = "f4f275a6f94a2c67d52456d82d8371023bb6a7b9"

auth_page = Blueprint('auth_page', __name__)

@auth_page.route("/", methods=["GET"])
def auth():
    """
        Authenticate in GitHub
    """
    auth_url = "https://github.com/login/oauth/authorize?client_id=" + client_id \
                + "&scope=user:email%20gist"
    return redirect(auth_url)

@auth_page.route("/callback", methods=["GET"])
def auth_callback():
    """
        GitHub Authentication Callback
    """
    code = request.args.get('code')

    if code is None:
        return jsonify(error="code is not presented")

    access_token_url = "https://github.com/login/oauth/access_token"

    res = requests.post(access_token_url, params={
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    })

    result = res.content.decode("utf-8")

    params = result.split("&")

    for param in params:
        keyval = param.split("=")
        print('%s=%s' % (keyval[0], keyval[1]))
        if keyval[0] == 'access_token':
            access_token = keyval[1]

    if access_token is None:
        return jsonify(error="access token is not presented")

    # access_code should be saved in user db(e.g. mongo), to save time and avoid DB setup,
    # this access code is encrypted and sent to client side directly.
    # User will then send message with the access token in every single request
    ciphercode = aes.encryptAES(access_token)
    homeurl = "/?access_token=" + ciphercode
    return redirect(homeurl)
