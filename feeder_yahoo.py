import yfinance as yf
import pandas as pd
import datetime as dt


def get_data(symbol, start_date=dt.datetime(2010, 1, 1)):
    start = {
        '^BVSP': dt.datetime(1996, 1, 1),
        '^GSPC': dt.datetime(1910, 1, 1),
        '^IXIC': dt.datetime(1910, 1, 1)
    }
    #    yf.pdr_override() # <== that's all it takes :-)
    data = yf.download(symbol, interval='1d')
    data = data.reset_index()
    data = data.rename(columns={
        'Date': 'd',
        'High': 'high',
        'Low': 'low',
        'Close': 'value',
        #'Adj Close': 'value',
        'Open': 'open',
        'Volume': 'volume'
    })
    x = pd.DataFrame()
    x['d'] = data['d']
    x['value'] = data['value']
    x['d'] = pd.to_datetime(x['d'])

    return x

def process_data(data):
    data['delta'] = data['close'].diff()
    data['delta'] = data['delta'].fillna(0)
    data['delta'] = data['close'] / (data['close'] - data['delta'])

    return data
