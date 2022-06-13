from models.community import Community

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