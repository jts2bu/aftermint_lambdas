import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, ALBResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.sessionHandler import SessionHandler


logger = Logger(service="APP")

app = APIGatewayRestResolver()

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

@app.get("/health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}

def lambda_handler(event, context):
    return app.resolve(event, context)
