'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np
from pricing.dataframemodel import NormalEuroOption
from model.datamodel import OptionsModel, FuturesModel
from configuration import ConfigurationFactory
from model.db import DatabaseManager
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import pandas as pd
import logging

class RiskModel:
    
    def __init__(self):
        self.size = 11
        self._init_risk_config()
        #init model
        self._init_fut_model()
        self._init_opt_model()
        self._logger = logging.getLogger("risk_matrix_log")
        
        # Add model shocks
        self.add_model_shocks(self.risk_config, "ECB", "euribor")
        # Initialise parameters
        self.add_model_config_params()
        
    def _init_risk_config(self):
        self.risk_config = ConfigurationFactory.create_config(name="RISK")
        self._db_config = ConfigurationFactory.create_config(name="LOG")
    
    def _init_fut_model(self):
        self.fut_model = FuturesModel()
    
    def _init_opt_model(self):
        self.opt_model = OptionsModel()
    
    def add_model_config_params(self):
        self.fut_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.risk_config)
        self.fut_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.risk_config)
        self.shock_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.risk_config)
        self.shock_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.risk_config)
        self.shock_model.fut_model.add_config_contract_spec("TickValue", "tick_value",
                                                self.risk_config)
        self.shock_model.fut_model.add_config_contract_spec("Multiplier", "multiplier",
                                                self.risk_config)
        
    def add_model_shocks(self, config, scenario, product):
        self.shock_model = self.opt_model
        # Drop the unused expiries
        self._logger.info("missing data {}".format(self.shock_model.model[self.shock_model.model.isnull().any(axis=1)]))
        self.shock_model.model.dropna(inplace=True)
        self.shock_model.model = self.shock_model.model[self.shock_model.model["ProductName"] == product]
        self.shock_model.fut_model.model = self.shock_model.fut_model.model[self.shock_model.fut_model.model["ProductName"] == product]
        self.shock_model._add_config_model_shocks(config, scenario)
        self.shock_model.fut_model._add_config_model_shocks(config, scenario)
        #reindex futures and shock model
        self.shock_model.model.reset_index(inplace=True)
        self.shock_model.fut_model.model.reset_index(inplace=True)
    
    def compute_opt_pl(self, fut_arr, vol_arr, df_r):
        # Define vectorised option parameters here:
        K = df_r["Strike"]
        contract_type = df_r["PutCall"]
        time = df_r["TimeToExpiry"]
        theo = df_r["Theo"]
        r = df_r["rate"]
        pos = df_r["Position"]
        tick_value = df_r["TickValue"]
        contract_name = df_r["ContractName"]
        # Compute option matrix here
        new_theo_array = NormalEuroOption.array_pricer(strike=K, time_to_expiry=time, 
                                                       rate=r, opt_type=contract_type,
                                                       fut_arr=fut_arr, vol_arr=vol_arr, c_name=contract_name)
        # Compute option P&L here:
        pl = (new_theo_array - theo) * pos * tick_value * 100
        return pl
        
    # Compute the futures P&L
    def compute_fut_pl(self, fut_arr, vol_arr, df_r):
        pl = (fut_arr - df_r["FuturesPrice"]) * 100 * df_r["Position"] * df_r["TickValue"]
        return pl
    
    # Creates the futures range
    def create_fut_range(self, opt, size):
        upper_fut_range = self._create_upper_fut_range(opt, size)
        lower_fut_range = self._create_lower_fut_range(opt, size)
        return np.concatenate((lower_fut_range, upper_fut_range))
    
    def _create_upper_fut_range(self, opt, size):
        size_adj = np.around(size / 2) #here we take half the size
        current_fut_level = opt["FuturesPrice"] #this is form mid point of the range
        upper_fut_level = opt["FuturesPrice"] + opt["fut_shock_upper"]
        return np.linspace(current_fut_level, upper_fut_level, size_adj)
    
    def _create_lower_fut_range(self, opt, size):
        size_adj = np.around(size / 2)
        current_fut_level = opt["FuturesPrice"]
        lower_fut_level = opt["FuturesPrice"] + opt["fut_shock_lower"] 
        return np.linspace(lower_fut_level, current_fut_level, size_adj)
    
    # Create the volatility range
    def create_vol_range(self, opt, size):
        upper_vol_range = self._create_upper_vol_range(opt, size)
        lower_vol_range = self._create_lower_vol_range(opt, size)
        return np.concatenate((lower_vol_range, upper_vol_range))

    def _create_upper_vol_range(self, opt, size):
        size_adj = np.around(size / 2)
        try:
            current_vol_level = opt["ActualVolatility"]
        except TypeError:
            return np.linspace(0, 0, size_adj)
        upper_vol_level = (1 + opt["vol_shock_upper"]) * opt["ActualVolatility"] 
        return np.linspace(current_vol_level, upper_vol_level, size_adj)
    
    def _create_lower_vol_range(self, opt, size):
        size_adj = np.around(size / 2)
        try:
            current_vol_level = opt["ActualVolatility"]
        except TypeError:
            return np.linspace(0, 0, size_adj)
        lower_vol_level = (1 + opt["vol_shock_lower"]) * opt["ActualVolatility"] 
        return np.linspace(lower_vol_level, current_vol_level, size_adj)
    
    # Output the futures and volatility matrix
    def create_fut_and_vol_matrix(self, fut_range, vol_range):
        return np.meshgrid(fut_range, vol_range)
    

class RiskEngine:
    
    def __init__(self):
        self.risk_matrix = RiskModel()
        self._logger = logging.getLogger("risk_matrix_log")
    
    def run_pricing(self):
        opt_matrix = self._run_options_pricing()
        fut_matrix = self._run_futures_pricing()
        portfolio_matrix = opt_matrix + fut_matrix
        # Plot portfolio matrix
        self.plot_heatmap(portfolio_matrix)
#         self.write_to_excel(portfolio_matrix)

    def run_pricing_and_risk(self, product=None, scenario=None):
        opt_matrix = self._run_options_pricing()
        fut_matrix = self._run_futures_pricing()
        portfolio_matrix = opt_matrix + fut_matrix
        # Plot portfolio matrix
        return portfolio_matrix

    def _run_options_pricing(self):
        sum_matrix = 0
        for idx, opt in self.risk_matrix.shock_model.model.iterrows():
            x_range = self.risk_matrix.create_fut_range(opt, self.risk_matrix.size)
            y_range = self.risk_matrix.create_vol_range(opt, self.risk_matrix.size)
            xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
            matrix = self.risk_matrix.compute_opt_pl(xx, yy, opt)
            self._logger.info("{}) Computed risk matrix for {}".format(idx, opt["ContractName"]))
            sum_matrix += matrix
        return sum_matrix
    
    def _run_futures_pricing(self):
        sum_matrix = 0
        for idx, fut in self.risk_matrix.shock_model.fut_model.model.iterrows():
            x_range = self.risk_matrix.create_fut_range(fut, self.risk_matrix.size)
            y_range = self.risk_matrix.create_vol_range(0, self.risk_matrix.size)
            xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
            matrix = self.risk_matrix.compute_fut_pl(xx, yy, fut)
            sum_matrix += matrix
        return sum_matrix

    def plot_heatmap(self, graph_model):
        self.size = 12
        fig, ax = plt.subplots()
        cm = mplc.LinearSegmentedColormap.from_list("", ["red","white","green"])
        im = ax.imshow(graph_model, cmap=cm)
        
        # Display all of the ticks
        ax.set_xticks(np.arange(self.size))
        ax.set_yticks(np.arange(self.size))
        # Label each of the x/y tick labels
        ax.set_xticklabels(["-", "-", "-", "-", "-", 0, 0, "+", "+", "+", "+", "+"])
        ax.set_yticklabels(["-", "-", "-", "-", "-", 0, 0, "+", "+", "+", "+", "+"][::-1])
        
        ax.set_xlabel("Futures step")
        ax.set_ylabel("Volatility")
        # Loop over data dimensions and create text annotations.
        for i in range(self.size):
            for j in range(self.size):
                text = ax.text(j, i, round(graph_model[i, j]/1000, 2),
                               ha="center", va="center", color="black",
                               size=8, fontweight='bold')
        ax.set_title("P&L Portfolio Heatmap ('000s)")
        fig.tight_layout()
        plt.colorbar(im)
        plt.show()
    
    def write_to_excel(self, array):
        temp_arr = np.array(array)
        df = pd.DataFrame(temp_arr)
        df.to_excel('test_file.xlsx', index=False, header=False)

    