from utils.constants import AUTHORIZATION, JWT_ALGORITHM, JWT_SECRET
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError, BadRequestError
from services.postService import getPostsForCommunity, createPostForCommunity
from services.sessionService import isCommunityMember, isCommunityOwner, parseJWT
from http import cookies
import jwt

class PostHandler:
    def getPosts(self, request, community):
        cookie = cookies.SimpleCookie()
        cookie.load(request.headers['Cookie'])
        if cookie['token'].value == None:
            raise UnauthorizedError("Authentication token not found")
        try:
            token_decoded = jwt.decode(cookie['token'].value, JWT_SECRET, JWT_ALGORITHM)
        except:
            raise BadRequestError("Token not formatted properly")
        if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
            raise UnauthorizedError("Authorization token missing parameters")
        if not isCommunityMember(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No membership found for " + community)    
        post_info = getPostsForCommunity(community)
        return {"posts" : post_info}, 200
        
    
    def createPost(self, request, community):
        cookie = cookies.SimpleCookie()
        cookie.load(request.headers['Cookie'])
        if cookie['token'].value == None:
            raise UnauthorizedError("Authentication token not found")
        try:
            token_decoded = jwt.decode(cookie['token'].value, JWT_SECRET, JWT_ALGORITHM)
        except:
            raise BadRequestError("Token not formatted properly")
        if (token_decoded['wallet'] == None or token_decoded['session'] == None or token_decoded['membership'] == None or token_decoded['ownership'] == None):
            raise UnauthorizedError("Authorization token missing parameters")
        body = request.json_body
        if not isCommunityOwner(token_decoded['wallet'], token_decoded['session'], community):
            raise UnauthorizedError("No ownership found for " + community)
        post_info = createPostForCommunity(community, body)
        return post_info, 200