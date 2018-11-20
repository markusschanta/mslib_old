import json
import time
import urllib.request

import pandas as pd


def get_coin_list():
    list_url = "https://s2.coinmarketcap.com/generated/search/quick_search.json"
    with urllib.request.urlopen(list_url) as url:
        data = json.loads(url.read().decode())
    coin_list = pd.DataFrame(data).set_index('rank').loc[:, ('slug', 'symbol', 'name')]
    return coin_list


def get_market_data_single(slug, resample='d'):
    market_data_url = "https://graphs2.coinmarketcap.com/currencies/%s/" % slug
    print("Fetching market data for: %s" % slug)
    time.sleep(1.5)
    with urllib.request.urlopen(market_data_url) as url:
        data = json.loads(url.read().decode())
    market_data = pd.concat({k: pd.Series(dict(v)) for k, v in data.items()}, axis=1)
    market_data.index = pd.to_datetime(list(market_data.index),unit='ms')
    if resample:
        market_data = market_data.resample(resample).last()
    return market_data

def get_market_data(slugs=None, n=10):
    if slugs != None:
        n = len(slugs)
    else:
        slugs = get_coin_list().slug.iloc[:n]

    market_data = {c: get_market_data_single(c) for c in slugs}
    market_data = pd.concat(market_data, axis=1, names=['slug', 'metric'])
    return market_data
