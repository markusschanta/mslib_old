import pandas as pd

from mslib.data import stocks
from mslib.finance import sharpe

def test_sharpe():
    price = stocks()
    returns = price.pct_change().dropna(how='all')
    sr = sharpe(returns, 12)
    assert sr.gt(-2).all()
    assert sr.lt(2).all()
