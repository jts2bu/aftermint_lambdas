from time import sleep
import requests
from utils.constants import COVALENT_API_KEY, COVALENT_CHAIN_IDS
from web3.auto import w3
from eth_account.messages import encode_defunct

def validateSignature(walletAddress, signedMessage):
    message = encode_defunct(text="Welcome to Aftermint! We will scan you wallet on the following blockchain networks to gather your communities: Ethereum, Avalanche.")
    signed_address = w3.eth.account.recover_message(message, signature=signedMessage)
    return signed_address == walletAddress

def getCommunityTickersForWalletFromRemote(walletAddress):
    queryParams = {
        'key': COVALENT_API_KEY,
        'nft': True,
        'no-nft-fetch': True
    }
    wallet_communities = []
    for chain in COVALENT_CHAIN_IDS:
        chain_id = str(chain.value)
        url = f"https://api.covalenthq.com/v1/{chain_id}/address/{walletAddress}/balances_v2/"
        r = requests.get(url, queryParams)
        while (r.status_code == 502):
            sleep(.333)
            r = requests.get(url, queryParams)
        if (r.status_code == 200):
            data = r.json()['data']
            for item in data['items']:
                if item['type'] == 'nft':
                    wallet_communities.append(item['contract_ticker_symbol'])
    
    return wallet_communities