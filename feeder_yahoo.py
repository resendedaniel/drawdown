from pandas_datareader import data as pdr


def get_data(symbol):
    data = pdr.get_data_yahoo(symbol)
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
