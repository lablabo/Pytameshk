from uuid import uuid4
from flask import Flask, jsonify, request

class controller:
    def __init__(self, action, libraries):
        blockchain = libraries['blockchain']
        print(blockchain.last_block())
        pass
