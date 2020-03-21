import numpy as np


def crashes(raw_data):
    data = raw_data[['d', 'value']].copy()
    data = data.reset_index(drop=True)
    ath = data['value'].max()
    data['cummax'] = data['value'].cummax()
    data['min'] = data.groupby('cummax')['value'].transform('min')
    data = data[::-1]
    data['cummin'] = data.groupby('cummax')['value'].agg('cummin')
    data = data[::-1]
    data = data[(data['cummin'] == data['min']) | (data['cummax'] == ath)]
    data = data.reset_index(drop=True)
    data['ord_d'] = data.groupby('cummax').cumcount()
    data['delta'] = data.groupby('cummax')['value'].transform('first')
    data['d_first'] = data.groupby('cummax')['d'].transform('first')
    data['delta'] = data['value'] / data['delta'] - 1

    data = data[['ord_d', 'd', 'value', 'delta', 'cummax']]

    return data


def drawdown(raw_data):
    data = raw_data[['d', 'value']].copy()
    data['factor'] = data['value'].diff().fillna(0)
    data['factor'] = data['value'] / (data['value'] - data['factor'])

    drawdown = []
    current_drawdown = 1
    for i in np.arange(len(data['factor'])):
        current_drawdown = min(current_drawdown * data['factor'][i], 1)
        drawdown.append(current_drawdown)
    data['drawdown'] = drawdown

    return data
