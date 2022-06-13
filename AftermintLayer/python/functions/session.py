from utils.constants import COVALENT_API_KEY, JWT_ALGORITHM, JWT_SECRET
from models.session import Session
from web3.auto import w3
from eth_account.messages import encode_defunct
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError
from functions.community import isWalletOwner, communityExists

import jwt

def getJWT(walletAddress, session, membership, ownership):
    data = {
        'wallet': walletAddress,
        'session': session,
        'membership': membership,
        'ownership': ownership
    }
    return jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)

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

def isCommunityOwner(walletAddress, session, community):
    try:
        active_session = Session.get(walletAddress, session)
        return community in active_session.ownership
    except Exception as error:
        return False