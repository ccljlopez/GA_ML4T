"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality

def min_volatility(allocs,data):
    #data equals normalized prices
    alloced_prices = allocs * data
    port_vals = alloced_prices * 1000000
    port_val = port_vals.sum(axis=1)

    #calculate daily return 
    dr = port_val/port_val.shift(1) -1
    sddr = dr.std()
    return sddr 

def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later


    # Get daily portfolio value
    normed_prices = prices/prices.ix[0]
    # Normalized SPY
    prices_SPY = prices_SPY/prices_SPY[0]

    alloced_prices = normed_prices * allocs
    port_vals = alloced_prices * sv
    port_val = port_vals.sum(axis=1) # add code here to compute daily portfolio values

    # Get portfolio statistics (note: std_daily_ret = volatility)
    # Get portfolio statistics (note: std_daily_ret = volatility)
    
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    # daily return
    dr = port_val/port_val.shift(1) - 1
    #dr.ix[0] = 0
    #average daily return mean and standard deviation
    adr = dr.mean()
    sddr = dr.std()
    #cumulative return
    cr = port_val[-1]/port_val[0] -1
    #calculate sharp ration
    sr = np.sqrt(sf)*(adr - rfr)/sddr
    return cr, adr, sddr, sr


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):
    
    num_syms = len(syms)
    allocs = np.zeros(num_syms)
    allocs[-1] = 1.0
    
    
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    normalized_prices = prices/prices.ix[0]
    prices_SPY = prices_SPY/prices_SPY[0]
    data = normalized_prices
    bnds = tuple((0, 1) for x in range(num_syms))
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    result = spo.minimize(min_volatility,allocs,args=(data,),constraints=cons,bounds=bnds,method='SLSQP',options={'disp':True})
    allocs = result.x
    cr, adr, sddr, sr = assess_portfolio(sd,ed,syms,allocs,1000000,0.0,252.0,False)
    
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    #  allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
