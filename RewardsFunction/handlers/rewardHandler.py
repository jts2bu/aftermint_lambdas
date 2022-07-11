from utils.constants import AUTHORIZATION, JWT_ALGORITHM, JWT_SECRET
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError
from services.rewardService import getRewardsForCommunity, getRewardInfo, createRewardForCommunity, addEntryToReward
from functions.session import isCommunityMember, isCommunityOwner, parseJWT, parseRequestCookieForVerifiedToken

from http import cookies
import jwt

class RewardHandler:
    def getRewards(self, request, community):
        token_decoded = parseRequestCookieForVerifiedToken(request)
        if not isCommunityMember(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No membership found for " + community)    
        rewards_info = getRewardsForCommunity(community)
        return {"rewards": rewards_info}, 200
    
    def createReward(self, request, community):
        token_decoded = parseRequestCookieForVerifiedToken(request)
        body = request.json_body
        if not isCommunityOwner(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No ownership found for " + community)
        reward_info = createRewardForCommunity(community, body)
        return reward_info, 200
    
    def getRewardInfo(self, request, community, reward):
        token_decoded = parseRequestCookieForVerifiedToken(request)
        if not isCommunityMember(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No membership found for " + community)    
        reward_info = getRewardInfo(community, reward)
        status_code = 200 if reward_info != None else 404
        return reward_info, status_code
    
    def submitEntry(self, request, community, reward):
        token_decoded = parseRequestCookieForVerifiedToken(request)
        wallet = request.json_body['wallet_address']
        if not isCommunityMember(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No membership found for " + community)
        entry_info = addEntryToReward(community, reward, wallet)
        return entry_info, 200

        