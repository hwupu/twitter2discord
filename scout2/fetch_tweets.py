# Fetch tweets
from subprocess import check_output
import json

def groupWatchlist(watchlist: list) -> list:
    """ Due to query limit of 512 char, we seperate the list to multiple requests """
    result = []
    temp = []
    count = 0
    for w in watchlist:
        if count < 450:
            temp.append(w)
            count += len(w) + 9
        else:
            result.append(temp)
            temp = [w]
            count = len(w) + 9

    result.append(temp)
    return result


def prepareQuery(watchlist: list) -> str:
    """ Prepare query string by joining watchlist """
    return " OR ".join(["from:{}".format(w) for w in watchlist])


def fetch(watchlist: list) -> list:
    """ Fetch tweets """
    result = []

    for w in groupWatchlist(watchlist):
        query = prepareQuery(w)
        out = check_output(["python",
                            "scout/search_tweets.py",
                            "--credential-file",
                            "config.yaml",
                            "--config-file",
                            "config.yaml",
                            "--query",
                            "({}) has:images".format(query)])
        if out:
            result.append(json.loads(out))

    print(result)
    return result if len(result) != 0 else None
