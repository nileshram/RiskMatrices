'''
Created on 13 Aug 2019

@author: nish
'''
import numpy as np

class RiskEngine:
    
    def __init__(self, matrix):
        pass
    
    def compute_shocks(self):
        pass
    
    def add_shocks(self):
        pass
    
    def create_fut_range(self, max_shock_ticks, size):
        return np.linspace(-max_shock_ticks, max_shock_ticks, size)
    
    def create_vol_range(self, max_vol_shock, size):
        return np.linspace(-max_vol_shock, max_vol_shock, size)
    
    def create_fut_and_vol_matrix(self, fut_range, vol_range):
        return np.meshgrid(fut_range, vol_range)
    
    def calculate_fut_pl_matrix(self, xx, yy, fut_model):
        pass
        
    
    