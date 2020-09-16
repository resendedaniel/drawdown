import feeder_yahoo
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn.linear_model import LinearRegression
import numpy as np


symbol = 'itub4.sa'
days = 3
data = feeder_yahoo.get_data(symbol)
data = feeder_yahoo.process_data(data)

data['mon'] = data['d'].dt.strftime('%Y-%m')

results = []
for mon in data['mon'].unique():
    subset = data[data['mon'] == mon]
    i = subset.index[-1]
    prev = data.loc[i-(days-1):i+1, 'delta'].prod()-1
    post = data.loc[i+1:i+days, 'delta'].prod()-1
    results.append({
        'mon': mon,
        'prev': prev,
        'post': post,
    })

results = pd.DataFrame(results)

model = LinearRegression()
model.fit(results['prev'].values.reshape((-1,1)), np.array(results['post'].values))
x_new = np.linspace(results['prev'].min(), results['prev'].max(), 100)
y_new = model.predict(x_new[:, np.newaxis])

fig, ax = plt.subplots(1)
ax.scatter(results['prev'], results['post'], s=1.5)
ax.plot(x_new, y_new)
ax.axvline(x=0, lw=.5, color='k')
ax.axhline(y=0, lw=.5, color='k')
ax.set_ylabel('Retorno após')
ax.set_xlabel('Retorno antes')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.title('{} for {} days'.format(symbol.replace('.SA', ''), days))
plt.show()
