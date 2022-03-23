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

# Database connection
conn = None

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


def run():
    """ Load watchlist and call relevant parser """
    watchlists = load_watchlist()

    for watchlist in watchlists:
        tweets = None

        source = get_prop(watchlist, "from")
        if  source == "twitter":
            logger.debug("Fetch from Twitter")
            tweets = fetch_tweets.fetch()
        else:
            logger.warning("Source platform is not supported.")

        if not tweets:
            logger.debug("No tweets found.")
            continue

        destination = get_prop(watchlist, "to")
        if destination == "discord":
            logger.debug("Post to Discord")
            post_discord.post(get_prop(watchlist, "webhook"))
        else:
            logger.warning("Destination platform is not supported.")


def main():
    """ Try to catch interupts """
    try:
        global conn
        conn = database.connect()
        run()
    except KeyboardInterrupt:
        print('\033[1;30mKeyboardInterrupt\033[m')
    except EOFError:
        print('\033[1;30mEOFError\033[m')
    finally:
        database.close(conn)


