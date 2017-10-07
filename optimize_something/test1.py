import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def error(line,data):
    err = np.sum((data[:,1]- (line[0] * data[:,0] + line[1])) ** 2)
    return err

def test_run():
    l_orig = np.float32([4,2])
    print "Original line: C0 = {}, C1 = {}".format(l_orig[0],l_orig[1])
    Xorig = np.linspace(0,10,21)
    Yorig = Xorig*l_orig[0] + l_orig[1]
    noise_sigma = 3.0
    noise = np.random.normal(0,noise_sigma,Yorig.shape)
    data = np.asarray([Xorig,Yorig + noise])
    l_fit = fit_line(data,error)
    print "Fitted line C0={},C1 = {}".format(l_fit[0],l_fit[1])

def fit_line(data,err_func):
    l = np.float32([0,np.mean(data[:,1])])
    result = spo.minimize(err_func,l,args=(data,),method='SLSQP',options={'disp':True})
    return result.x
if __name__ == "__main__":
    test_run()
