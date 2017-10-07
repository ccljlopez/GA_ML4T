"""
A simple wrapper for decision tree.  (c) 2017 Li Chen
"""

import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size =leaf_size
        self.tree = np.array([])

    def author(self):
        return 'lchen427' # replace tb34 with your Georgia Tech username

    def buildTree(self,dataX,dataY):
        #print dataX.shape,dataY.shape,"init-in learner"
        #f_dict = {} # dictionary to store feature corrcoef
        if dataX.shape[0] <= self.leaf_size:
            #self.tree = np.append(self.tree, [[-1,dataY.mean(),-1,-1]],axis=0)
            #print "xxxxxxxxxx",np.array([[-1,dataY.mean(),-1,-1]])
            return np.array([[-1,dataY.mean(),-1,-1]])
        elif (np.count_nonzero(dataY == dataY[0]) == len(dataY)) and (dataX.shape[0] > self.leaf_size):
            return np.array([[-1,dataY[0],-1,-1]])
        else:
            max_feature_index = dataX.shape[1]
            i = np.random.randint(max_feature_index) #determine the best feature i to split on
            # print "feature", i, f_dict[i]
            splitVal = np.median(dataX[:,i])
            split_index_left = dataX[:,i] <= splitVal
            split_index_right = dataX[:,i] > splitVal
            if (np.count_nonzero(split_index_left==False)==len(split_index_left)) or (np.count_nonzero(split_index_right==False)==len(split_index_right)):
                return  np.array([[-1,dataY.mean(),-1,-1]])
            #print "left",  dataX[dataX[:,i] <= splitVal],dataX[dataX[:,i] <= splitVal].shape[0]
            #print "right", dataX[dataX[:,i] > splitVal]
            lefttree = self.buildTree(dataX[dataX[:,i] <= splitVal],dataY[dataX[:,i] <= splitVal])
            #print lefttree,"left tree"
            righttree = self.buildTree(dataX[dataX[:,i] > splitVal],dataY[dataX[:,i] > splitVal])
            root = np.array([[int(i),splitVal,1, lefttree.shape[0] + 1]])
            tmp = np.append(root,lefttree, axis = 0)
            return  np.append(tmp, righttree, axis = 0)

    def addEvidence(self,dataX,dataY):
        self.tree = self.buildTree(dataX,dataY)
        #print "self.tree",self.tree
 
    def query(self,Xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        Ytest = np.array([])
        for row in Xtest:
            loop = True
            j = 0
            while loop:
                factor = int(self.tree[j][0])
                splitVal = self.tree[j][1]
                if factor == -1:
                    loop = False
                    Ytest = np.append(Ytest,splitVal)
                else:
                    if row[factor] <= splitVal:
                        j = int(j + self.tree[j][2])
                    else:
                        j = int(j + self.tree[j][3])
        return Ytest    
        #return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
