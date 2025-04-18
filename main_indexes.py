import feeder_yahoo
import process
import cache
import plot

symbol = '^GSPC'
data = feeder_yahoo.get_data(symbol)
print(data.tail())

crashes = process.crashes(data)
cache.save_crashes(crashes, symbol)
plot.crashes(crashes, symbol, save=True)

#    drawdown = process.drawdown(data)
#    cache.save_drawdown(drawdown, symbol)
#    plot.drawdown(drawdown, symbol)

recover = process.recover(data)
plot.recover(recover, symbol, save=True)
