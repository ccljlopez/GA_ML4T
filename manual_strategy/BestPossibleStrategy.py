import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import os
from util import get_data,plot_data
from marketsimcode import compute_portvals

class BestPossibleStrategy(object):
    def __init__(self, commission = 0.0, impact = 0.0):
        self.commission = commission
        self.impact = impact

    def author(self):
        return 'lchen427'

    def testPolicy(self,symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        prices_all = get_data(symbols,dates)
        prices = prices_all[symbol] 
        dt_trades = pd.DataFrame(index=prices.index.copy()) 
        dt_trades['trading'] = 0
        dt_trades['holding'] = 0
        num = prices.shape[0]
        
        #set the trade action for the first day
        if prices.ix[0] < prices.ix[1]:
            dt_trades['trading'].ix[0] = 1000
            dt_trades['holding'].ix[0] = 1000
        elif prices.ix[0] == prices.ix[1]:
            dt_trades['trading'].ix[0] = 0
            dt_trades['holding'].ix[0] = 0
        else:
            dt_trades['trading'].ix[0] = -1000
            dt_trades['holding'].ix[0] = -1000

        #set the trade action for the remaining days
        for i in range (1, num - 1):
            if (prices.ix[i] >  prices.ix[i+1]):
                dt_trades['holding'].ix[i] = -1000
                dt_trades['trading'].ix[i] = dt_trades['holding'].ix[i] - dt_trades['holding'].ix[i-1]
            elif (prices.ix[i] <  prices.ix[i+1]):
                dt_trades['holding'].ix[i] = 1000
                dt_trades['trading'].ix[i] = dt_trades['holding'].ix[i] - dt_trades['holding'].ix[i-1]
            else:
                dt_trades['holding'].ix[i] = dt_trades['holding'].ix[i-1]
                dt_trades['trading'].ix[i] = 0

        #set the trade action for the last day
        dt_trades['trading'].ix[num-1] = 0
        dt_trades['holding'].ix[num-1] = dt_trades['holding'].ix[num-2]                
     
        return pd.Series.to_frame(dt_trades['trading'])

if __name__ == "__main__":
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    commission = 0
    impact = 0 
    start_val = 100000
    dates = pd.date_range(sd, ed)
    symbol = "JPM"
    symbols = []
    symbols.append(symbol)
    prices_all = get_data(symbols,dates)
    prices = pd.Series.to_frame(prices_all[symbol])
    #print "prices\n", prices
    bps = BestPossibleStrategy()
    dt_trades = bps.testPolicy()
    bench_trade = dt_trades.copy()
    bench_trade['trading'] = 0
    bench_trade['trading'].ix[0] = 1000
    #print "dt_trades\n",dt_trades
    portvals = compute_portvals(dt_trades, prices, symbols, start_val, commission, impact)
    bench_mark = compute_portvals(bench_trade, prices, symbols, start_val, commission, impact)
    cr_p = portvals['net'].ix[-1] / portvals['net'].ix[0] - 1
    cr_b = bench_mark['net'].ix[-1] / bench_mark['net'].ix[0] - 1
    dr_p = portvals['net']/portvals['net'].shift(1) -1
    dr_b = bench_mark['net']/bench_mark['net'].shift() -1
    adr_p = dr_p.mean()
    adr_b = dr_b.mean()
    sddr_p = dr_p.std()
    sddr_b = dr_b.std()
    #report the metrics
    print [cr_p,adr_p,sddr_p],[cr_b,adr_b,sddr_b]
    #normalize the portfoli performance
    portvals = portvals['net']/portvals['net'][0]
    bench_mark = bench_mark['net']/bench_mark['net'][0]
    fig,ax = plt.subplots()
    ax.plot(portvals, label="best possible portfolio",color='black')
    ax.plot(bench_mark, label='benchmark', color='blue')
    ax.set_xlabel("date")
    ax.set_ylabel("value")
    ax.set_title("Performance of benchmark and best possible portfolio")
    legend = ax.legend(loc='upper left',fontsize = 'small')
    plt.show()


