from utils.constants import AUTHORIZATION, JWT_ALGORITHM, JWT_SECRET
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError
from services.postService import getPostsForCommunity, createPostForCommunity
from functions.session import isCommunityMember, isCommunityOwner, parseJWT, parseRequestCookieForVerifiedToken
from http import cookies
import jwt

class PostHandler:
    def getPosts(self, request, community):
        try:
            token_decoded = parseRequestCookieForVerifiedToken(request)
            if isCommunityMember(token_decoded['wallet'], token_decoded['session'], community):
                post_info = getPostsForCommunity(community, True)
            else:
                post_info = getPostsForCommunity(community, False)
        except:
            post_info = getPostsForCommunity(community, False)

        return {"posts" : post_info}, 200
        
    
    def createPost(self, request, community):
        token_decoded = parseRequestCookieForVerifiedToken(request)
        body = request.json_body
        if not isCommunityOwner(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No ownership found for " + community)
        post_info = createPostForCommunity(community, body)
        return post_info, 200