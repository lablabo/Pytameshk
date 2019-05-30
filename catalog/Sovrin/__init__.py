import asyncio,json, pprint
from indy import pool, ledger, wallet, did
from indy.error import IndyError

from catalog.Sovrin.assets import config
from catalog.Sovrin.library import message


class controller:

    def __init__(self, action, libraries):
        self.local_config = config.config()
        self.message = message.message()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.write_nym_and_query_verkey())
        loop.close()

    async def write_nym_and_query_verkey(self):

        try:
            await pool.set_protocol_version(self.local_config.PROTOCOL_VERSION)
            pool_config = json.dumps({'genesis_txn': self.local_config.genesis_file_path})

            self.message.show('\n1. Create new pool ledger configuration to connect to ledger.\n')
            await pool.create_pool_ledger_config(config_name=self.local_config.pool_name, config=pool_config)
            try:
                await pool.create_pool_ledger_config(config_name=self.local_config.pool_name, config=pool_config)
            except IndyError:
                await pool.delete_pool_ledger_config(config_name=self.local_config.pool_name)
                await pool.create_pool_ledger_config(config_name=self.local_config.pool_name, config=pool_config)

            self.message.show('\n2. Open ledger and get handle\n')
            pool_handle = await pool.open_pool_ledger(config_name=self.local_config.pool_name, config=None)

            self.message.show('\n3. Create new identity wallet\n')
            await wallet.create_wallet(self.local_config.wallet_config, self.local_config.wallet_credentials)

            self.message.show('\n4. Open identity wallet and get handle\n')
            wallet_handle = await wallet.open_wallet(self.local_config.wallet_config, self.local_config.wallet_credentials)

            self.message.show('\n5. Generate and store steward DID and verkey\n')
            steward_seed = '000000000000000000000000Steward1'
            did_json = json.dumps({'seed': steward_seed})
            steward_did, steward_verkey = await did.create_and_store_my_did(wallet_handle, did_json)
            self.message.show('Steward DID: ', steward_did)
            self.message.show('Steward Verkey: ', steward_verkey)

            self.message.show('\n6. Generating and storing trust anchor DID and verkey\n')
            trust_anchor_did, trust_anchor_verkey = await did.create_and_store_my_did(wallet_handle, "{}")
            self.message.show('Trust anchor DID: ', trust_anchor_did)
            self.message.show('Trust anchor Verkey: ', trust_anchor_verkey)

            self.message.show('\n7. Building NYM request to add Trust Anchor to the ledger\n')
            nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                     target_did=trust_anchor_did,
                                                                     ver_key=trust_anchor_verkey,
                                                                     alias=None,
                                                                     role='TRUST_ANCHOR')

            self.message.show('NYM transaction request: ')
            pprint.pprint(json.loads(nym_transaction_request))

            self.message.show('\n8. Sending NYM request to the ledger\n')
            nym_transaction_response = await ledger.sign_and_submit_request(pool_handle=pool_handle,
                                                                            wallet_handle=wallet_handle,
                                                                            submitter_did=steward_did,
                                                                            request_json=nym_transaction_request)
            self.message.show('NYM transaction response: ')
            pprint.pprint(json.loads(nym_transaction_response))

            self.message.show('\n9. Generating and storing DID and verkey representing a Client '
                              'that wants to obtain Trust Anchor Verkey\n')
            client_did, client_verkey = await did.create_and_store_my_did(wallet_handle, "{}")
            self.message.show('Client DID: ', client_did)
            self.message.show('Client Verkey: ', client_verkey)

            self.message.show('\n10. Building the GET_NYM request to query trust anchor verkey\n')
            get_nym_request = await ledger.build_get_nym_request(submitter_did=client_did,
                                                                 target_did=trust_anchor_did)
            self.message.show('GET_NYM request: ')
            pprint.pprint(json.loads(get_nym_request))

            self.message.show('\n11. Sending the Get NYM request to the ledger\n')
            get_nym_response_json = await ledger.submit_request(pool_handle=pool_handle, request_json=get_nym_request)
            get_nym_response = json.loads(get_nym_response_json)

            self.message.show('GET_NYM response: ')
            pprint.pprint(get_nym_response)

            self.message.show('\n12. Comparing Trust Anchor verkey as written by Steward and as retrieved in GET_NYM '
                              'response submitted by Client\n')

            self.message.show('Written by Steward: ', trust_anchor_verkey)
            verkey_from_ledger = json.loads(get_nym_response['result']['data'])['verkey']

            self.message.show('Queried from ledger: ', verkey_from_ledger)
            self.message.show('Matching: ', verkey_from_ledger == trust_anchor_verkey)
            self.message.show('\n13. Closing wallet and pool\n')
            await wallet.close_wallet(wallet_handle)
            await pool.close_pool_ledger(pool_handle)

            self.message.show('\n14. Deleting created wallet\n')
            await wallet.delete_wallet(self.local_config.wallet_config, self.local_config.wallet_credentials)

            self.message.show('\n15. Deleting pool ledger config\n')
            await pool.delete_pool_ledger_config(self.local_config.pool_name)

        except IndyError as e:
            print('Error occurred: %s' % e)


