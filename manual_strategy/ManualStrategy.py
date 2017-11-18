import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os
from util import get_data,plot_data
from marketsimcode import compute_portvals

class ManualStrategy(object):
    def __init__(self):
        print "Create a manual strategy object."

    def author(self):
        return 'lchen427'

    def testPolicy(self,symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        prices_all = get_data(symbols,dates)
        prices = prices_all[symbols]
        prices_SPY = prices_all[['SPY']]
        #print prices.ix[:9]
        dt_trades = pd.DataFrame(index=prices.index.copy())
        dt_trades['trading'] = 0
        dt_trades['holding'] = 0
        num = prices.shape[0]
        
        #calculate the indicator Price Channels
        prices_all_low = get_data(symbols,dates,colname = 'Low')
        prices_all_high = get_data(symbols,dates,colname = 'High')
        prices_low = prices_all_low[symbols]
        prices_high = prices_all_high[symbols]
        price_channel_high = prices_high.shift().rolling(20).max() #pd.rolling_max(prices_high.shift(), 20)
        price_channel_low = prices_low.shift().rolling(20).min() #pd.rolling_min(prices_low.shift(), 20)
        
        #calculate the indicator Price/SMA
        sma = prices.rolling(30).mean() #pd.rolling_mean(prices, 30)
        sma_index = prices/sma
        sma_spy = prices_SPY.rolling(30).mean()
        sma_index_spy = prices_SPY/sma_spy

        #calculate the indicator Bollinger Bands %
        bollinger_mean = prices.rolling(30).mean() #pd.rolling_mean(prices, 30)
        bollinger_std = prices.rolling(30).std() #pd.rolling_std(prices, 30)
        bollinger_up = bollinger_mean + 2 * bollinger_std
        bollinger_bottom = bollinger_mean - 2 * bollinger_std
        bollinger = (prices - bollinger_bottom) / (bollinger_up - bollinger_bottom)
      
        # implement the manual strategy here
        dt_trades = pd.DataFrame(index=prices.index.copy())
        dt_trades['holding'] = 0
        dt_trades['trading'] = 0
        #dt_trades['operating'] = 0
        for day in range (30, num):
            dt_trades.ix[day,'holding'] = dt_trades.ix[day-1,'holding']
            #overbought
            if (bollinger.ix[day,symbol] > 1) and (sma_index.ix[day,symbol] > 1.05) and (prices.ix[day,symbol] > 0.95 * price_channel_high.ix[day,symbol]) and (sma_index_spy.ix[day,'SPY'] <= 1.05):
                if dt_trades.ix[day,'holding'] != -1000:
                    dt_trades.ix[day,'holding'] = -1000
                    dt_trades.ix[day,'trading'] = dt_trades.ix[day,'holding'] - dt_trades.ix[day-1,'holding']
                    dt_trades.ix[day,'operating'] = 1
            #oversold
            elif (bollinger.ix[day,symbol] < 0) and (sma_index.ix[day,symbol] < 0.95) and (prices.ix[day,symbol] <  price_channel_low.ix[day,symbol]) and (sma_index_spy.ix[day,'SPY'] >= 0.95):
                if dt_trades.ix[day,'holding'] != 1000:
                    dt_trades.ix[day,'holding'] = 1000
                    dt_trades.ix[day,'trading'] = dt_trades.ix[day,'holding'] - dt_trades.ix[day-1,'holding'] 
                    dt_trades.ix[day,'operating'] = 2
            #Close long position when Price/SMA cross 1 upward
            elif (sma_index.ix[day,symbol] > 1) and (sma_index.ix[day-1,symbol] <= 1):
                if dt_trades.ix[day,'holding'] == 1000:
                    dt_trades.ix[day,'holding'] = 0
                    dt_trades.ix[day,'trading'] = dt_trades.ix[day,'holding'] - dt_trades.ix[day-1,'holding']
                    dt_trades.ix[day,'operating'] = 3
            #close short position when Price/SMA cross 1 downward
            elif (sma_index.ix[day,symbol] < 1) and (sma_index.ix[day-1,symbol] >= 1):
                if dt_trades.ix[day,'holding'] == -1000:
                    dt_trades.ix[day,'holding'] = 0
                    dt_trades.ix[day,'trading'] = dt_trades.ix[day,'holding'] - dt_trades.ix[day-1,'holding']
                    dt_trades.ix[day,'operating'] = 4
        #for day in range(num):
            #print dt_trades.ix[day,'trading'], dt_trades.ix[day,'holding'], dt_trades.ix[day,'operating']   
        return pd.Series.to_frame(dt_trades['trading'])      



if __name__ == "__main__":
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    commission = 9.95
    impact = 0.005
    start_val = 100000
    dates = pd.date_range(sd, ed)
    symbol = "JPM"
    symbols = []
    symbols.append(symbol)
    prices_all = get_data(symbols,dates)
    prices = prices_all[symbols]
    ms = ManualStrategy()
    dt_trades = ms.testPolicy(sd = sd, ed = ed)
    bench_trade = dt_trades.copy()
    dt_trades = dt_trades[(dt_trades.T != 0).any()] # remove no trading days
    #print dt_trades
    #bench_trade = dt_trades.copy()
    bench_trade['trading'] = 0
    bench_trade['trading'].ix[0] = 1000
    bench_trade = bench_trade[(bench_trade.T != 0).any()] # remove no trading days
    #calculate position
    trade_position = dt_trades.copy()
    trade_position = trade_position.cumsum(axis=0)
    trade_position = trade_position.rename(columns = {'trading':'position'})
  
    portvals = compute_portvals(dt_trades, prices, symbols, start_val, commission, impact)
    bench_mark = compute_portvals(bench_trade, prices, symbols, start_val, commission, impact)
    cr_m = portvals['net'].ix[-1] / start_val - 1
    cr_b = bench_mark['net'].ix[-1] / start_val - 1
    dr_m = portvals['net']/portvals['net'].shift(1) -1
    dr_b = bench_mark['net']/bench_mark['net'].shift() -1
    adr_m = dr_m.mean()
    adr_b = dr_b.mean()
    sddr_m = dr_m.std()
    sddr_b = dr_b.std()
    #report the metrics
    print [cr_m,adr_m,sddr_m],[cr_b,adr_b,sddr_b]
    #normalize the portfoli performance
    portvals = portvals['net']/portvals['net'][0]
    bench_mark = bench_mark['net']/bench_mark['net'][0]
    fig,ax = plt.subplots()
    ax.plot(portvals, label="manual strategy portfolio",color='black')
    ax.plot(bench_mark, label='benchmark', color='blue')
    dt_trades = dt_trades.join(trade_position)
    dt_trade_long = dt_trades[dt_trades['trading'] > 0]
    dt_trade_long = dt_trade_long[dt_trade_long['position']==1000]
    dt_long = dt_trade_long.index.to_datetime()
    dt_trade_short = dt_trades[dt_trades['trading'] < 0]
    dt_trade_short = dt_trade_short[dt_trade_short['position']==-1000]
    dt_short = dt_trade_short.index.to_datetime()
    ymin, ymax = ax.get_ylim()
    for xc in dt_long:
        ax.vlines(x=xc,ymax = ymax, ymin = ymin, color='green')
    for xc in dt_short:
        ax.vlines(x= xc,ymin = ymin, ymax = ymax, color='red')
    ax.set_xlabel("date")
    ax.set_ylabel("value")
    green_line = mlines.Line2D([], [], color='green', marker='|', label='long')
    plt.legend(handles=[green_line])
    ax.set_title("Performance of benchmark and manual portfolio")
    legend = ax.legend(loc='upper left',fontsize = 'small')
    plt.show()
