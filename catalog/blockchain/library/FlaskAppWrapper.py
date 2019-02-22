from flask import Flask, jsonify, request, app, Response
from werkzeug.exceptions import HTTPException
from catalog.blockchain.library import EndpointAction


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        # Error Handling
        self.app.register_error_handler(HTTPException, lambda e: (str(e), e.code))

    def run(self):
        self.app.run(host='0.0.0.0')

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction.EndpointAction(handler))
