from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, JSONAttribute, BooleanAttribute
)
from utils.envar import getEnvironmentVariable
from utils.constants import DYNAMODB_HOST_URL, DYNAMODB_POST_TABLE_NAME

class Post(Model):
    class Meta:
        table_name = DYNAMODB_POST_TABLE_NAME
        if (getEnvironmentVariable(DYNAMODB_HOST_URL)):
            host = getEnvironmentVariable(DYNAMODB_HOST_URL)
    
    community_ticker = UnicodeAttribute(hash_key=True)
    post_id = UnicodeAttribute(range_key=True)
    title = UnicodeAttribute()
    body = UnicodeAttribute(null=True)
    creation_date = UTCDateTimeAttribute()
    private = BooleanAttribute()