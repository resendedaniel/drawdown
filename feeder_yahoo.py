from pandas_datareader import data as pdr
import datetime as dt
import pandas as pd


def get_data(symbol, start_date=dt.datetime(2010, 1, 1)):
    start = {
        '^BVSP': dt.datetime(2000, 1, 1),
        '^GSPC': dt.datetime(1910, 1, 1)
    }
    #    yf.pdr_override() # <== that's all it takes :-)
    data = pdr.get_data_yahoo(symbol, start.get(symbol, start_date))
    data = data.reset_index()
    data = data.rename(columns={
        'Date': 'd',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'value',
        'Open': 'open',
        'Volume': 'volume'
    })
    data['d'] = pd.to_datetime(data['d'])

    return data

def process_data(data):
    data['delta'] = data['close'].diff()
    data['delta'] = data['delta'].fillna(0)
    data['delta'] = data['close'] / (data['close'] - data['delta'])

    return data
