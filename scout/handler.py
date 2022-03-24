# Load watchlist and call relevant parser.
import os
import logging
import json
from json.decoder import JSONDecodeError

from . import database
from . import fetch_tweets
from . import post_discord

logger = logging.getLogger()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "ERROR"))
#logger.setLevel(logging.DEBUG)

def load_watchlist() -> list:
    """ Try to read watchlist json and return as list of dict """
    try:
        f = open("watchlist.json", "r")
        j = json.load(f)
        return j if type(j) is list else [j]
    except JSONDecodeError as e:
        logger.critical("\033[1;31mError parsing watchlist.json.\033[m")
        raise e
    except FileNotFoundError:
        logger.critical("\033[1;31mUnable to find watchlist.json.\033[m")
        exit(1)
    finally:
        if f:
            f.close()


def get_prop(dictionary: dict, key: str) -> str:
    """ Try to catch KeyError if there are any mistake in watchlist """
    try:
        return dictionary[key]
    except KeyError:
        logger.critical("\033[1;31mUnable to locate \"{}\" in watchlist.json.\033[m".format(key))
        exit(1)


def main():
    """ Load watchlist and call relevant parser """
    watchlists = load_watchlist()

    for watchlist in watchlists:
        tweets = None

        source = get_prop(watchlist, "from")
        if  source == "twitter":
            logger.debug("Fetch from Twitter")
            ww = get_prop(watchlist, "watchlist")
            tweets = fetch_tweets.fetch(ww)
        else:
            logger.warning("{} is not supported as source platform.".format(source))

        if tweets:
            tweets = [tweet for tweet in tweets if not database.hasTweetBeenPosted(tweet['id'])]
        
        if not tweets or len(tweets) == 0:
            logger.debug("No tweets found.")
            continue

        for tweet in tweets:
            database.storeTweetToDatabse(tweet["id"])

        destination = get_prop(watchlist, "to")
        if destination == "discord":
            logger.debug("Post to Discord")
            webhook = get_prop(watchlist, "webhook")
            post_discord.post(tweets, webhook)
        else:
            logger.warning("{} is not supported as destination platform.".format(destination))


