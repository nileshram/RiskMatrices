'''
Created on 24 Jul 2019

@author: nish
'''
import pandas as pd
from service.file import FileManager
from contract.functions import DateFunctions, ContractSpecification
from pricing.dataframemodel import NormalEuroOption
import logging
#global
pd.options.display.float_format = '{:2,.6f}'.format

class DataModel:
    
    def __init__(self):
        self.model = FileManager.get_csv_data()
        self._logger = logging.getLogger("risk_matrix_log")
    
    def add_model_param(self, param, function, args=None):
        if args is None:
            self.model[param] = self.model.apply(lambda x: function(x), axis=1)
        else:
            self.model[param] = self.model.apply(function, args=args, axis=1)
            
    def convert_to_datetime(self, param):
        self.model[param] = pd.to_datetime(self.model[param])
    
    def sort_model(self, param):
        self.model.sort_values(by=param, inplace=True, ascending=True)
    
    def remove_params(self, *args):
        cols = [arg for arg in args]
        self.model.drop(columns=cols, inplace=True)
    
    def rename_param(self, old_param, new_param):
        self.model.rename(columns={old_param : new_param}, inplace=True)
    
    def add_config_contract_spec(self, new_param_name, param, c):
        self.model[new_param_name] = self.model["ProductName"].map(c["contract_spec"][param])

    def _add_config_model_shocks(self, config, scenario):
        self.add_model_param("fut_shock_upper", ContractSpecification.add_fut_shock_upper,
                                   args=(config, scenario))
        self.add_model_param("fut_shock_lower", ContractSpecification.add_fut_shock_lower,
                                   args=(config, scenario))
        self.add_model_param("vol_shock_upper", ContractSpecification.add_vol_shock_upper,
                                   args=(config, scenario))
        self.add_model_param("vol_shock_lower", ContractSpecification.add_vol_shock_lower,
                                   args=(config, scenario))
        
class FuturesModel(DataModel):
    
    def __init__(self):
        super(FuturesModel, self).__init__()
        
        #Initialise Model
        self._init_futures_data()
        
        #Add fields
        self.add_date_codes()
        self.sort_model("ExpiryDate")
        
        #Drop non used fields
        self.remove_params("Symbol", "Strike", "PutCall",
                           "Name", "Delta", "Theta", "Gamma",
                           "ActualVolatility", "ImpliedVolatility",
                           "Vega")
        
        self.rename_param("Theo", "FuturesPrice")
        
    def _init_futures_data(self):
        self.model = self.model[(self.model["Product"] == "Future")
                                & (self.model["Position"] != 0)]

        
    def add_date_codes(self):
        self.convert_to_datetime("ExpiryDate")
        self.add_model_param("UnderlyingFutureMonthCode", DateFunctions.add_month_code)
        self.add_model_param("UnderlyingFutureYY", DateFunctions.get_year_expiry)
        self.add_model_param("UnderlyingFutureMM-YY", DateFunctions.add_mm_yy)
        self.add_model_param("UnderlyingFuturePCC", ContractSpecification.add_contract_spec)
        self.add_model_param("FutureContract", ContractSpecification.add_future_contract_name)
        self.add_model_param("ProductName", ContractSpecification.add_product)
        self.add_model_param("ExpiryIndex", ContractSpecification.add_fut_expiries)
         
class OptionsModel(DataModel):
    
    def __init__(self):
        super(OptionsModel, self).__init__()
        self._init_options_data()
        
        #add contract specs
        self.add_product_classifier()
        
        #Drop non used fields
        self.remove_params("Name", "Delta", "Theta", "Gamma", "Vega",
                           "ImpliedVolatility")
        
        self._init_futures_model()
        self.add_futures_model()
        self.compute_theo(NormalEuroOption.price)
        
    def _init_options_data(self):
        self.model = self.model[(self.model["Product"] == "Option")
                                & (self.model["Position"] != 0)]
        
    def _init_futures_model(self):
        self.fut_model = FuturesModel()
        
    def compute_theo(self, opt_model):
        self.model = self.model.assign(rate=0) #default rate = 0 for BS pricing
        self.model.round({"Theo": 5}) #Round existing theo 6dp
        self.add_model_param("atl_bs_theo", opt_model)
        
    def add_product_classifier(self):
        self.convert_to_datetime("ExpiryDate")
        self.add_model_param("MonthCode", DateFunctions.add_month_code)
        self.add_model_param("ExpiryYear", DateFunctions.get_year_expiry)
        self.add_model_param("PCC", ContractSpecification.add_contract_spec)
        
        self.add_model_param("UnderlyingFutureMonthCode", DateFunctions.add_underlying_future_month_code)
        self.add_model_param("UnderlyingFutureYY", ContractSpecification.add_underling_future_expiry_year)
        self.add_model_param("UnderlyingFuturePCC", ContractSpecification.add_underlying_contract_spec)
        self.add_model_param("ProductName", ContractSpecification.add_product)
        self.add_model_param("ContractName", ContractSpecification.add_option_contract_name)
        
    def add_futures_model(self):
        self.model = pd.merge(self.model, self.fut_model.model[["UnderlyingFutureMonthCode",
                                                                "UnderlyingFuturePCC", 
                                                                "UnderlyingFutureYY",
                                                                "FutureContract",
                                                                "ExpiryIndex", 
                                                                "FuturesPrice"]],
                                                                on=["UnderlyingFutureMonthCode",
                                                                "UnderlyingFuturePCC", 
                                                                "UnderlyingFutureYY"],
                                                                how="left")


    