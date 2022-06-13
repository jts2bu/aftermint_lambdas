import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.rewardHandler import RewardHandler

logger = Logger(service="RewardsFunction")

app = ApiGatewayResolver()

@app.get("/communities/<community>/rewards")
def getRewards(community):
    rh = RewardHandler()
    response, status = rh.getRewards(app.current_event, community)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/communities/<community>/rewards")
def createReward(community):
    rh = RewardHandler()
    response, status = rh.createReward(app.current_event, community)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )


@app.get("/communities/<community>/rewards/<rewardId>")
def getRewardInfo(community, rewardId):
    rh = RewardHandler()
    response, status = rh.getRewardInfo(app.current_event, community, rewardId)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/communities/<community>/rewards/<rewardId>/submit")
def submitRewardEntry(community, rewardId):
    rh = RewardHandler()
    response, status = rh.submitEntry(app.current_event, community, rewardId)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.get("/rewards_health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)
