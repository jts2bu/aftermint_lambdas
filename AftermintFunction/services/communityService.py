from models.session import Session
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError
from models.community import Community
from models.session import Session

def isWalletOwner(walletAddress, communityTicker):
    try:
        c = Community.get(communityTicker)
        if (c.owners):
            return walletAddress in c.owners
        else:
            return False
    except Exception as error:
        return False

def communityExists(communityTicker):
    try:
        Community.get(communityTicker)
        return True
    except:
        return False

def getCommunitiesInfoForWalletFromLocal(wallet, session):
    try:
        current_session = Session.get(wallet, session)
    except:
        raise UnauthorizedError("No session found for wallet: " + wallet)
    
    communities_info = []
    for community_ticker in current_session.membership:
        try:
            community_info = Community.get(community_ticker)
            communities_info.append(
                {
                    "name": community_info.community_name,
                    "id": community_info.community_ticker,
                    "profile_img": community_info.profile_img
                }
            )
        except:
            continue
    return {"communities" : communities_info}

def getCommunityInfoForTicker(ticker):
    try:
        community = Community.get(ticker)
    except:
        return None

    return {
        "name": community.community_name,
        "id": community.community_ticker,
        "profile_img": community.profile_img,
        "background_img": community.background_img
    }