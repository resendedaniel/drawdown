import feeder_yahoo
import process
import plot
import cache
import symbols
import datetime as dt
import pandas as pd


def cache_symbols(symbols):
    for symbol in symbols:
        if not cache.check_equity_data_availability(symbol):
            print(symbol)
            symbol = '{}.SA'.format(symbol)
            data = feeder_yahoo.get_data(symbol, dt.datetime(2020, 2, 19))
            symbol = symbol.replace('.SA', '')
            df = process.crash_2020(data)
            cache.save_ibov_equity(df, symbol)


def load_symbols(symbols):
    falls = pd.DataFrame()
    for symbol in symbols:
        df = cache.load_equity_data(symbol)
        df['symbol'] = symbol
        df = df[['symbol', 'd', 'cumdelta']]
        falls = pd.concat([falls, df])

    falls = falls.reset_index(drop=True).sort_values(['symbol', 'd'])

    return falls


cache_symbols(symbols.ibrxa_symbols)
falls = load_symbols(symbols.ibrxa_symbols)

plot.crash_2020_trajectories(falls)
