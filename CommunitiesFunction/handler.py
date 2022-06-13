import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.communityHandler import CommunityHandler

logger = Logger(service="CommunitiesFunction")

app = ApiGatewayResolver()

@app.get("/communities")
def getCommunities():
    ch = CommunityHandler()
    response, status = ch.getCommunities(app.current_event)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response (
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/communities")
def requestCommunity():
    ch = CommunityHandler()
    return ch.createCommunity(app.current_event)

@app.get("/communities/<community>")
def getCommunityInfo(community):
    ch = CommunityHandler()
    response, status = ch.getCommunityInfo(app.current_event, community)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.get("/communities_health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)