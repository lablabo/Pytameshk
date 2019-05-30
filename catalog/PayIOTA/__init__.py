from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask, jsonify, request, Response
from flask import Flask, request
from flask_restful import Resource, Api



class controller:
    iota = None
    def __init__(self, action, libraries, settings):
        app = Flask(__name__)
        api = Api(app)

        threadPool = libraries['thread'].create_thread(2)
        api.add_resource(SERVER, '/api/<address>', resource_class_kwargs={'action': action,
                                                                          'libraries': libraries,
                                                                          'settings': settings})
        threadPool.queueTask(app.run(port=settings['DEFAULT']['SERVER_PORT']))
        # threadPool.queueTask(libraries['zmq'].start(settings['ZMQ']['SERVER']))



class SERVER(Resource):
    def __init__(self, action, libraries, settings):
        self.settings = settings
        self.action = action
        self.libraries = libraries
        database = self.libraries['database']

        # create a database connection to a SQLite database
        self.connection = database.connection(self.settings['DEFAULT']['DATABASE_PATH'])

        if self.connection is not None:
            database.createTable(self.connection, self.settings['QUERIES']['ADDRESS_TABLE'])
        else:
            exit("Error! cannot create the database connection.")

        # _thread.start_new_thread()

    def get(self, address):
        database = self.libraries['database']
        iota = self.libraries['iota']

        # Set API URL Call
        iota.setApiCall(self.settings['DEFAULT']['API_CALL'])

        # Insert New Record
        last_insert_id = database.insert(self.connection, self.settings['QUERIES']['INSERT_ADDRESS'], (address,))

        # query = "SELECT * FROM addresses"
        # result = database.select(self.connection, query, "")

        return jsonify({"address": address, "last_insert_id": last_insert_id})

