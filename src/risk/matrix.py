'''
Created on 24 Jul 2019

@author: nish
'''
import numpy as np
from pricing.dataframemodel import NormalEuroOption
from model.datamodel import OptionsModel, FuturesModel
from configuration import ConfigurationFactory
import matplotlib.pyplot as plt
import matplotlib.colors as mplc

class RiskModel:
    
    def __init__(self):
        self.size = 11
        self._init_config()
        self._init_fut_model()
        self._init_opt_model()
        
        # Add model shocks
        self.add_model_shocks(self.config, "ECB", "euribor")
        # Initialise parameters
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
        # Drop the unused expiries
        print("missing data {}".format(self.shock_model.model[self.shock_model.model.isnull().any(axis=1)]))
        self.shock_model.model.dropna(inplace=True)
        self.shock_model.model = self.shock_model.model[self.shock_model.model["ProductName"] == product]
        self.shock_model.fut_model.model = self.shock_model.fut_model.model[self.shock_model.fut_model.model["ProductName"] == product]
        self.shock_model._add_config_model_shocks(config, scenario)
        self.shock_model.fut_model._add_config_model_shocks(config, scenario)
    
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
        new_theo_array = NormalEuroOption.array_pricer(strike=K, time_to_expiry=time, rate=r, opt_type=contract_type,
                                                  fut_arr=fut_arr, vol_arr=vol_arr, c_name=contract_name)
        # Compute option P&L here:
        pl = (new_theo_array - theo) * pos * tick_value * 100
        return pl
        
    # Compute the futures P&L
    def compute_fut_pl(self, x, y, df_r):
        new_fut_px = df_r["FuturesPrice"] + x
        pl = (new_fut_px - df_r["FuturesPrice"]) * 100 * df_r["Position"] * \
        df_r["TickValue"]
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
            print("Could not generate matrix for the following {}".format(opt))
        upper_vol_level = (1 + opt["vol_shock_upper"]) * opt["ActualVolatility"] 
        return np.linspace(current_vol_level, upper_vol_level, size_adj)
    
    def _create_lower_vol_range(self, opt, size):
        size_adj = np.around(size / 2)
        try:
            current_vol_level = opt["ActualVolatility"]
        except TypeError:
            print("Could not generate matrix for the following {}".format(opt))
        lower_vol_level = (1 + opt["vol_shock_lower"]) * opt["ActualVolatility"] 
        return np.linspace(lower_vol_level, current_vol_level, size_adj)
    
    # Output the futures and volatility matrix
    def create_fut_and_vol_matrix(self, fut_range, vol_range):
        return np.meshgrid(fut_range, vol_range)
    

class RiskEngine:
    
    def __init__(self):
        self.risk_matrix = RiskModel()
    
    def run_pricing(self):
        opt_matrix = self._run_options_pricing()
        fut_matrix = self._run_futures_pricing()
        portfolio_matrix = opt_matrix + fut_matrix
        # Plot portfolio matrix
        self.plot_heatmap(portfolio_matrix)


    def _run_options_pricing(self):
        sum_matrix = 0
        for idx, opt in self.risk_matrix.shock_model.model.iterrows():
            x_range = self.risk_matrix.create_fut_range(opt, self.risk_matrix.size)
            y_range = self.risk_matrix.create_vol_range(opt, self.risk_matrix.size)
            xx, yy = self.risk_matrix.create_fut_and_vol_matrix(x_range, y_range)
            matrix = self.risk_matrix.compute_opt_pl(xx, yy, opt)
            print("{}) Computed risk matrix for {}".format(idx, opt["ContractName"]))
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
        fig, ax = plt.subplots()
        cm = mplc.LinearSegmentedColormap.from_list("", ["red","white","green"])
        im = ax.imshow(graph_model, cmap=cm)
        
        # Display all of the ticks
        ax.set_xticks(np.arange(len(self.size)))
        ax.set_yticks(np.arange(len(self.size)))
        # Label each of the x/y tick labels
#         ax.set_xticklabels(np.around(fut_arr[0], decimals=3))
#         ax.set_yticklabels(np.around(vol_arr[:,0], decimals=3))
        
        ax.set_xlabel("Futures step")
        ax.set_ylabel("Volatility")
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        # Loop over data dimensions and create text annotations.
        for i in range(len(self.size)):
            for j in range(len(self.size)):
                text = ax.text(j, i, graph_model[i, j],
                               ha="center", va="center", color="black")
        ax.set_title("P&L Portfolio Heatmap")
        fig.tight_layout()
        plt.colorbar(im)
        plt.show()

if __name__ == "__main__":
    risk_engine = RiskEngine()
    risk_engine.run_pricing()

    