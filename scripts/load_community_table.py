from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, UnicodeSetAttribute
)
import json

class Community(Model):
    class Meta:
        table_name = "Communities"
        host = "http://localhost:8000"
        region = "us-east-1"
    
    community_ticker = UnicodeAttribute(hash_key=True)
    community_name = UnicodeAttribute()
    owners = UnicodeSetAttribute(default=[])
    profile_img = UnicodeAttribute(null=True)
    background_img = UnicodeAttribute(null=True)


def main():
    data_file = "scripts/data/communitydata.json"
    with open(data_file) as f:
        data = json.load(f)
    for item in data["data"]:
        print(item)
        c = Community(item['community_ticker'], community_name=item['community_name'], owners=item['owners'])
        c.save()
    
    print(Community.count())

main()