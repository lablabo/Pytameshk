from uuid import uuid4
from flask import Flask, jsonify, request, app, Response
from argparse import ArgumentParser
from werkzeug.exceptions import HTTPException


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        self.app.register_error_handler(HTTPException, lambda e: (str(e), e.code))

    def run(self):
        self.app.run(host= '0.0.0.0')

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


class controller:

    app = None
    blockchain = None
    node_identifier = None

    def __init__(self, action, libraries):

        self.node_identifier = str(uuid4()).replace('-', '')
        self.blockchain = libraries['blockchain']

        app = FlaskAppWrapper('wrap')
        app.add_endpoint(endpoint='/mine', endpoint_name='mine', handler=self.mine)
        app.add_endpoint(endpoint='/new_transaction', endpoint_name='new_transaction', handler=self.new_transaction)
        app.add_endpoint(endpoint='/full_chain', endpoint_name='full_chain', handler=self.full_chain)
        app.add_endpoint(endpoint='/register_nodes', endpoint_name='register_nodes', handler=self.register_nodes)
        app.add_endpoint(endpoint='/consensus', endpoint_name='consensus', handler=self.consensus)


        app.run()

        # parser = ArgumentParser()
        # parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
        # args = parser.parse_args()
        # port = args.port
        # self.app.run(host='0.0.0.0', port=port)
        pass

    def mine(self):
        last_block = self.blockchain.last_block
        proof = self.blockchain.proof_of_work(last_block)

        self.blockchain.new_transaction(
            sender="0",
            recipient=self.node_identifier,
            amount=1,
        )

        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        print(response)
        return jsonify(response), 200

    # POST
    def new_transaction(self):
        values = request.get_json()

        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        index = self.blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    def full_chain(self):
        response = {
            'chain': self.blockchain.chain,
            'length': len(self.blockchain.chain),
        }
        print(response)
        return jsonify(response), 200

    # POST
    def register_nodes(self):
        values = request.get_json()

        nodes = values.get('nodes')
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400

        for node in nodes:
            self.blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(self.blockchain.nodes),
        }
        return jsonify(response), 201

    def consensus(self):
        replaced = self.blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': self.blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': self.blockchain.chain
            }

        return jsonify(response), 200
