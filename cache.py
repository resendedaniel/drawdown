import os
import pandas as pd


def save_crashes(data, symbol):
    #    date_str = dt.datetime.today().isoformat()[:10]
    data.to_json('data/crashes_{}.json'.format(symbol))


def save_drawdown(data, symbol):
    #    date_str = dt.datetime.today().isoformat()[:10]
    data.to_json('data/drawdown_{}.json'.format(symbol))


def save_ibov_equity(df, symbol):
    df.to_csv('data/ibov/{}.csv'.format(symbol), index=False)


def check_equity_data_availability(symbol):
    return os.path.exists('data/ibov/{}.csv'.format(symbol))


def load_equity_data(symbol):
    df = pd.read_csv('data/ibov/{}.csv'.format(symbol))
    df['d'] = pd.to_datetime(df['d'])

    return df
