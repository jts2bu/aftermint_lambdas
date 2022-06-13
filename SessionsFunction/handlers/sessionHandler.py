import json
from uuid import uuid4
from models.session import Session
from services.sessionService import getCommunityTickersForWalletFromRemote, validateSignature
from functions.session import getJWT, getMembershipAndOwnership

from utils.constants import CHAIN_ID, MSG_SIGNATURE, WALLET_ADDRESS, JWT_ALGORITHM, JWT_SECRET
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, InternalServerError, UnauthorizedError
from http import cookies
import jwt

class SessionHandler:
    def login(self, request):
        try:
            wallet = request.json_body.get(WALLET_ADDRESS)
            signature = request.json_body.get(MSG_SIGNATURE)
        except:
            raise BadRequestError("Missing body parameter")
        
        if (wallet == None or signature == None):
            raise BadRequestError("Missing body parameter")

        if validateSignature(wallet, signature):
            all_tickers = getCommunityTickersForWalletFromRemote(wallet)
            wallet_membership, wallet_ownership = getMembershipAndOwnership(wallet, all_tickers)
            session_id = uuid4()
            jwt_token = getJWT(walletAddress=wallet, session=str(session_id), membership=wallet_membership, ownership=wallet_ownership)

            new_session = Session(hash_key=wallet, range_key=str(session_id), membership=wallet_membership, ownership=wallet_ownership)
            new_session.save()
            return jwt_token, 201

        else: raise BadRequestError("Could not validate signature")
    
    def logout(self, request):
        cookie = cookies.SimpleCookie()
        if request.headers['Cookie'] is None:
            raise BadRequestError("Cookie not found")
        cookie.load(request.headers['Cookie'])
        if cookie['token'].value == None:
            raise UnauthorizedError("Authentication token not found")
        try:
            token_decoded = jwt.decode(cookie['token'].value, JWT_SECRET, JWT_ALGORITHM)
        except:
            raise BadRequestError("Token not formatted properly")
        if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
            raise UnauthorizedError("Authorization token missing parameters")
        active_session = Session.get(token_decoded['wallet'], token_decoded['session'])
        active_session.delete()
        return 204