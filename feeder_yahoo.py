from pandas_datareader import data as pdr
import datetime as dt


def get_data(symbol):
    start = {
        '^BVSP': dt.datetime(2000, 1, 1),
        '^GSPC': dt.datetime(1910, 1, 1)
    }
    #    yf.pdr_override() # <== that's all it takes :-)
    data = pdr.get_data_yahoo(symbol, start[symbol])
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

    return data
