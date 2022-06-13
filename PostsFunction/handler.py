import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.postHandler import PostHandler

logger = Logger(service="PostsFunction")

app = ApiGatewayResolver()

@app.get("/communities/<community>/posts")
def getPosts(community):
    ph = PostHandler()
    response, status = ph.getPosts(app.current_event, community)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.post("/communities/<community>/posts")
def createPost(community):
    ph = PostHandler()
    response, status = ph.createPost(app.current_event, community)
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps(response))
    return Response(
        body=json.dumps(response), content_type="application/json", status_code=status
    )

@app.get("/posts_health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)
