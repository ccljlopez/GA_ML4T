"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'lchen427' # replace tb34 with your Georgia Tech username.

def compute_portvals(orders_file = "./orders/orders-10.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    order = pd.read_csv(orders_file,index_col = 'Date',parse_dates=True)
    order = order.sort_index()

    dates = pd.date_range(order.index[0],order.index[-1])
    stock_list = order['Symbol'].unique().tolist()

    order_new = pd.DataFrame(index = dates)

    stock_price = get_data(stock_list,dates)
    #print stock_price,delete later
    stock_price.fillna(method = 'ffill',inplace = True)
    stock_price.fillna(method = 'backfill', inplace = True)

    for stock in stock_list:
        df_tmp = order[order['Symbol']==stock]
    
        #df_tmp['Shares'][df_tmp['Order'] =='SELL'] = -1 * df_tmp['Shares'][df_tmp['Order'] =='SELL']
        #df_tmp.loc(df_tmp['Order'] =='SELL').ix[:,'Shares'] =  df_tmp.loc(df_tmp['Order'] =='SELL').ix[:,'Shares'] * (-1)
        df_tmp.loc[df_tmp.Order=='SELL','Shares'] = -1 * df_tmp.loc[df_tmp.Order=="SELL",'Shares']  
        #df_tmp.loc[df_tmp['Order']=='SELL','Shares'] * (-1)
        stock_share = stock + "_share"
        stock_commission = stock + '_commission'
        stock_impact = stock + "_impact"
        df_tmp = df_tmp.rename(columns = {'Shares':stock_share}) 
        df_tmp[stock_commission] = commission
        tmp = stock_price[stock]
        df_tmp = df_tmp.join(tmp,how = 'left')
        df_tmp[stock_impact] = impact * df_tmp[stock_share].abs() * df_tmp[stock]
        df_tmp.drop('Order',axis = 1,inplace = True)
        df_tmp.drop('Symbol', axis = 1, inplace = True) 
        df_tmp.drop(stock,axis = 1, inplace = True)
        df_tmp = df_tmp.groupby(df_tmp.index).sum()
        #print df_tmp
        order_new = order_new.join(df_tmp)
 
    #order_count = order['Symbol'].count() 
    
    order_new = order_new.fillna(value = 0)
    #print order_new[180:220] 
    #order_new = order_new.groupby(order_new.index).sum()
    #order_acc = order_new.cumsum(axis = 0)
    #stock_price = stock_price.fillna(value = 0)

    #print stock_price,delete later
 
    table_1 = stock_price.join(order_new)
    
    table_1["change"] = 0 
    for stock in stock_list:
        stock_share = stock + "_share"
        
        table_1["change"] = table_1["change"] - table_1[stock] * table_1[stock_share] #- table_1[stock] * impact * table_1[stock_share].abs()
        table_1.drop(stock,inplace = True,axis = 1)
    table_1.drop("SPY",axis = 1,inplace=True)
    table_1 = table_1.cumsum(axis = 0) 
    table_2 = stock_price.join(table_1)
    table_2.dropna(axis = 0)
   
    
    table_2["net"] = start_val + table_2["change"]
    for stock in stock_list:
        stock_share = stock + "_share"
        stock_commission = stock + '_commission'
        stock_impact = stock + '_impact'
        table_2["net"] = table_2["net"] + table_2[stock] * table_2[stock_share] - table_2[stock_commission] - table_2[stock_impact]
        


    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    # start_date = dt.datetime(2008,1,1)
    # end_date = dt.datetime(2008,6,1)
    # portvals = get_data(['IBM'], pd.date_range(start_date, end_date))
    portvals = table_2['net']  # remove SPY

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    #test_code()
    print compute_portvals()
