from flask import Flask, render_template, send_from_directory
from flask import jsonify
from .endpoints.gists import gist_api
from .endpoints.auth import auth_page
from .endpoints.jsonconverter import JSONEncoderCustom
from .nocache import nocache
import logging.config
import json

# configure logging settings
with open('logging.json') as f:
    config_dict = json.load(f)
    logging.config.dictConfig(config_dict)

# api version No.
version = "v1.0"

app = Flask(__name__, static_url_path='/static')

# json serializer
app.json_encoder = JSONEncoderCustom

# define endpoints
app.register_blueprint(gist_api, url_prefix=('/%s/gist' % version))
app.register_blueprint(auth_page, url_prefix='/auth')


# handling static pages & files
@app.route('/')
def render_static():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
@nocache
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
@nocache
def send_css(path):
    return send_from_directory('static/css', path)

if __name__ == '__main__':
    app.run()
