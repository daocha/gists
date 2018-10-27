# Date: 27 Oct 2018
# Author: Ray LI
""" GitHub authentication """
from flask import Flask, redirect, request, Blueprint, jsonify
from dcha.security import aes

client_id = "e506af0c5bf4efc48819"

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
    access_code = request.args.get('code')

    if access_code is None:
        return jsonify(error="code is not presented")

    # access_code should be saved in user db(e.g. mongo), to save time and avoid DB setup,
    # this access code is encrypted and sent to client side directly.
    # User will then send message with the access token in every single request
    ciphercode = aes.encryptAES(access_code)
    homeurl = "/?code=" + ciphercode
    return redirect(homeurl)
