import json
from uuid import uuid4
from models.reward import Reward

def getRewardsForCommunity(community):
    rewards_info = []
    for reward in Reward.query(community):
        rewards_info.append(
            {
                "id": reward.reward_id,
                "title": reward.title,
                "subtitle": reward.subtitle,
                "end": reward.end,
                "img_url": reward.img_url
            }
        )
    return rewards_info

def getRewardInfo(community, rewardId):
    try:
        reward = Reward.get(community, rewardId)
    except:
        return None
    return {
        "id": reward.reward_id,
        "title": reward.title,
        "body": reward.body,
        "winners": reward.winners,
        "requirements": reward.requirements,
        "end": reward.end
    }

def createRewardForCommunity(community, data):
    uuid = uuid4()
    reward = Reward(hash_key=community, range_key=str(uuid), title=data['title'], body=data['body'], winners=data['winners'], end=data['end'], requirements=data['requirements'])
    reward.save()
    return {
        "id": reward.reward_id,
        "title": reward.title,
        "body": reward.body,
        "winners": reward.winners,
        "requirements": reward.requirements,
        "end": reward.end
    }

def addEntryToReward(community, reward_id, wallet_entry):
    reward = Reward.get(community, reward_id)
    if reward.entries == None:
        reward.entries = [wallet_entry]
    else:
        reward.entries.add(wallet_entry)
    reward.save()
    return {
        "entries": len(reward.entries)
    }