'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np
from pricing.dataframemodel import NormalEuroOption
from model.datamodel import OptionsModel, FuturesModel
from configuration import ConfigurationFactory
from datetime import datetime, time, timedelta
from model.db import DatabaseManager
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import pandas as pd
import logging
from graph.graphlib import GraphEngine

class RiskModel:
    
    def __init__(self, product=None, scenario=None):
        #commented for new size
        #note that the size here has to be n + 1 in self.size in the graphlib
        #self.size = 11
        self.size = 6
        self._init_risk_config()
        #init model
        self._init_fut_model()
        self._init_opt_model()
        self._logger = logging.getLogger("risk_matrix_log")
        
        # Add model shocks
        self.add_model_shocks(config=self.risk_config, product=product, scenario=scenario)
        # Initialise parameters
        self.add_model_config_params()
        #dump model to excel for analysis
#         self.fut_model.model.to_excel("{} - {}.xlsx".format(product, scenario))
#         self.opt_model.model.to_excel("{} - {}.xlsx".format(product, scenario))

    
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
        
    def add_model_shocks(self, config=None, product=None, scenario=None):
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
        return np.linspace(current_fut_level, upper_fut_level, int(size_adj))
    
    def _create_lower_fut_range(self, opt, size):
        size_adj = np.around(size / 2)
        current_fut_level = opt["FuturesPrice"]
        lower_fut_level = opt["FuturesPrice"] + opt["fut_shock_lower"] 
        return np.linspace(lower_fut_level, current_fut_level, int(size_adj))
    
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
            return np.linspace(0, 0, int(size_adj))
        upper_vol_level = (1 + opt["vol_shock_upper"]) * opt["ActualVolatility"] 
        return np.linspace(current_vol_level, upper_vol_level, int(size_adj))
    
    def _create_lower_vol_range(self, opt, size):
        size_adj = np.around(size / 2)
        try:
            current_vol_level = opt["ActualVolatility"]
        except TypeError:
            return np.linspace(0, 0, int(size_adj))
        lower_vol_level = (1 + opt["vol_shock_lower"]) * opt["ActualVolatility"] 
        return np.linspace(lower_vol_level, current_vol_level, int(size_adj))
    
    # Output the futures and volatility matrix
    def create_fut_and_vol_matrix(self, fut_range, vol_range):
        return np.meshgrid(fut_range, vol_range)
    

class RiskEngine:
    
    def __init__(self, scenario=None, product=None):
        self.risk_matrix = RiskModel(product=product, scenario=scenario)
        self._logger = logging.getLogger("risk_matrix_log")
#         self._init_models()

    def _init_models(self):
        self._models = {"w" : {"opt" : self.risk_matrix.shock_model.model[self.risk_matrix.shock_model.model["CurveSegment"] == "whites"],
                                   "fut" : self.risk_matrix.shock_model.fut_model.model[self.risk_matrix.shock_model.fut_model.model["CurveSegment"] == "whites"]},
                            "m" : {"opt" : self.risk_matrix.shock_model.model[self.risk_matrix.shock_model.model["CurveSegment"] == "mids"],
                                   "fut" : self.risk_matrix.shock_model.fut_model.model[self.risk_matrix.shock_model.fut_model.model["CurveSegment"] == "mids"]},
                            "g" : {"opt" : self.risk_matrix.shock_model.model[self.risk_matrix.shock_model.model["CurveSegment"] == "greens"],
                                   "fut" : self.risk_matrix.shock_model.fut_model.model[self.risk_matrix.shock_model.fut_model.model["CurveSegment"] == "greens"]},
                            "b" : {"opt" : self.risk_matrix.shock_model.model[self.risk_matrix.shock_model.model["CurveSegment"] == "blues"],
                                   "fut" : self.risk_matrix.shock_model.fut_model.model[self.risk_matrix.shock_model.fut_model.model["CurveSegment"] == "blues"]},
                            "all" : {"opt" : self.risk_matrix.shock_model.model,
                                   "fut" : self.risk_matrix.shock_model.fut_model.model}
                            }
        

    def run_pricing_and_risk(self):
        self._init_models()
        start_time = datetime.now()
        self._run_option_model_pricing() # computes options pl per curve segment
        self._run_futures_model_pricing() # computes futs pl per curve segment
        self._sum_futures_and_options_risk() # computes the combined pl risk from options and futures
        end_time = datetime.now()
        #compute elapsed time here
        elapsed_time = end_time - start_time
        self._logger.info("Elapsed time - Seconds: {}, Microseconds: {}".format(elapsed_time.seconds, elapsed_time.microseconds))
        #generate graph figures here
        self._generate_heatplot()

    def _run_option_model_pricing(self):
        self._logger.info("Initialising option model pricing")
        for curve_segment in self._models:
            model = self._models[curve_segment]["opt"]
            sum_matrix = 0
            for idx, opt in model.iterrows():
                x_range = self.risk_matrix.create_fut_range(opt, self.risk_matrix.size)
                y_range = self.risk_matrix.create_vol_range(opt, self.risk_matrix.size)
                xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
                matrix = self.risk_matrix.compute_opt_pl(xx, yy, opt)
                self._logger.info("{}) Computed risk matrix for {}".format(idx, opt["ContractName"]))
                sum_matrix += matrix
            self._models[curve_segment]["opt"] = sum_matrix

    def _run_futures_model_pricing(self):
        self._logger.info("Initialising futures model pricing")
        for curve_segment in self._models:
            model = self._models[curve_segment]["fut"]
            sum_matrix = 0
            for idx, fut in model.iterrows():
                x_range = self.risk_matrix.create_fut_range(fut, self.risk_matrix.size)
                y_range = self.risk_matrix.create_vol_range(0, self.risk_matrix.size)
                xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
                matrix = self.risk_matrix.compute_fut_pl(xx, yy, fut)
                self._logger.info("{}) Computed risk matrix for {}".format(idx, fut["FutureContract"]))
                sum_matrix += matrix
            self._models[curve_segment]["fut"] = sum_matrix

    def _sum_futures_and_options_risk(self):
        for curve_segment in self._models:
            self._models[curve_segment]["summary"] = self._models[curve_segment]["opt"] + self._models[curve_segment]["fut"]

    def _generate_heatplot(self):
        for curve_segment in self._models:
            self._models[curve_segment]["graph"] = GraphEngine().plot_heatmap(self._models[curve_segment]["summary"])
            
    def write_to_excel(self, array):
        temp_arr = np.array(array)
        df = pd.DataFrame(temp_arr)
        df.to_excel('test_file.xlsx', index=False, header=False)

    