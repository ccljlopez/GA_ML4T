"""
A simple wrapper for decision tree.  (c) 2017 Li Chen
"""

import numpy as np
import DTLearner as dt
import LinRegLearner as lrl
import RTLearner as rt
import BagLearner as bg
class BagLearner(object):

    def __init__(self,learner = dt.DTLearner, kwargs = {},bags = 20, boost = False,verbose = False):
        self.bags = bags
        if ((learner == dt.DTLearner) or (learner ==rt.RTLearner)) and ('leaf_size'in kwargs):
            self.leaf_size = kwargs['leaf_size']
        else:
            self.leaf_size = 1
        self.learners = []
        if learner == dt.DTLearner:
            self.learner_type = 'dt'
        elif learner == rt.RTLearner:
            self.learner_type = 'rt'
        else: 
            self.learner_type = 'lrl'   
        for i in range(0,bags):
            if learner == dt.DTLearner:
                self.learners.append(dt.DTLearner(leaf_size = self.leaf_size))
            elif learner == rt.RTLearner:
                self.learners.append(rt.RTLearner(leaf_size = self.leaf_size))
            else:
                self.learners.append(lrl.LinRegLearner(verbose = False)) 

    def author(self):
        return 'lchen427'

    def addEvidence(self,Xtrain,Ytrain):
        data_count = Xtrain.shape[0]
        for machine in self.learners:
            filter = []
            for i in range(data_count):
                j = np.random.random()
                if j > 0.4:
                    filter.append(True)
                else:
                    filter.append(False)
            Xtrain_bag = Xtrain[filter]
            Ytrain_bag = Ytrain[filter]
            machine.addEvidence(Xtrain_bag,Ytrain_bag)

    def query(self,Xtest):
        n = Xtest.shape[0]
        results = np.ones((self.bags, n))
        i = 0
        for machine in self.learners:
            result = machine.query(Xtest) 
            results[i] = result    
            i = i + 1
        return np.mean(results,axis=0)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
