from uuid import uuid4
from flask import jsonify, request
from catalog.blockchain.assets import config
from catalog.blockchain.library import message, FlaskAppWrapper


class controller:

    app = None
    blockchain = None
    node_identifier = None
    thread = None
    network = None
    custom_config = None
    message = None

    def __init__(self, action, libraries):

        self.custom_config = config.custom_config()
        self.message = message.Message()

        self.node_identifier = str(uuid4()).replace('-', '')
        self.blockchain = libraries['blockchain']
        self.network = libraries['network']

        self.thread = libraries['thread']
        pool = self.thread.create_thread(2)

        pool.queueTask(self.start_listening, None, None)
        pool.queueTask(self.start_flask, None, None)

        pool.joinAll()

        pass

    def start_flask(self, data):

        app = FlaskAppWrapper.FlaskAppWrapper('wrap')
        app.add_endpoint(endpoint='/mine', endpoint_name='mine', handler=self.mine)
        app.add_endpoint(endpoint='/new_transaction', endpoint_name='new_transaction', handler=self.new_transaction)
        app.add_endpoint(endpoint='/full_chain', endpoint_name='full_chain', handler=self.full_chain)
        app.add_endpoint(endpoint='/register_nodes', endpoint_name='register_nodes', handler=self.register_nodes)
        app.add_endpoint(endpoint='/consensus', endpoint_name='consensus', handler=self.consensus)
        app.run()

        pass

    def start_listening(self, data):
        socket_ = self.network.create_socket('', self.custom_config.PORT)
        while True:
            message_, address = socket_.recvfrom(self.custom_config.PORT)
            print(address)
            print(self.message.convert(message_))
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
        text = self.message.convert(response, 'json_to_byte')
        self.network.send_message(text, '<broadcast>', self.custom_config.PORT)
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
