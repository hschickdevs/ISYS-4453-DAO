from web3 import Web3
from pathlib import Path
from os import getenv
import json
from dotenv import load_dotenv

"""Voting Tokens Will Need to Be Distributed to all classmates"""
USERS = []
VOTING_TOKEN_ADDRESS = "0xfd269D0f2C3f268471d3585E4B3c8213AeE22A4d"  # "0xc7Ca49101464e7684a3AF5c94A901ee83359a461"  <- Real address


if __name__ == "__main__":
    load_dotenv(dotenv_path=Path(__file__).parent.joinpath('.env'))
    assert getenv('PRIVATE_KEY') and getenv('MUMBAI_INFURA_URL') and getenv('WALLET_ADDRESS')
    
    web3 = Web3(Web3.HTTPProvider(getenv('MUMBAI_INFURA_URL')))
    
    VotingToken = web3.eth.contract(address=Web3.toChecksumAddress(VOTING_TOKEN_ADDRESS), 
                                    abi=json.load(open(Path(__file__).parent.joinpath('abi', 'token.json'))))
    decimals = VotingToken.functions.decimals().call()
    name = VotingToken.functions.name().call()

    for user in USERS:
        transfer_amount = 1 * (10 ** decimals)
        try:
            bal = VotingToken.functions.balanceOf(Web3.toChecksumAddress(user)).call()
            assert bal == 0, f'User already has {bal * (10 ** decimals)} voting tokens'
            
            tx = VotingToken.functions.transfer(Web3.toChecksumAddress(user), 1).buildTransaction({
                "from": Web3.toChecksumAddress(getenv('WALLET_ADDRESS')),
                'chainId': 80001,  # 80001: Mumbai testnet
                # 'gas': 76335152,
                'nonce': web3.eth.getTransactionCount(getenv('WALLET_ADDRESS')),
            })
            
            print(f'Sent {transfer_amount} {name} to {user}')
        except Exception as err:
            print(f'Could not send tokens to {user} - {err}')

