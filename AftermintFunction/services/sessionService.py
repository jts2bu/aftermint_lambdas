import requests
import jwt
from services.communityService import communityExists, isWalletOwner
from models.session import Session
from utils.constants import COVALENT_API_KEY, JWT_ALGORITHM, JWT_SECRET
from web3.auto import w3
from eth_account.messages import encode_defunct
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError


def validateSignature(walletAddress, signedMessage):
    message = encode_defunct(text="Welcome to Aftermint! We will scan you wallet on the following blockchain networks to gather your communities: Ethereum, Avalanche.")
    signed_address = w3.eth.account.recover_message(message, signature=signedMessage)
    return signed_address == walletAddress


def getCommunityTickersForWalletFromRemote(walletAddress, chain_id):
    queryParams = {
        'key': COVALENT_API_KEY,
        'nft': True,
        'no-nft-fetch': True
    }
    url = f"https://api.covalenthq.com/v1/{chain_id}/address/{walletAddress}/balances_v2/"
    r = requests.get(url, queryParams)
    if (r.status_code == 200):
        wallet_communities = []
        data = r.json()['data']
        for item in data['items']:
            if item['type'] == 'nft':
                wallet_communities.append(item['contract_ticker_symbol'])
        
        return wallet_communities
    else:
        return []


def getJWT(walletAddress, session, membership, ownership):

    data = {
        'wallet': walletAddress,
        'session': session,
        'membership': membership,
        'ownership': ownership
    }

    return jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)


def getMembershipAndOwnership(walletAddress, communityTickers):
    membership = []
    ownership = []

    for ticker in communityTickers:
        if (communityExists(ticker)):
            membership.append(ticker)
        if (isWalletOwner(walletAddress, ticker)):
            ownership.append(ticker)
    
    return membership, ownership

def hasActiveSession(walletAddress):
    try:
        Session.get(walletAddress)
        return True
    except Exception:
        return False

def isCommunityMember(walletAddress, session, community):
    try:
        active_session = Session.get(walletAddress, session)
        return community in active_session.membership
    except Exception as error:
        return False

def isCommunityOwner(walletAddress,session, community):
    try:
        active_session = Session.get(walletAddress, session)
        return community in active_session.ownership
    except Exception as error:
        return False

def parseJWT(jwt_string):
    if jwt_string == None:
        raise UnauthorizedError("Authentication token not found")
    try:
        token_decoded = jwt.decode(jwt_string, JWT_SECRET, JWT_ALGORITHM)
    except:
        raise BadRequestError("Token not formatted properly")
    if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
        raise UnauthorizedError("Authorization token missing parameters")
    return token_decoded
