# Post tweets to Discord
import logging
import requests
import time

logger = logging.getLogger()

def hasImageUrl(media: list) -> bool:
    for m in media:
        if "url" not in m:
            return False
    return True


def post(tweets: list, webhook: str):
    """ POST to Discord webhook """
    for tweet in tweets:

        source_author = "[debug] source: @{}".format(tweet["author"]["username"])
        t = tweet["referenced_tweets"][0] if "referenced_tweets" in tweet else tweet

        if "attachments" not in t or not hasImageUrl(t["attachments"]["media"]):
            logger.info("Tweet contain no image: {}".format(t["id"]))
            continue

        payload = {
            "username": "{} (@{})".format(t["author"]["name"], t["author"]["username"]),
            "avatar_url": t["author"]["profile_image_url"],
            "content": t["text"],
            "embeds": [
                {"description": source_author},
                {"image": {"url": a["url"]}} for a in t["attachments"]["media"],
            ],
        } 

        result = requests.post(webhook, json=payload)

        if 200 <= result.status_code < 300:
            logger.info("{}:Posted tweet:{}".format(result.status_code, tweet["id"]))
        else:
            logger.warning("{}:Fail to posted tweet:{}".format(result.status_code, tweet["id"]))
            logger.warning("Responce:{}".format(result.json()))

        time.sleep(1)
