from time import time
from uuid import uuid4
from models.post import Post


def getPostsForCommunity(community, user_is_member):
    posts_info = []
    for post in Post.query(community):
        if user_is_member or not post.private:
            posts_info.append(
                {
                    "id": post.post_id,
                    "title": post.title,
                    "body": post.body,
                    "creation_date": post.creation_date,
                    "private": post.private
                }
            )
    return posts_info

def createPostForCommunity(community, data):
    uuid = uuid4()
    now = time()
    post = Post(hash_key=community, range_key=str(uuid), title=data['title'], body=data['body'], creation_date=now)
    post.save()
    return {
        "id": post.post_id,
        "title": post.title,
        "body": post.body,
        "creation_date": post.creation_date,
        "private": post.private
    }