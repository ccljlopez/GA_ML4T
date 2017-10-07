"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)

    X = np.random.random(size = (500,50))
    Y = np.zeros(500)
    factor = np.zeros(50)
    for i in range(50):
        factor[i] = i * 2
    for j in range(500):
        for h in range(50):
            Y[j]= Y[j] + factor[h]* X[j,h]
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    # Y = X[:,0] + np.sin(X[:,1]) + X[:,2]**2 + X[:,3]**3
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    X = np.random.random(size = (300,3))*10
    Y = np.zeros(300)
    for i in range(300):
        tmp = X[i].mean()
        if tmp >= 20:
            Y[i] = 20
        elif tmp< 20 and tmp >15:
            Y[i] = 15
        elif tmp <=15 and tmp > 10:
            Y[i] = 10
        else:
            Y[i] = 5
        
    return X, Y

def author():
    return 'lchen427' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
