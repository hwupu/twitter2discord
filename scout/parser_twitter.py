from searchtweets import (ResultStream,
                          load_credentials,
                          merge_dicts,
                          read_config,
                          gen_params_from_config)

def get(config):
    """ Fetch new tweets """
    creds_dict = load_credentials("config.yaml",
                                  yaml_key="search_tweets_v2",
                                  env_overwrite=False)
    
    dict_filter = lambda x: {k: v for k, v in x.items() if v is not None}

    joint_from = ' OR '.join(['from:{}'.format(tw) for tw in config['scout']['twitter-ids']])

    query_dict = {
        #'query': '({}) {}'.format(joint_from, config['search_rules']['base-query']),
        'query': '{} {}'.format('from:tapioca_tw', config['search_rules']['base-query']),
    }

    configfile_dict = read_config('config.yaml')

    config_dict = merge_dicts(dict_filter(query_dict),
                              dict_filter(configfile_dict),
                              dict_filter(creds_dict))

    stream_params = gen_params_from_config(config_dict)
    print(stream_params)

    rs = ResultStream(tweetify=False, **stream_params)
    stream = rs.stream()
    
    for tweet in stream:
        print(json.dumps(tweet))
