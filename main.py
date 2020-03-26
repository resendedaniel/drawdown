import feeder_yahoo
import process
import cache
import plot

symbols = ['^BVSP', '^GSPC']
for symbol in symbols:
    data = feeder_yahoo.get_data(symbol)
    print(data.tail())

    crashes = process.crashes(data)
    cache.save_crashes(crashes, symbol)
    plot.crashes(crashes, symbol)

#    drawdown = process.drawdown(data)
#    cache.save_drawdown(drawdown, symbol)
#    plot.drawdown(drawdown, symbol)

    recover = process.recover(data)
    plot.recover(recover, symbol)
