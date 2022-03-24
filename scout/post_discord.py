# Post tweets to Discord
import logging
import requests

logger = logging.getLogger()

def post(tweets: list, webhook: str):
    """ POST to Discord webhook """
    for tweet in tweets:

        t = tweet["referenced_tweets"][0] if "referenced_tweets" in tweet else tweet

        if "attachments" not in t:
            logger.info("Tweet contain no image: {}".format(t["id"]))
            continue

        for media in t["attachments"]["media"]:
            if "url" not in media:
                logger.info("Tweet contain no image: {}".format(t["id"]))
                continue

        payload = {
            "username": "{} (@{})".format(t["author"]["name"], t["author"]["username"]),
            "avatar_url": t["author"]["profile_image_url"],
            "content": t["text"],
            "embeds": [ {"image": {"url": a["url"]}} for a in t["attachments"]["media"]],
        } 

        result = requests.post(webhook, json=payload)

        if 200 <= result.status_code < 300:
            logger.info("{}:Posted tweet:{}".format(result.status_code, tweet["id"]))
        else:
            logger.warning("{}:Fail to posted tweet:{}".format(result.status_code, tweet["id"]))
            logger.warning("Responce:{}".format(result.json()))
