import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
#matplotlib.use('Agg')
from util import get_data

def test_run():
    #Read data
    dates = pd.date_range('2010-10-1','2010-12-5')
    #symbols = ['SPY','XOM','GOOG','GLD']
    symbols = ['SPY']
    df = get_data(symbols,dates)
    #rm_SPY = pd.rolling_mean(df,window = 20)
    #print df
    ax = df['SPY'].plot(title='SPY rolling mean', label = 'SPY')
    #rm_SPY.plot(label = "rolling mean",ax=ax)
    #ax.set_xlabel("Date")
    #ax.set_ylabel("Price")
    #ax.legend(loc='upper left')
    daily_return = compute_daily_return(df)
    #print daily_return
    cumulative_return = compute_cumulative_return(df)
    #print cumulative_return
    #cumulative_return.plot()
    #plt.show()
    rm_SPY = get_rolling_mean(df['SPY'],window = 20) 
    rm_SPY.plot(label = "rolling mean",ax=ax)  
    rstd_SPY = get_rolling_std(df['SPY'],window = 20)
    upper_band,lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)
    upper_band.plot(label='upper band',ax = ax)
    lower_band.plot(label = 'lower band', ax = ax)
    plt.show()

def compute_daily_return(df):
    #daily_returns = df.copy()
    daily_returns = (df/df.shift(1)) - 1
    daily_returns.ix[0,:] = 0
    return daily_returns

def compute_cumulative_return(df):
    print "start",df.values[0,:],"end"
    cumulative_returns = df/df.values[0,:]
  
def get_rolling_mean(values, window):
    return pd.rolling_mean(values,window)

def get_rolling_std(values,window):
    return pd.rolling_std(values,window)

def get_bollinger_bands(rm,rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2 
    return upper_band, lower_band 

if __name__ == '__main__':
    test_run()
