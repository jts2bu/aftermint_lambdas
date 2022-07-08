from functions.session import isCommunityMember, parseJWT
from utils.constants import AUTHORIZATION, JWT_ALGORITHM, JWT_SECRET
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError
from services.communityService import getCommunitiesInfoForWalletFromLocal, getCommunityInfoForTicker
from http import cookies
import jwt

class CommunityHandler:
    def getCommunities(self, request):
        cookie = cookies.SimpleCookie()
        if 'Cookie' not in request.headers:
            raise UnauthorizedError("Cookie not found")
        if request.headers['Cookie'] is None:
            raise UnauthorizedError("Cookie not found")
        cookie.load(request.headers['Cookie'])
        if cookie['token'].value == None:
            raise UnauthorizedError("Authentication token not found")
        try:
            token_decoded = jwt.decode(cookie['token'].value, JWT_SECRET, JWT_ALGORITHM)
        except:
            raise BadRequestError("Token not formatted properly")
        if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
            raise UnauthorizedError("Authorization token missing parameters")
        communityInfo = getCommunitiesInfoForWalletFromLocal(token_decoded['wallet'], token_decoded['session'])
        return communityInfo, 200
    
    def createCommunity(self, request):
        return {}
    
    def getCommunityInfo(self, request, community):
        cookie = cookies.SimpleCookie()
        if 'Cookie' not in request.headers:
            raise UnauthorizedError("Cookie not found")
        if request.headers['Cookie'] is None:
            raise UnauthorizedError("Cookie not found")
        cookie.load(request.headers['Cookie'])
        if cookie['token'].value == None:
            raise UnauthorizedError("Authentication token not found")
        try:
            token_decoded = jwt.decode(cookie['token'].value, JWT_SECRET, JWT_ALGORITHM)
        except:
            raise UnauthorizedError("Token not formatted properly")
        if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
            raise UnauthorizedError("Authorization token missing parameters")
        if not isCommunityMember(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No membership found for " + community)
        community_info = getCommunityInfoForTicker(community)
        status_code = 200 if community_info != None else 404
        return community_info, status_code