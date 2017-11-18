"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states = 100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.rar = rar
        self.radr = radr
        self.s = 0
        self.a = 0
        self.Q = np.full((self.num_states,self.num_actions),-1.0)
        self.R = np.zeros((self.num_states,self.num_actions))
        self.T = np.full((self.num_states,self.num_actions,self.num_states),0.000000001)
        self.Tc = np.full((self.num_states,self.num_actions,self.num_states),0.00000001)
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if rand.random() >= self.rar:
            action = np.argmax(self.Q[s,:])
        else:
            action = rand.randint(0,self.num_actions - 1)
        self.rar = self.rar * self.radr
        self.a = action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        self.Q[self.s, self.a] = (1 - self.alpha) * (self.Q[self.s, self.a]) + self.alpha * (r + self.gamma * self.Q[s_prime,np.argmax(self.Q[s_prime,:])])
        if self.dyna > 0:
            self.Tc[self.s,self.a,s_prime] = self.Tc[self.s,self.a,s_prime] + 1
            self.R[self.s,self.a] = (1 - self.alpha) * self.R[self.s,self.a] + self.alpha * r          
            self.T[self.s,self.a,:] = self.Tc[self.s,self.a,:] / np.sum(self.Tc[self.s,self.a,:])

        if np.sum(self.Tc) > 3500 and self.dyna > 0:
            #print "hallucination"
            for k in range(0, self.dyna):
                s = rand.randint(0, self.num_states-1)
                a = rand.randint(0, self.num_actions-1)
                if np.sum(self.Tc[s,a,:]) < 1:
                    pass
                else:
                    r = self.R[s,a]
                    s_primmy = np.argmax(np.random.multinomial(1, self.T[s,a,:])) #s_primmy is s_prime in the hallucilation process
                    self.Q[s,a] = (1.0 - self.alpha) * self.Q[s,a] + self.alpha * (r + self.gamma * self.Q[s_primmy,np.argmax(self.Q[s_primmy,:])])

        if self.verbose: print "s =", s_prime,"a =",self.a,"r =",r
        self.a = self.querysetstate(s_prime)
        return self.a

    def author(self):
        return 'lchen427'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
