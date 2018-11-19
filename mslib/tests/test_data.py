import pandas as pd

from mslib.data import stocks

def test_stocks():
    s = stocks()
    assert len(s) > 100
    assert pd.Series(['AAPL', 'AMZN', 'GOOG', 'IBM', 'MSFT']).isin(s.columns).all()
    assert s.index.name == 'date'
    assert s.columns.name == 'symbol'