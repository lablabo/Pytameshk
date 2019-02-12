from uuid import uuid4
from flask import Flask, jsonify, request, app
from argparse import ArgumentParser


class controller:
    def __init__(self, action, libraries):
        self.app = Flask(__name__)
        self.node_identifier = str(uuid4()).replace('-', '')
        self.blockchain = libraries['blockchain']

        parser = ArgumentParser()
        parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
        args = parser.parse_args()
        port = args.port

        self.app.run(host='0.0.0.0', port=port)
        pass

    #@app.route('/mine', methods=['GET'])
    def mine(self):
        # We run the proof of work algorithm to get the next proof...
        last_block = self.blockchain.last_block
        proof = self.blockchain.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        self.blockchain.new_transaction(
            sender="0",
            recipient=self.node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200

    #@app.route('/transactions/new', methods=['POST'])
    def new_transaction(self):
        values = request.get_json()

        # Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = self.blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    #@app.route('/chain', methods=['GET'])
    def full_chain(self):
        response = {
            'chain': self.blockchain.chain,
            'length': len(self.blockchain.chain),
        }
        return jsonify(response), 200

    #@app.route('/nodes/register', methods=['POST'])
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

    #@app.route('/nodes/resolve', methods=['GET'])
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
