def save_crashes(data, symbol):
    #    date_str = dt.datetime.today().isoformat()[:10]
    data.to_json('data/crashes_{}.json'.format(symbol))


def save_drawdown(data, symbol):
    #    date_str = dt.datetime.today().isoformat()[:10]
    data.to_json('data/drawdown_{}.json'.format(symbol))
