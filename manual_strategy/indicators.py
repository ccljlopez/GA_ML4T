"""MC2-P2: Manual Strategy"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'lchen427'

def price_channel(prices, prices_low, prices_high, window):
    price_channel_high = pd.rolling_max(prices_high.shift(), window)
    price_channel_low = pd.rolling_min(prices_low.shift(), window)
    price_channel_mid = (price_channel_high + price_channel_low)/2
    price_channel = (prices - price_channel_low) / (price_channel_high - price_channel_low)
    fig,ax = plt.subplots() 
    ax.plot(price_channel_low,label="Low",color = "#3498DB") #color blue
    ax.plot(price_channel_high,label="High",color = "#3498DB") #color blue
    ax.plot(prices,label="Stock Price",color = "#7F8C8D") #color grey
    ax.set_title("Price Channels")
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    legend = ax.legend(loc='upper right',fontsize = 'small')
    plt.show()

def sma(prices, window):
    sma = prices.copy()
    #clear out the dataframe so that we cn assign value to it
    sma[:] = 0
    prices = prices/prices.ix[0]
    sma = pd.rolling_mean(prices,window)
    sma_index = prices/sma
    fig,ax = plt.subplots()
    ax.plot(prices,label="Price",color = "#7F8C8D") #color blue
    ax.plot(sma_index,label="Price/SMA",color = "#3498DB") #color blue
    ax.plot(sma,label="SMA",color = "#E67E22") #color orange
    ax.set_title("Price/SMA")
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    legend = ax.legend(loc='upper right',fontsize = 'small')
    plt.show()

def bollinger(prices, window):
    prices = prices/prices.ix[0]
    bollinger = prices.copy()
    bollinger[:] = 0
    bollinger_mean = pd.rolling_mean(prices,window)
    bollinger_std = pd.rolling_std(prices,window)
    bollinger_up = bollinger_mean + 2 * bollinger_std
    bollinger_bottom = bollinger_mean - 2 * bollinger_std
    bollinger = (prices - bollinger_bottom) / (bollinger_up - bollinger_bottom)
    fig,ax = plt.subplots()
    ax.plot(bollinger_up,label="Upper band",color = "#E67E22") #color orange
    ax.plot(bollinger,label="Bollinger %",color = "#3498DB") #color blue
    ax.plot(bollinger_bottom,label="Lower band",color = "#E67E22") #color orange
    ax.plot(bollinger_mean,label="SMA", color = "#7F8C8D")
    ax.set_title("Bollinger Bands")
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    legend = ax.legend(loc='upper right',fontsize = 'small')
    plt.show()
  
  
if __name__ == "__main__":
    stock_list = ['JPM']
    start_date = dt.datetime(2008,1,1)
    #end_date = dt.datetime(2008,1,14)
    end_date = dt.datetime(2009,12,31)
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(stock_list,dates)
    prices = prices_all[stock_list]
    prices_all_low = get_data(stock_list,dates,colname = 'Low')
    prices_all_high = get_data(stock_list,dates,colname = 'High')
    prices_low = prices_all_low[stock_list]
    prices_high = prices_all_high[stock_list]

    window_1 = 20
    price_channel(prices,prices_low, prices_high, window_1)
    window = 30
    sma(prices,window)
    bollinger(prices,window_1)
