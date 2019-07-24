'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np

class RiskMatrix:
    
    def __init__(self, fut_model, opt_model):
        self.fut_model = fut_model
        self.opt_model = opt_model
    
    def gen_fut_risk_matrix(self, expiry):
        self.fut_model[expiry].iloc[0]
        pass