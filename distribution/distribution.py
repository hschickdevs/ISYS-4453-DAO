from web3 import Web3
from web3.middleware import geth_poa_middleware

from pathlib import Path
from os import getenv
import json
from dotenv import load_dotenv


"""Voting Tokens Will Need to Be Distributed to all classmates"""
USERS = ['0x13751DC2749A3fC61f4B2Ca5F5c09bd31062EF0A']
VOTING_TOKEN_ADDRESS = "0xfd269D0f2C3f268471d3585E4B3c8213AeE22A4d"  # "0xc7Ca49101464e7684a3AF5c94A901ee83359a461"  <- Real address


if __name__ == "__main__":
    load_dotenv(dotenv_path=Path(__file__).parent.joinpath('.env'))
    assert getenv('PRIVATE_KEY') and getenv('MUMBAI_INFURA_URL') and getenv('WALLET_ADDRESS')
    
    web3 = Web3(Web3.HTTPProvider(getenv('MUMBAI_INFURA_URL')))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    VotingToken = web3.eth.contract(address=Web3.toChecksumAddress(VOTING_TOKEN_ADDRESS),
                                    abi=json.load(open(Path(__file__).parent.joinpath('abi', 'token.json'))))
    decimals = VotingToken.functions.decimals().call()
    name = VotingToken.functions.name().call()

    for user in USERS:
        transfer_amount = 1 * (10 ** decimals)
        try:
            bal = VotingToken.functions.balanceOf(Web3.toChecksumAddress(user)).call()
            assert bal < transfer_amount, f'User already has {bal / (10 ** decimals)} voting tokens'
            
            tx = VotingToken.functions.transfer(Web3.toChecksumAddress(user), transfer_amount).buildTransaction({
                "from": Web3.toChecksumAddress(getenv('WALLET_ADDRESS')),
                'chainId': 80001,  # 80001: Mumbai testnet
                # 'gas': 76335152,
                'nonce': web3.eth.getTransactionCount(getenv('WALLET_ADDRESS')),
            })
            signed_txn = web3.eth.account.sign_transaction(
                tx, private_key=getenv('PRIVATE_KEY')
            )
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            receipt = dict(web3.eth.wait_for_transaction_receipt(tx_hash))
            
            print(f'Sent {transfer_amount / (10) ** decimals} {name} to {user} - Receipt: {receipt}')
        except Exception as err:
            print(f'Could not send tokens to {user} - {err}')

