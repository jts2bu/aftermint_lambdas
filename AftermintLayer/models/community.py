from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, UnicodeSetAttribute
)
from utils.envar import getEnvironmentVariable
from utils.constants import DYNAMODB_HOST_URL, DYNAMODB_COMMUNITY_TABLE_NAME

class Community(Model):
    class Meta:
        table_name = DYNAMODB_COMMUNITY_TABLE_NAME
        if (getEnvironmentVariable(DYNAMODB_HOST_URL)):
            host = getEnvironmentVariable(DYNAMODB_HOST_URL)
        region = "us-east-1"
    
    community_ticker = UnicodeAttribute(hash_key=True)
    community_name = UnicodeAttribute()
    owners = UnicodeSetAttribute()
    profile_img = UnicodeAttribute(null=True)
    background_img = UnicodeAttribute(null=True)