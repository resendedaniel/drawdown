import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
#import fix_yahoo_finance as yf
import datetime as dt

def get_data(ind):
    if ind == 'ibov':
        return get_ibov()
    elif ind == 'sp500':
        return get_sp500()
    elif ind == 'dowjones':
        return get_dowjones()

def get_ibov():
    url = 'https://assets-comparacaodefundos.s3-sa-east-1.amazonaws.com/cvm/ibovespa'
    data = pd.read_json(url)
    data = data.rename(columns={'c': 'value'})
    data = data.append({'d': 20200316, 'value': 71168.0}, ignore_index=True)
    data['d'] = pd.to_datetime(data['d'], format='%Y%m%d')
    data = data.sort_values('d')

    return data

def get_sp500():
    #    yf.pdr_override() # <== that's all it takes :-)
    data = pdr.get_data_yahoo('^GSPC',
        dt.datetime(1970, 1, 1),
        dt.datetime.today())
    data = data.reset_index()
    data = data.rename(columns={'Date': 'd', 'Close': 'value'})
    data = data[['d', 'value']]
    #data = data.append({'d': '2020-03-16', 'value': 2386.13}, ignore_index=True)

    return data

def get_dowjones():
    file = 'data/dowjones_daily.csv'
    data = pd.read_csv(file, skiprows=9)
    data = data.rename(columns={'Date': 'd', 'Closing Value': 'value'})

    return data


ind = 'dowjones'
data = get_data(ind)
print(data.tail())

strs = {
    'ibov': {
        'title': 'Ibovespa: Atual queda comparada com suas maiores',
        'xlabel': '# de dias úteis desde a primeira queda\nDesde 2000\nAtualizado em {}\n\nTwitter @resendedaniel_',
    },
    'sp500': {
        'title': 'Current S&P 500 sell off against major ones',
        'xlabel': '# of trading days since first fall\nSince 1970\nUpdated at {}\n\nTwitter @resendedaniel_',
    },
    'dowjones': {
        'title': 'Current Dow Jones sell off against major ones',
        'xlabel': '# of trading days since first fall\nSince 1914\nUpdated at {}\n\nTwitter @resendedaniel_',
    }
}

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


max_days = data['ord_d'].max()
color_max = '#E6550D'
color_non_max = 'grey'

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
now = (dt.datetime.today() - dt.timedelta(days=1)).strftime('%Y-%m-%d')
plt.xlabel('{}'.format(strs[ind]['xlabel'].format(now)), horizontalalignment='right', x=1.0)

my_dpi=300
#plt.figure(figsize=(1200/my_dpi, 675/my_dpi), dpi=my_dpi)
#plt.savefig('img.png', dpi=my_dpi)
plt.show()
