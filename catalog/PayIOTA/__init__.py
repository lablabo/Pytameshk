from __future__ import absolute_import, division, print_function, unicode_literals
from flask import jsonify, request, Response, Flask
from flask_restful import reqparse, Api, Resource


class controller:
    iota = None

    def __init__(self, action, libraries, settings):
        app = Flask(__name__)
        api = Api(app)
        parser = reqparse.RequestParser()
        # Threads Pool
        # TODO :: Multi-threading & Multi-processing

        api.add_resource(SERVER, '/api/<url_action>',
                         resource_class_kwargs={
                             'action': action,
                             'libraries': libraries,
                             'settings': settings,
                             "parser": parser
                         })
        #app.run(port=settings['DEFAULT']['SERVER_PORT'])
        libraries['zmq'].start(settings['ZMQ']['SERVER'])


class SERVER(Resource):
    def __init__(self, action, libraries, settings, parser):
        self.settings = settings
        self.action = action
        self.libraries = libraries
        self.parser = parser
        database = self.libraries['database']

        # create a database connection to a SQLite database
        self.connection = database.connection(self.settings['DEFAULT']['DATABASE_PATH'])

        if self.connection is not None:
            database.createTable(self.connection, self.settings['QUERIES']['ADDRESS_TABLE'])
        else:
            exit("Error! cannot create the database connection.")

        # _thread.start_new_thread()

    # GET method
    def get(self, url_action):
        # database = self.libraries['database']
        # iota = self.libraries['iota']

        # Set API URL Call
        # iota.setApiCall(self.settings['DEFAULT']['API_CALL'])

        # Insert New Record
        # last_insert_id = database.insert(self.connection, self.settings['QUERIES']['INSERT_ADDRESS'], (address,))

        # query = "SELECT * FROM addresses"
        # result = database.select(self.connection, query, "")

        # return jsonify({"address": address, "last_insert_id": last_insert_id})
        return jsonify({"type": "error", "messages": "GET request is not supported."})

    # POST method
    def post(self, url_action):
        if url_action == "payment_address":
            self.parser.add_argument('address', type=str)
            args = self.parser.parse_args()

            if args['address'] is None:
                return jsonify({"type": "error", "message": "Address Required"})

            return jsonify({
                "type": "success",
                "address": args['address']
            })

        # Invalid Request
        return jsonify({"type": "error", "message": "Request Invalid"})
