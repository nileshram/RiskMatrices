'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np
from pricing.dataframemodel import NormalEuroOption
from model.datamodel import OptionsModel, FuturesModel
from configuration import ConfigurationFactory

class RiskMatrix:
    
    def __init__(self):
        self.size = 20
        self._init_config()
        self._init_fut_model()
        self._init_opt_model()
        
        #add model shocks
        self.add_model_shocks(self.config, "ECB", "euribor")
        #init_params
        self._add_model_config_params()
        
    def _init_config(self):
        self.config = ConfigurationFactory.create_config()
    
    def _init_fut_model(self):
        self.fut_model = FuturesModel()
    
    def _init_opt_model(self):
        self.opt_model = OptionsModel()
    
    def _add_model_config_params(self):
        self.fut_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.config)
        self.fut_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.config)
        self.opt_model.model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.config)
        self.opt_model.model.add_config_contract_spec("TickValue", "tick_value",
                                                self.config)
        
    def add_model_shocks(self, config, scenario, product):
        self.shock_model = self.opt_model
        #drop the unused expiries
        print("missing data {}".format(self.shock_model.model[self.shock_model.model.isnull().any(axis=1)]))
        self.shock_model.model.dropna(inplace=True, axis=1)
        self.shock_model.model = self.shock_model.model[self.shock_model.model["ProductName"] == product]
        self.shock_model._add_config_model_shocks(config, scenario)
    
    def run_model_shocks(self, scenario):
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
    
    def compute_fut_pl(self, x, y, df_r):
        new_fut_px = df_r["Theo"] + x
        pl = (new_fut_px - df_r["Theo"]) * df_r["Position"] * \
        df_r["TickValue"] * df_r["Multiplier"]
        return pl


import numpy as np
from model.datamodel import fm
import pandas as pd

x_range = np.linspace(-0.05, 0.05, 20)
y_range = np.linspace(0, 0, 20)
model_fut = fm.model
model_fut["TickValue"] = 25
model_fut["Multiplier"] = 1000
model_fut = model_fut.iloc[0]
 
 
print(x_range)
print(y_range)
print(model_fut)

r = RiskMatrix()
xx, yy = np.meshgrid(x_range, y_range)
m_res = r.compute_fut_pl(xx, yy, model_fut)
print(m_res)
print("Length of pl matrix {}x{}".format(len(m_res), len(m_res)))

# r2 = RiskMatrix()
# x1, y1 = np.meshgrid(x_range, y_range)
# m2_res = r2.compute_opt_pl(x, y, df_r)
    