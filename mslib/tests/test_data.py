import pandas as pd

from mslib.data import stocks
from mslib.data.bitcoin.coinmarketcap import get_coin_list, get_market_data_single, get_market_data

def test_stocks():
    s = stocks()
    assert len(s) > 100
    assert pd.Series(['AAPL', 'AMZN', 'GOOG', 'IBM', 'MSFT']).isin(s.columns).all()
    assert s.index.name == 'date'
    assert s.columns.name == 'symbol'

def test_coinmarketcap_get_coin_list():
    cl = get_coin_list()
    assert len(cl) > 1000
    assert pd.Series(['slug', 'symbol', 'name']).isin(cl.columns).all()
    assert cl.index.name == 'rank'
    
def test_coinmarketcap_get_market_data_single():
    btc = get_market_data_single('bitcoin')
    assert len(btc) > 1000
    expected_columns = ['market_cap_by_available_supply', 'price_btc', 'price_usd', 'volume_usd']
    assert pd.Series(expected_columns).isin(btc.columns).all()

def test_coinmarketcap_get_market_data():
    market_data = get_market_data(n=2)
    assert len(market_data) > 1000
    assert len(market_data.columns) >= 8
    assert market_data.columns.names == ['slug', 'metric']
