import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, ALBResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.rewardHandler import RewardHandler

logger = Logger(service="APP")

app = APIGatewayRestResolver()

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

def lambda_handler(event, context):
    return app.resolve(event, context)
