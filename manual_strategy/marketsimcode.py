"""MC2-P2: Manual Strategy"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'lchen427' # replace tb34 with your Georgia Tech username.

def compute_portvals(order_file,prices,stocks, start_val = 1000000, commission=9.95, impact=0.005):
    #order = pd.read_csv(orders_file,index_col = 'Date',parse_dates=True)
    #order = order.sort_index()
    order = order_file
    #dates = pd.date_range(order.index[0],order.index[-1])
    symbol = stocks[0]
    order_new = pd.DataFrame(index = prices.index.copy())
    stock_price = prices
    stock_price.fillna(method = 'ffill',inplace = True)
    stock_price.fillna(method = 'backfill', inplace = True)

   
    df_tmp = order_file
    
    #pd.Series.to_frame(df_tmp)
    #print "order\n", df_tmp 
    stock_share = symbol + "_share"
    stock_commission = symbol + '_commission'
    stock_impact = symbol + "_impact"
    df_tmp[stock_commission] = commission
    df_tmp = df_tmp.rename(columns = {'trading':stock_share}) 
    df_tmp[stock_commission] = commission
    df_tmp = df_tmp.join(prices,how='left')
    #print df_tmp
    df_tmp[stock_impact] = impact * df_tmp[stock_share].abs() * df_tmp[symbol]
        #df_tmp.drop('Order',axis = 1,inplace = True)
        #df_tmp.drop('Symbol', axis = 1, inplace = True) 
        #df_tmp.drop(stock,axis = 1, inplace = True)
    table_1 = df_tmp.groupby(df_tmp.index).sum()
    #print table_1
    table_1 = table_1.fillna(value = 0)
    #print order_new[180:220] 
    #order_new = order_new.groupby(order_new.index).sum()
    #order_acc = order_new.cumsum(axis = 0)
    #stock_price = stock_price.fillna(value = 0)

    #print stock_price,delete later
 
    #table_1 = stock_price.join(order_new)
    
    table_1["change"] = 0 
    for stock in stocks:
        stock_share = stock + "_share"
        
        table_1["change"] = table_1["change"] - table_1[stock] * table_1[stock_share]
        table_1.drop(stock,inplace = True,axis = 1)
        table_1 = stock_price.join(table_1, how = 'left')
        table_1 = table_1.fillna(value = 0)
        table_1.drop(stock,inplace = True,axis = 1)
    #print table_1
    #table_1.drop("SPY",axis = 1,inplace=True)
    table_1 = table_1.cumsum(axis = 0) 
    table_2 = stock_price.join(table_1,how = 'left')
    table_2 = table_2.fillna(value = 0)
    #print table_2
    table_2.dropna(axis = 0)
    #table_2 = table_1.copy()
    #print table_2.ix[:9]
    
    table_2["net"] = start_val + table_2["change"]
    for stock in stocks:
        stock_share = stock + "_share"
        stock_commission = stock + '_commission'
        stock_impact = stock + '_impact'
        table_2["net"] = table_2["net"] + table_2[stock] * table_2[stock_share] - table_2[stock_commission] - table_2[stock_impact]

#############################
    #print table_2

############################
    portvals = table_2['net']  # remove SPY
 
    return pd.Series.to_frame(portvals)


