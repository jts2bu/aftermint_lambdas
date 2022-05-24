import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, ALBResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.communityHandler import CommunityHandler
from handlers.postHandler import PostHandler
from handlers.rewardHandler import RewardHandler
from handlers.sessionHandler import SessionHandler

from models.community import Community
from models.post import Post
from models.reward import Reward
from models.session import Session

logger = Logger(service="APP")

app = APIGatewayRestResolver()

if not Community.exists():
    Community.create_table(wait=True, read_capacity_units=5, write_capacity_units=5)

if not Post.exists():
    Post.create_table(wait=True, read_capacity_units=5, write_capacity_units=5)
    
if not Reward.exists():
    Reward.create_table(wait=True, read_capacity_units=5, write_capacity_units=5)

if not Session.exists():
    Session.create_table(wait=True, read_capacity_units=5, write_capacity_units=5)

@app.post("/api/login")
def login():
    sh = SessionHandler()
    token, status = sh.login(app.current_event)

    response_headers = {
        "Set-Cookie": f"token={token}; httponly"
    }
    return Response(
        body=json.dumps({"token" : token}), content_type="application/json", status_code=status, headers=response_headers
    )

@app.post("/api/logout")
def logout():
    sh = SessionHandler()
    status = sh.logout(app.current_event)
    response_headers = {
        'Set-Cookie' : 'token=; expires=Thu, 01 Jan 1970 00:00:00 GMT'
    }
    return Response(body="", content_type="application/json", status_code=status, headers=response_headers)

@app.get("/api/communities")
def getCommunities():
    ch = CommunityHandler()
    response, status = ch.getCommunities(app.current_event)
    return Response (
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/api/communities")
def requestCommunity():
    ch = CommunityHandler()
    return ch.createCommunity(app.current_event)

@app.get("/api/communities/<community>")
def getCommunityInfo(community):
    ch = CommunityHandler()
    response, status = ch.getCommunityInfo(app.current_event, community)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.get("/api/communities/<community>/posts")
def getPosts(community):
    ph = PostHandler()
    response, status = ph.getPosts(app.current_event, community)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/api/communities/<community>/posts")
def createPost(community):
    ph = PostHandler()
    response, status = ph.createPost(app.current_event, community)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.get("/api/communities/<community>/rewards")
def getRewards(community):
    rh = RewardHandler()
    response, status = rh.getRewards(app.current_event, community)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/api/communities/<community>/rewards")
def createReward(community):
    rh = RewardHandler()
    response, status = rh.createReward(app.current_event, community)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )


@app.get("/api/communities/<community>/rewards/<rewardId>")
def getRewardInfo(community, rewardId):
    rh = RewardHandler()
    response, status = rh.getRewardInfo(app.current_event, community, rewardId)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/api/communities/<community>/rewards/<rewardId>/submit")
def submitRewardEntry(community, rewardId):
    rh = RewardHandler()
    response, status = rh.submitEntry(app.current_event, community, rewardId)
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.get("/health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}

@app.route(method="OPTIONS", rule=".*") # Matches any pre-flight request coming from API Gateway
def preflight_handler():
    preflight_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Request-Method": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Request-Headers": "Content-Type"
    }
    return Response(body="", status_code=200, content_type="application/json", headers=preflight_headers)

def lambda_handler(event, context):
    return app.resolve(event, context)
