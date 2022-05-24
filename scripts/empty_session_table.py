from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, UnicodeSetAttribute, TTLAttribute
)
import json

class Session(Model):
    class Meta:
        table_name = "Active-Sessions"
        host = "http://localhost:8000"
        region = "us-east-1"
    
    wallet_address = UnicodeAttribute(hash_key=True)
    session_id = UnicodeAttribute(range_key=True)
    membership = UnicodeSetAttribute(null = True)
    ownership = UnicodeSetAttribute(null = True)
    expiration = TTLAttribute(null=True)

def main():
    all_entries = Session.scan()
    for entry in all_entries:
        entry.delete()


main()