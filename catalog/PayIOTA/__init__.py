from __future__ import absolute_import, division, print_function, unicode_literals
import zmq
from zmq.utils.monitor import recv_monitor_message
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from flask import Flask, jsonify, request, Response
from multiprocessing import Value
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

class controller:
    iota = None
    def __init__(self, action, libraries, settings):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Employees_Name, '/api/<address>', resource_class_kwargs={'action': action,
                                                                                  'libraries': libraries,
                                                                                  'settings': settings})
        app.run(port='5002')

    def testZMG(self, iota):
        context = zmq.Context()
        socket = zmq.Socket(context, zmq.SUB)
        monitor = socket.get_monitor_socket()

        #tcp://iota.av.it.pt:5555
        socket.connect("tcp://iota.av.it.pt:5555")
        while True:
            status = recv_monitor_message(monitor)
            if status['event'] == zmq.EVENT_CONNECTED:
                break
            elif status['event'] == zmq.EVENT_CONNECT_DELAYED:
                pass

        print('connected')
        socket.subscribe('tx_trytes')
        while True:
            topic = socket.recv_string()
            topic = topic.split(" ")
            print(topic)
            data = iota.decode_tryte_method_2(topic[1].encode('utf-8'))
            # More Information https://pyota.readthedocs.io/en/latest/types.html
            print(data)


class Employees_Name(Resource):
    def __init__(self, action, libraries, settings):
        self.settings = settings
        self.action = action
        self.libraries = libraries

    def get(self, address):
        self.db_connect = create_engine('sqlite:///chinook.db')
        self.iota = self.libraries['iota']

        # Set API URL Call
        # You can change it in setup.ini
        self.iota.setApiCall(self.settings['DEFAULT']['API_CALL'])

        return jsonify({"number": address})

        # conn = db_connect.connect()
        # query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        # result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
