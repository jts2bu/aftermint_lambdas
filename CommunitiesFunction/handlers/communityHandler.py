from functions.session import isCommunityMember, parseJWT, parseRequestCookieForVerifiedToken
from utils.constants import AUTHORIZATION, JWT_ALGORITHM, JWT_SECRET
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError
from services.communityService import getCommunitiesInfoForWalletFromLocal, getCommunityInfoForTicker
from http import cookies
import jwt

class CommunityHandler:
    def getCommunities(self, request):
        token_decoded = parseRequestCookieForVerifiedToken(request)
        if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
            raise UnauthorizedError("Authorization token missing parameters")
        communityInfo = getCommunitiesInfoForWalletFromLocal(token_decoded['wallet'], token_decoded['session'])
        return communityInfo, 200
    
    def createCommunity(self, request):
        return {}
    
    def getCommunityInfo(self, request, community):
        community_info = getCommunityInfoForTicker(community)
        status_code = 200 if community_info != None else 404
        return community_info, status_code