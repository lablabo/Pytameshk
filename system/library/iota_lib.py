from iota import Transaction
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString
import json
from argparse import ArgumentParser
from getpass import getpass as secure_input
from sys import argv
from typing import Optional, Text
import time
from six import binary_type, moves as compat, text_type

from iota import Iota, __version__
from iota.crypto.addresses import AddressGenerator
from iota.crypto.types import Seed
import json, urllib
from urllib.request import urlopen
import  urllib.request

# https://docs.iota.org/docs/iri/0.1/references/api-reference#storetransactions


class controller:

    register = None

    def __init__(self, register):
        self.register = register

    def encode_tryte(self, input_text):
        message_trytes = TryteString.from_unicode(input_text)
        print(message_trytes)

    # More Information https://pyota.readthedocs.io/en/latest/types.html
    def decode_tryte_method_2(self, encoded_text):
        txn_1 = Transaction.from_tryte_string(encoded_text)
        return {"address": txn_1.address,
                "value": txn_1.value,
                "legacy_tag": txn_1.legacy_tag,
                "hash": txn_1.hash,
                "timestamp": txn_1.timestamp,
                "tag": txn_1.tag,
                "current_index": txn_1.current_index,
                "last_index": txn_1.last_index,
                "bundle_hash": txn_1.bundle_hash,
                "trunk_transaction_hash": txn_1.trunk_transaction_hash,
                "branch_transaction_hash": txn_1.branch_transaction_hash,
                "nonce": txn_1.nonce,
                "signature_message_fragment": txn_1.signature_message_fragment.decode()
                }

    def decode_tryte_method_1(self, encoded_text):
        trytes = TryteString(encoded_text)
        message = trytes.decode()
        print(message)

    def output_seed(self, seed):
        print(binary_type(seed).decode('ascii'))

    def get_seed(self):
        # type: () -> binary_type
        """
        Prompts the user securely for their seed.
        """
        seed = ""
        return seed.encode('ascii')

    def prepare_transaction(self):
        seed = self.get_seed()
        api = Iota('http://iota.av.it.pt:14265', seed)
        if not seed:
            print('A random seed has been generated.')
            self.output_seed(api.seed)

        #api_response = api.get_new_addresses(index, count, security, checksum)
        api_response = api.get_new_addresses(0, None, AddressGenerator.DEFAULT_SECURITY_LEVEL, False)
        address = None;
        for addy in api_response['addresses']:
            address = (binary_type(addy).decode('ascii'))

        # Test your connection to the server by sending a getNodeInfo command
        # -> print(api.get_node_info())

        data = {
            "option1": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        message = str(data)

        print('Starting transfer.')
        start = time.time()

        # For more information, see :py:meth:`Iota.send_transfer`.
        result = api.send_transfer(
            depth=3,
            # One or more :py:class:`ProposedTransaction` objects to add to the
            # bundle.
            transfers=[
                ProposedTransaction(
                    # Recipient of the transfer.
                    address=Address(address),

                    # Amount of IOTA to transfer.
                    # By default this is a zero value transfer.
                    value=0,

                    # Optional tag to attach to the transfer.
                    tag=Tag(b'TAG'),

                    # Optional message to include with the transfer.
                    message=TryteString.from_string(message),
                ),
            ],
        )
        stop = time.time()

        if 'bundle' in result:
            print('attached address', address)
            print('with transaction', str(result['bundle'].transactions[-1].hash))
            print('in bundle', str(result['bundle'].hash))
            print('within', round(stop - start, 1), 'seconds')
        else:
            print('probably failed')
        print('Transfer complete.')

    def do_getTransactionsToApprove(self):
        command = {
            "command": "getTransactionsToApprove",
            "depth": 4,
        }
        stringified = json.dumps(command)
        headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }
        request = urllib.request.Request(url="http://iota.av.it.pt:14265", data=stringified.encode(), headers=headers)
        returnData = urllib.request.urlopen(request).read()

        return json.loads(returnData)

    def do_prepare_transaction(self):
        seed = self.get_seed()
        api = Iota('http://iota.av.it.pt:14265', seed)
        if not seed:
            print('A random seed has been generated.')
            self.output_seed(api.seed)

        #api_response = api.get_new_addresses(index, count, security, checksum)
        api_response = api.get_new_addresses(0, None, AddressGenerator.DEFAULT_SECURITY_LEVEL, False)
        address = None;
        for addy in api_response['addresses']:
            address = (binary_type(addy).decode('ascii'))

        # Test your connection to the server by sending a getNodeInfo command
        # -> print(api.get_node_info())

        data = {
            "option1": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        message = str(data)

        print('Starting transfer.')
        start = time.time()

        # For more information, see :py:meth:`Iota.send_transfer`.
        result = api.send_transfer(
            depth=3,
            # One or more :py:class:`ProposedTransaction` objects to add to the
            # bundle.
            transfers=[
                ProposedTransaction(
                    # Recipient of the transfer.
                    address=Address(address),

                    # Amount of IOTA to transfer.
                    # By default this is a zero value transfer.
                    value=0,

                    # Optional tag to attach to the transfer.
                    tag=Tag(b'TAG'),

                    # Optional message to include with the transfer.
                    message=TryteString.from_string(message),
                ),
            ],
        )
        stop = time.time()

        if 'bundle' in result:
            print('attached address', address)
            print('with transaction', str(result['bundle'].transactions[-1].hash))
            print('in bundle', str(result['bundle'].hash))
            print('within', round(stop - start, 1), 'seconds')
        else:
            print('probably failed')
        print('Transfer complete.')

    def do_attachToTangle(self):
        result = self.do_getTransactionsToApprove()
        command = {
            "command": "attachToTangle",
            "trunkTransaction": result['trunkTransaction'],
            "branchTransaction": result['branchTransaction'],
            "minWeightMagnitude": 14,
            "trytes":[
                "LBTCBDSCTCFD999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999BENDER999BENDER999BENDER999BENDER999BENDER999BENDER999BENDER999BENDER999BENDER999999999999999999999999999999EOPDER999999999999999999999HXGQRAD99999999999999999999CIODD9IUZOQDODRCHEOIDQDEIBAJQAGXWXFYUDFKIWXDIKBJQ9OEKJCKMPMPEECBIWGCVGISWKEKZWVJCZ9QQW9YLDAOD9ODLQSNCTHPZXWMZESYLRVIGQIUKUTC9ZYC9BUPDYHFHJB9RCCQFJZKKHUXZBSOV99999WXSYRQCIIGAYGMWOCHQWSFQHD9OJGSRBT9KOKPFLEYIPTEXFEQHBKTDPPCBZDEFTG9MROROFFJVIA9999BENDER999999999999999999999UCPCHEANF999999999MMMMMMMMMTIA9999999LJK99999999999999"
            ]
        }

        stringified = json.dumps(command)

        headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        request = urllib.request.Request(url="http://iota.av.it.pt:14265", data=stringified.encode(), headers=headers)
        returnData = urllib.request.urlopen(request).read()

        return json.loads(returnData)

    def do_storeTransactions(self, trytes):
        command = {
            "command": "storeTransactions",
            "trytes": trytes
        }

        stringified = json.dumps(command)

        headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        request = urllib.request.Request(url="http://iota.av.it.pt:14265", data=stringified.encode(), headers=headers)
        returnData = urllib.request.urlopen(request).read()

        jsonData = json.loads(returnData)

        print(jsonData)

    def do_broadcastTransactions(self):
        result = self.do_attachToTangle()
        self.do_storeTransactions(result['trytes'])
        command = {
            "command": "broadcastTransactions",
            "trytes": result['trytes']
        }

        stringified = json.dumps(command)

        headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        request = urllib.request.Request(url="http://iota.av.it.pt:14265", data=stringified.encode(), headers=headers)
        returnData = urllib.request.urlopen(request).read()

        jsonData = json.loads(returnData)
        print(jsonData)
