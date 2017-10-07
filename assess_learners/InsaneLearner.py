"""
A simple wrapper for decision tree.  (c) 2017 Li Chen
"""

import numpy as np
import DTLearner as dt
import LinRegLearner as lrl
import RTLearner as rt
import BagLearner as bg

class InsaneLearner(object):

    def __init__(self,verbose=False):
        self.learners = []
        for i in range(20):
            self.learners.append(bg.BagLearner(verbose = False,bags=20, learner = lrl.LinRegLearner,kwargs = {}, boost = False)) 

    def author(self):
        return 'lchen427'

    def addEvidence(self,Xtrain,Ytrain):
        for machine in self.learners:
            machine.addEvidence(Xtrain,Ytrain)

    def query(self,Xtest):
        n = Xtest.shape[0]
        results = np.ones((20, n))
        i = 0
        for machine in self.learners:
            result = machine.query(Xtest) 
            results[i] = result    
            i = i + 1
        return np.mean(results,axis=0)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
