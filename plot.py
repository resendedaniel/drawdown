import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import seaborn as sns

def crashes(data, symbol, save=False):
    strs = {
        '^BVSP': {
            'title': 'Ibovespa: Atual queda comparada com suas maiores',
            'xlabel': '  # de dias úteis desde a primeira queda\nDesde 1996\nAtualizado em {}\n\nTwitter @resende451',
            'id': 'ibov'
        },
        '^GSPC': {
            'title': 'Current S&P 500 sell off against major ones',
            'xlabel': '  # of trading days since first fall\nSince 1927\nUpdated at {}\n\nTwitter @resende451',
            'id': 'sp500'
        }
    }

    color_max = '#E6550D'
    color_non_max = 'grey'
    ath = data['value'].max()

    fig, ax = plt.subplots(figsize=(10.8*16/9, 10.8))
    for x in data['cummax'].unique():
        sub = data[data['cummax'] == x]
        if sub['delta'].min() < -.02:
            plt.plot(sub['ord_d'], sub['delta'],
                     color=color_max if x == ath else color_non_max,
                     alpha=1 if x == ath else (sub['delta'].min() * -1) ** .8)
            plt.scatter(sub['ord_d'].max(),
                        sub['delta'].values[-1],
                        color=color_max if x == ath else color_non_max,
                        alpha=1 if x == ath else (sub['delta'].min() * -1) ** .8,
                        marker='.')
        if sub['delta'].min() < -.2 or x == ath:
            plt.text(sub['ord_d'].max(),
                     sub['delta'].values[-1],
                     ' {}: {:.1%} '.format(str(sub['d'].values[0])[:4], sub['delta'].values[-1]),
                     color=color_max if x == ath else color_non_max,
                     horizontalalignment='left' if str(sub['d'].values[0])[:4] in [
                '2018', '2004', '1987', '2020'] else 'right',
                verticalalignment='center')

    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    plt.title(strs[symbol]['title'], size=28)
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    now = (dt.datetime.today() - dt.timedelta(days=0)).strftime('%Y-%m-%d')
    plt.xlabel('{}'.format(strs[symbol]['xlabel'].format(now)), horizontalalignment='right', x=1.0)

    if save:
        plt.savefig('img/crash_{}.png'.format(strs[symbol]['id']), dpi=100)
    else:
        plt.show()


def drawdown(data, symbol):
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(data['d'], data['drawdown'])
    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    plt.title('{} Drawdown'.format(symbol))
    plt.show()


def recover(data, symbol, save=False):
    strs = {
        '^BVSP': {
            'title': 'Comportamento do Ibovespa nos auges das quedas',
            'xlabel': '# pregões desde o mínimo\nDesde 2000\nAtualizado em {}\n\nTwitter @resende451',
            'ylabel': 'Variação sobre o valor do menor fechamento',
            'id': 'ibov'
        },
        '^GSPC': {
            'title': 'S&P 500 Behavior around bottoms',
            'xlabel': '# of trading days since minimal\nSince 1927\nUpdated at {}\n\nTwitter @resende451',
            'ylabel': 'Variation over minimum close value',
            'id': 'sp500'
        }
    }
    color_max = '#E6550D'
    color_non_max = 'grey'
    ath = data['value'].max()

    fig, ax = plt.subplots(figsize=(10.8, 10.8))
    for x in data['cummax'].unique():
        sub = data[data['cummax'] == x]
        sub_d = sub['ord_d'].max()
        sub = sub[sub['ord_d'] >= -100]
        sub = sub[sub['ord_d'] <= 100]
        if sub['min'].min() < .98:
            plt.plot(sub['ord_d'], sub['cumdelta'],
                     color=color_max if x == ath else color_non_max,
                     alpha=1 if x == ath else (1 - sub['min'].min()) ** .8)
            plt.scatter(sub['ord_d'].max(),
                        sub['cumdelta'].values[-1],
                        color=color_max if x == ath else color_non_max,
                        alpha=1 if x == ath else (1 - sub['min'].min()) ** .8,
                        marker='.')
        if sub['min'].min() < .8 or x == ath:
            plt.text(sub['ord_d'].max(),
                     sub['cumdelta'].values[-1],
                     ' {}'.format(str(sub['d'].values[0])[:4], sub_d),
                     color=color_max if x == ath else color_non_max,
                     horizontalalignment='right' if str(sub['d'].values[0])[:4] in [
                '2018'] else 'left',
                verticalalignment='center')

    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    plt.title(strs[symbol]['title'], size=28)
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    now = (dt.datetime.today() - dt.timedelta(days=0)).strftime('%Y-%m-%d')
    plt.xlabel('{}'.format(strs[symbol]['xlabel'].format(now)),
               horizontalalignment='right', x=1.0)
    plt.ylabel('{}'.format(strs[symbol]['ylabel'].format(now)))

    if save:
        plt.savefig('img/recovery_{}.png'.format(strs[symbol]['id']), dpi=100)
    else:
        plt.show()


def crash_2020_trajectories(data):
    fall_values = data.groupby('symbol').last().reset_index()
    fall_values = fall_values.sort_values('cumdelta')
    n = min(16, int(fall_values.shape[0]/2))
    top_symbols = fall_values['symbol'].values[:n]
    bottom_symbols = fall_values['symbol'].values[-n:]
    colors = sns.color_palette("RdBu", n_colors=fall_values.shape[0]).as_hex()
    #colors = colors[:n] + colors[-n:]

    top_domain = np.mean(fall_values['cumdelta'].values[:n]) + np.array([.06, -.06])
    top_range = list(np.linspace(top_domain[0], top_domain[1], n))

    bottom_domain = np.mean(fall_values['cumdelta'].values[-n:]) + np.array([.06, -.06])
    bottom_range = list(np.linspace(bottom_domain[0], bottom_domain[1], n))

    fig, ax = plt.subplots(figsize=(10, 5))
    texts = []
    for symbol in fall_values['symbol']:
        equity_data = data[data['symbol'] == symbol]
        color = colors.pop(0)
        alpha = .66 if symbol in top_symbols or symbol in bottom_symbols else .2
        plt.plot(equity_data['d'],
                 equity_data['cumdelta'],
                 c=color,
                 linewidth=1.0,
                 alpha=alpha)

        if symbol in top_symbols:
            plt.text(equity_data['d'].values[-1],
                     top_range.pop(),
                     '{} {:.1%}'.format(symbol, equity_data['cumdelta'].values[-1]),
                     c=color)
        if symbol in bottom_symbols:
            plt.text(equity_data['d'].values[-1],
                     bottom_range.pop(),
                     '{} {:.1%}'.format(symbol, equity_data['cumdelta'].values[-1]),
                     c=color)

    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    plt.title('Quedas do crash de 2020')
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])

    plt.show()
