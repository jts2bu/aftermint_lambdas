import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, ALBResolver, ApiGatewayResolver
from aws_lambda_powertools.event_handler.api_gateway import Response, CORSConfig
from http import cookies

from handlers.sessionHandler import SessionHandler


logger = Logger(service="SessionsFunction")

app = ApiGatewayResolver()

@app.post("/login")
def login():
    sh = SessionHandler()
    token, status = sh.login(app.current_event)

    response_headers = {
        "Set-Cookie": f"token={token}; httponly"
    }
    logger.info("Status Code: " + str(status))
    logger.info("Response: " + json.dumps({"token" : token}))
    return Response(
        body=json.dumps({"token" : token}), content_type="application/json", status_code=status, headers=response_headers
    )

@app.post("/logout")
def logout():
    sh = SessionHandler()
    status = sh.logout(app.current_event)
    response_headers = {
        'Set-Cookie' : 'token=; expires=Thu, 01 Jan 1970 00:00:00 GMT'
    }
    return Response(body="", content_type="application/json", status_code=status, headers=response_headers)

@app.get("/sessions_health")
def health():
    logger.info("Health Check Request")
    return {"status": "HEALTHY"}

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)
