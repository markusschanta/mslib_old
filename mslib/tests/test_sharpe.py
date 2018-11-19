from finance import sharpe
import pandas as pd

def test_sharpe():
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    sharpe(df)
