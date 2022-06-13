from enum import Enum


DYNAMODB_HOST_URL = "DYNAMODB_HOST_URL"
DYNAMODB_REWARD_TABLE_NAME = "Aftermint_Rewards"
DYNAMODB_COMMUNITY_TABLE_NAME = "Aftermint_Communities"
DYNAMODB_POST_TABLE_NAME = "Aftermint_Posts"
DYNAMODB_SESSION_TABLE_NAME = "Aftermint_Active-Sessions"


JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"

WALLET_ADDRESS = "wallet_address"
MSG_SIGNATURE = "message_signature"
CHAIN_ID = "chain_id"
AUTHORIZATION = "Authorization"

MSG_TO_SIGN = "MESSAGE_TO_SIGN"


COVALENT_API_KEY = "ckey_bd00bca5b93a40b780556ae115f"
class COVALENT_CHAIN_IDS(Enum):
    ETH = 1
    AVAX = 43114