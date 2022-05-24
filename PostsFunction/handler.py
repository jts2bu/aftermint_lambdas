import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, ALBResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.postHandler import PostHandler

logger = Logger(service="APP")

app = APIGatewayRestResolver()

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

@app.get("/health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}

def lambda_handler(event, context):
    return app.resolve(event, context)
