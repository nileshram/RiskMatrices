'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np
from pricing.dataframemodel import NormalEuroOption

class RiskMatrix:
    
    def __init__(self):
        pass
    
    def gen_fut_risk_matrix(self, expiry):
        pass
    
    def gen_upper_fut_arr(self, df_r):
        return np.linspace()
    
    def gen_lower_fut_arr(self):
        pass
    
    def gen_upper_vol_arr(self):
        pass
    
    def gen_lower_vol_arr(self):
        pass
    
    @np.vectorize
    def compute_opt_pl(self, x, y, df_r):
        cur_theo = df_r["Theo"]
        #assign new vol and fut
        df_r["ActualVolatility"] = y
        df_r["UnderlyingFuture"] = x
        new_theo = NormalEuroOption.price(df_r)
        
        pl = (new_theo - cur_theo) * df_r["Position"] * \
        df_r["Multiplier"] * df_r["TickValue"]
        
        return pl
    
    @np.vectorize
    def compute_fut_pl(self, x, y, df_r):
        new_fut_px = df_r["Theo"] + x
        pl = new_fut_px * df_r["Theo"] * df_r["Position"] * \
        df_r["TickValue"] * df_r["Multiplier"]
        return pl


import numpy as np

x_fut_range = np.linspace(-0.05, 0.05, 20)
y_fut_range = np.linspace(0, 0, 20)
print(x_fut_range)
print(y_fut_range)
    