import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime as dt

def get_data(ind):
    ticker = {
        'ibov': '^BVSP',
        'sp500': '^GSPC'
    }
    start = {
        'ibov': dt.datetime(2000, 1, 1),
        'sp500': dt.datetime(1910, 1, 1)
    }
    #    yf.pdr_override() # <== that's all it takes :-)
    data = pdr.get_data_yahoo(ticker[ind],
        start[ind],
        dt.datetime.today())
    data = data.reset_index()
    data = data.rename(columns={'Date': 'd', 'Close': 'value'})
    data = data[['d', 'value']]
    #data = data.append({'d': '2020-03-16', 'value': 2386.13}, ignore_index=True)

    return data

def process_data(raw_data):
    data = raw_data.copy()
    ath = data['value'].max()
    data['cummax'] = data['value'].cummax()
    data['min'] = data.groupby('cummax')['value'].transform('min')
    data = data[::-1]
    data['cummin'] = data.groupby('cummax')['value'].agg('cummin')
    data = data[::-1]
    data = data[(data['cummin'] == data['min']) | (data['cummax'] == ath)].reset_index()
    data['ord_d'] = data.groupby('cummax').cumcount()
    data['delta'] = data.groupby('cummax')['value'].transform('first')
    data['d_first'] = data.groupby('cummax')['d'].transform('first')
    data['delta'] = data['value'] / data['delta'] - 1

    return data

def save_data(data, ind):
    date_str = dt.datetime.today().isoformat()[:10]
    data.to_json('data/{}_{}.json'.format(ind, date_str))

def plot_data(data):
    strs = {
        'ibov': {
            'title': 'Ibovespa: Atual queda comparada com suas maiores',
            'xlabel': '# de dias úteis desde a primeira queda\nDesde 2000\nAtualizado em {}\n\nTwitter @resendedaniel_',
        },
        'sp500': {
            'title': 'Current S&P 500 sell off against major ones',
            'xlabel': '# of trading days since first fall\nSince 1927\nUpdated at {}\n\nTwitter @resendedaniel_',
        }
    }



    max_days = data['ord_d'].max()
    color_max = '#E6550D'
    color_non_max = 'grey'
    ath = data['value'].max()

    fig, ax = plt.subplots(figsize=(10, 5))
    for x in data['cummax'].unique():
        sub = data[data['cummax'] == x]
        if sub['delta'].min() < -.02:
            plt.plot(sub['ord_d'], sub['delta'],
                color = color_max if x == ath else color_non_max,
                alpha = 1 if x == ath else (sub['delta'].min() * -1) ** .8)
            plt.scatter(sub['ord_d'].max(),
                        sub['delta'].values[-1],
                        color = color_max if x == ath else color_non_max,
                        alpha = 1 if x == ath else (sub['delta'].min() * -1) ** .8,
                        marker='.')
        if sub['delta'].min() < -.2 or x == ath:
            plt.text(sub['ord_d'].max(),
                     sub['delta'].values[-1],
                     ' {}: {:.1%} '.format(str(sub['d'].values[0])[:4], sub['delta'].values[-1]),
                     color = color_max if x == ath else color_non_max,
                     horizontalalignment='left' if str(sub['d'].values[0])[:4] in ['2018', '2004'] else 'right',
                     verticalalignment='center')

    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    plt.title(strs[ind]['title'], size=28)
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    now = (dt.datetime.today() - dt.timedelta(days=0)).strftime('%Y-%m-%d')
    plt.xlabel('{}'.format(strs[ind]['xlabel'].format(now)), horizontalalignment='right', x=1.0)

    my_dpi=300
    #plt.figure(figsize=(1200/my_dpi, 675/my_dpi), dpi=my_dpi)
    #plt.savefig('img.png', dpi=my_dpi)
    plt.show()


for ind in ['ibov', 'sp500']:
    print('Processing {}'.format(ind))
    data = get_data(ind)
    data = process_data(data)
    save_data(data, ind)
    plot_data(data)
