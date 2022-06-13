from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, TTLAttribute, UnicodeSetAttribute
)
from utils.envar import getEnvironmentVariable
from utils.constants import DYNAMODB_HOST_URL, DYNAMODB_SESSION_TABLE_NAME

class Session(Model):
    class Meta:
        table_name = DYNAMODB_SESSION_TABLE_NAME
        if (getEnvironmentVariable(DYNAMODB_HOST_URL)):
            host = getEnvironmentVariable(DYNAMODB_HOST_URL)
    
    wallet_address = UnicodeAttribute(hash_key=True)
    session_id = UnicodeAttribute(range_key=True)
    membership = UnicodeSetAttribute(null = True)
    ownership = UnicodeSetAttribute(null = True)
    expiration = TTLAttribute(null=True)