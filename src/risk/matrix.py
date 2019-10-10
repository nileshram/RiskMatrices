'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np
from pricing.dataframemodel import NormalEuroOption
from model.datamodel import OptionsModel, FuturesModel
from configuration import ConfigurationFactory
import matplotlib.pyplot as plt
import matplotlib.colors

class RiskModel:
    
    def __init__(self):
        self.size = 11
        self._init_config()
        self._init_fut_model()
        self._init_opt_model()
        
        #add model shocks
        self.add_model_shocks(self.config, "ECB", "euribor")
        #init_params
        self.add_model_config_params()
        
    def _init_config(self):
        self.config = ConfigurationFactory.create_config()
    
    def _init_fut_model(self):
        self.fut_model = FuturesModel()
    
    def _init_opt_model(self):
        self.opt_model = OptionsModel()
    
    def add_model_config_params(self):
        self.fut_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.config)
        self.fut_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.config)
        self.shock_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.config)
        self.shock_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.config)
        self.shock_model.fut_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.config)
        self.shock_model.fut_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.config)
        
    def add_model_shocks(self, config, scenario, product):
        self.shock_model = self.opt_model
        #drop the unused expiries
        print("missing data {}".format(self.shock_model.model[self.shock_model.model.isnull().any(axis=1)]))
        self.shock_model.model.dropna(inplace=True)
        self.shock_model.model = self.shock_model.model[self.shock_model.model["ProductName"] == product]
        self.shock_model.fut_model.model = self.shock_model.fut_model.model[self.shock_model.fut_model.model["ProductName"] == product]
        self.shock_model._add_config_model_shocks(config, scenario)
        self.shock_model.fut_model._add_config_model_shocks(config, scenario)
    
    def run_model_shocks(self, scenario):
        pass
    
    
    def gen_fut_risk_matrix(self, expiry):
        pass
    
#     @np.vectorize
    def compute_opt_pl(self, x, y, df_r):
        #define option parameters here:
        K = df_r["Strike"]
        contract_type = df_r["PutCall"]
        time = df_r["TimeToExpiry"]
        theo = df_r["Theo"]
        r = df_r["rate"]
        pos = df_r["Position"]
        tick_value = df_r["TickValue"]
        #assign vol and fut array
        fut_arr = df_r["FuturesPrice"] + x
        vol_arr = (1 + y) * df_r["ActualVolatility"]
        new_theo_array = NormalEuroOption.array_pricer(strike=K, time_to_expiry=time, rate=r, opt_type=contract_type,
                                                  fut_arr=fut_arr, vol_arr=vol_arr)
        
        #compute option pl here:
        pl = (new_theo_array - theo) * pos * tick_value * 100
        graph_model = np.around(pl, decimals=0)
        
        #plot heatmap here
        fig, ax = plt.subplots()
#         cm = plt.cm.get_cmap('bwr')
        cm = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","white","green"])
        im = ax.imshow(graph_model, cmap=cm)
        
        # We want to show all ticks...
        ax.set_xticks(np.arange(len(fut_arr)))
        ax.set_yticks(np.arange(len(vol_arr)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(np.around(fut_arr[0], decimals=3))
        ax.set_yticklabels(np.around(vol_arr[:,0], decimals=3))
        
        ax.set_xlabel("Futures step")
        ax.set_ylabel("Volatility")
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        # Loop over data dimensions and create text annotations.
        for i in range(len(fut_arr)):
            for j in range(len(vol_arr)):
                text = ax.text(j, i, graph_model[i, j],
                               ha="center", va="center", color="black")
        ax.set_title("P&L Portfolio Heatmap Test")
        fig.tight_layout()
        plt.colorbar(im)
        plt.show()
    
        return pl
    
    #Compute the futures P&L
    def compute_fut_pl(self, x, y, df_r):
        new_fut_px = df_r["FuturesPrice"] + x
        pl = (new_fut_px - df_r["FuturesPrice"]) * 100 * df_r["Position"] * \
        df_r["TickValue"]
        return pl
    
    #Creates the futures range
    def create_fut_range(self, max_shock_ticks, size):
        return np.linspace(-max_shock_ticks, max_shock_ticks, size)
    
    #Create the volatility range
    def create_vol_range(self, max_vol_shock, size):
        return np.linspace(-max_vol_shock, max_vol_shock, size)
    
    #Output the futures and volatility matrix
    def create_fut_and_vol_matrix(self, fut_range, vol_range):
        xy_pairs = np.vstack([fut_range.reshape(-1), vol_range.reshape(-1)])
        print("xy-pairs {}".format(xy_pairs))
        return np.meshgrid(fut_range, vol_range)
    

class RiskEngine:
    
    def __init__(self):
        self.risk_matrix = RiskModel()
    
    def run(self):
#         for idx, opt in self.risk_matrix.shock_model.model.iterrows():
        idx = 0
        opt = self.risk_matrix.shock_model.model.iloc[0]
        x_range = self.risk_matrix.create_fut_range(opt["fut_shock_upper"], self.risk_matrix.size)
        y_range = self.risk_matrix.create_vol_range(opt["vol_shock_upper"], self.risk_matrix.size)
        xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
        matrix = self.risk_matrix.compute_opt_pl(xx, yy, opt)
        print("Matrix Id: {} P&L Matrix: {}".format(idx, matrix))
        
        #temp graphing lib
        
    
    def _run(self):
        for idx, fut in self.risk_matrix.shock_model.fut_model.model.iterrows():
            x_range = self.risk_matrix.create_fut_range(fut["fut_shock_upper"], self.risk_matrix.size)
            y_range = self.risk_matrix.create_vol_range(0, self.risk_matrix.size)
            xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
            matrix = self.risk_matrix.compute_fut_pl(xx, yy, fut)
            print("Matrix Id: {} P&L Matrix: {}".format(idx, matrix))

risk_engine = RiskEngine()
risk_engine.run()

# z = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# z2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print(np.add(z, z2))


# import numpy as np
# from model.datamodel import fm
# import pandas as pd
# 
# x_range = np.linspace(-0.05, 0.05, 20)
# y_range = np.linspace(0, 0, 20)
# model_fut = fm.model
# model_fut["TickValue"] = 25
# model_fut["Multiplier"] = 1000
# model_fut = model_fut.iloc[0]
#  
#  
# print(x_range)
# print(y_range)
# print(model_fut)
# 
# r = RiskEngine()
# xx, yy = np.meshgrid(x_range, y_range)
# m_res = r.compute_fut_pl(xx, yy, model_fut)
# print(m_res)
# print("Length of pl matrix {}x{}".format(len(m_res), len(m_res)))

    