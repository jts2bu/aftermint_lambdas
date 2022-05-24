from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, JSONAttribute
)
from utils.envar import getEnvironmentVariable
from utils.constants import DYNAMODB_HOST_URL, DYNAMODB_REWARD_TABLE_NAME

class Reward(Model):
    class Meta:
        table_name = DYNAMODB_REWARD_TABLE_NAME
        if (getEnvironmentVariable(DYNAMODB_HOST_URL)):
            host = getEnvironmentVariable(DYNAMODB_HOST_URL)
    
    community_ticker = UnicodeAttribute(hash_key=True)
    reward_id = UnicodeAttribute(range_key=True)
    title = UnicodeAttribute()
    subtitle = UnicodeAttribute()
    body = UnicodeAttribute(null=True)
    winners = NumberAttribute()
    end = UTCDateTimeAttribute()
    entries = UnicodeSetAttribute()
    requirements = JSONAttribute()
    img_url = UnicodeAttribute(null = True)