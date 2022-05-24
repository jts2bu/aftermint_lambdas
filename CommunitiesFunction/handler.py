import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, ALBResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.communityHandler import CommunityHandler

logger = Logger(service="APP")

app = APIGatewayRestResolver()

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