from iota import Transaction
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString
import time
from six import binary_type, moves as compat, text_type
from iota import Iota, __version__
from iota.crypto.addresses import AddressGenerator
from iota.crypto.types import Seed
import json, urllib
from urllib.request import urlopen
import urllib.request

# https://docs.iota.org/docs/iri/0.1/references/api-reference#storetransactions


class controller:

    register = None

    def __init__(self, register):
        self.register = register

    def do_send_request(self, stringified, headers, url):

        if headers is None:
            headers = {
                'content-type': 'application/json',
                'X-IOTA-API-Version': '1'
            }

        if url is None:
            url = "http://iota.av.it.pt:14265"

        request = urllib.request.Request(url=url, data=stringified.encode(), headers=headers)
        return_data = urllib.request.urlopen(request).read()
        return json.loads(return_data)

    # Check the consistency of transactions. A consistent transaction is one where the following statements are true:
    # The transaction isn't missing a reference transaction
    # The transaction's bundle is valid
    # The transaction's reference transactions are valid
    def do_checkConsistency(self, tails):
        command = {
            "command": "checkConsistency",
            "tails": tails
        }

        # Response
        # State ::State of the given transactions in the tails parameter. A true value means that all given transactions
        # are consistent. A false value means that one or more of the given transactions aren't consistent.
        # info :: If the state field is false, this field contains information about why the transaction is inconsistent
        # duration :: Number of milliseconds it took to complete the request
        return self.do_send_request(json.dumps(command), None, None)

    # Find transactions that contain the given values in their transaction fields. The parameters define the transaction
    # fields to search for, including bundles, addresses, tags, and approves.
    # Using multiple transaction fields, returns transactions hashes at the intersection of those values.
    def do_findTransactions(self, addresses):
        # Parameters
        # bundles :: Bundle hashes to search for - array of strings
        # addresses :: Addresses to search for (do not include the checksum) - array of strings
        # tags :: Tags to search for - array of strings
        # approvees :: Child transactions to search for	- array of strings
        command = {
            "command": "findTransactions",
            "addresses": addresses
        }

        # Response
        # An array of transaction hashes, is returned in the same order for all individual elements.
        # hashes :: The transaction hashes which are returned depend on your input.
        # - bundles: returns an array oftransaction hashes that contain the given bundle hash.
        # - addresses: returns an array of transaction hashes that contain the given address in the address field.
        # - tags: returns an array of transaction hashes that contain the given value in the tag field.
        # - approvees: returns an array of transaction hashes that contain the given transactions in their
        #   branchTransaction or trunkTransaction fields.
        # duration :: Number of milliseconds it took to complete the request
        return self.do_send_request(json.dumps(command), None, None)

    # Get the confirmed balance of an address.
    # If the tips parameter is missing, the returned balance is correct as of the latest confirmed milestone.
    def do_getBalances(self, addresses, threshold):
        # Parameters
        # addresses :: Address for which to get the balance (do not include the checksum) - array of strings
        # threshold :: Confirmation threshold between 0 and 100 - integer
        # tips (Optional):: Tips whose history of transactions to traverse to find the balance - array of strings
        command = {
            "command": "getBalances",
            "addresses": addresses,
            "threshold": threshold
        }

        # Response
        # balances :: Array of balances in the same order as the addresses parameters were passed to the endpoint
        # references :: The referencing tips. If no tips parameter was passed to the endpoint, this field contains
        #               the hash of the latest milestone that confirmed the balance
        # milestoneIndex :: The index of the milestone that confirmed the most recent balance
        # duration :: Number of milliseconds it took to process the request
        return self.do_send_request(json.dumps(command), None, None)

    # Get the inclusion states of a set of transactions. This endpoint determines if a transaction is confirmed
    # by the network (referenced by a valid milestone). You can search for multiple tips (and thus, milestones)
    # to get past inclusion states of transactions.
    def do_getInclusionStates(self, transactions, tips):
        # Parameters
        # transactions :: List of transaction hashes for which you want to get the inclusion state
        # tips (Optional) :: List of tip transaction hashes (including milestones) you want to search for
        command = {
            "command": "getInclusionStates",
            "transactions": transactions,
            "tips": tips
        }

        # Response
        # states :: List of boolean values in the same order as the transactions parameters. A true value means
        #           the transaction was confirmed
        # duration :: Number of milliseconds it took to complete the request
        return self.do_send_request(json.dumps(command), None, None)

    # Get information about a node.
    def do_getNodeInfo(self):
        command = {"command": "getNodeInfo"}
        return self.do_send_request(json.dumps(command), None, None)

    # Get tip transaction hashes from a node.
    def do_getTips(self):
        command = {"command": "getTips"}

        # Response
        # hashes :: Array of tip transaction hashes
        # duration :: Number of milliseconds it took to complete the request
        return self.do_send_request(json.dumps(command), None, None)

    # Get two consistent tip transaction hashes to use as branch/trunk transactions.
    def do_getTransactionsToApprove(self, depth):
        # Parameters
        # depth :: Number of bundles to go back to determine the transactions for approval.
        # reference (Optional) :: Transaction hash from which to start the weighted random walk. Use this parameter
        #           to make sure the returned tip transaction hashes approve a given reference transaction.
        command = {
            "command": "getTransactionsToApprove",
            "depth": depth,
        }

        # Response
        # trunkTransaction :: Valid trunk transaction hash
        # branchTransaction	 :: Valid branch transaction hash
        # duration :: The time it took to process the request in milliseconds
        return self.do_send_request(json.dumps(command), None, None)

    # Get a transaction's contents in trytes.
    def do_getTrytes(self):
        # Parameters
        # hashes :: Transaction hashes
        command = {
            "command": "getTrytes",
            "hashes": [
                "NGDFRIHOOS9J9YBQCDSFJZJKNSAJTNFKSXXEZWPZQSLRTYQDNX9UCGJHU9OZGFATCCQSGSFUZLLET9LID",
                "MUIYDLYHCAYGYK9IPVQX9GIHIWWCATAJ9BNFPVKZHZOSXAWVHEHHMSVEVTNRJVGCGEMSNI9ATUXFKPZRQ"
            ]
        }

        # Response
        return self.do_send_request(json.dumps(command), None, None)


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


