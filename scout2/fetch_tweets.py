# Fetch tweets
from subprocess import check_output
import json
from searchtweets import (ResultStream,
                          load_credentials,
                          merge_dicts,
                          read_config,
                          write_result_stream,
                          gen_params_from_config)

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
        configfile_dict = read_config("config.yaml")

        creds_dict = load_credentials(filename="config.yaml",
                                      yaml_key="search_tweets_v2",
                                      env_overwrite=False)

        query = prepareQuery(w)

        args_dict = {
            "query": "({}) has:images".format(query),
            "output_format": "a"
        }

        dict_filter = lambda x: {k: v for k, v in x.items() if v is not None}

        config_dict = merge_dicts(dict_filter(configfile_dict),
                                  dict_filter(creds_dict),
                                  dict_filter(args_dict))

        stream_params = gen_params_from_config(config_dict)

        rs = ResultStream(tweetify=False, **stream_params)

        result += list(rs.stream())

    return result if len(result) != 0 else None


