'''
Created on 24 Jul 2019

@author: nish
'''
import pandas as pd
from service.file import FileManager
from contract.functions import DateFunctions, ContractSpecification
from pricing.dataframemodel import NormalEuroOption

class DataModel:
    
    def __init__(self):
        self.model = FileManager.get_csv_data()
    
    def add_model_param(self, param, function):
        self.model[param] = self.model.apply(lambda x: function(x), axis=1)
    
    def convert_to_datetime(self, param):
        self.model[param] = pd.to_datetime(self.model[param])
    
    def sort_model(self, param):
        self.model.sort_values(by=param, inplace=True, ascending=True)
    
    def remove_params(self, *args):
        cols = [arg for arg in args]
        self.model.drop(columns=cols, inplace=True)
        
class FuturesModel(DataModel):
    
    def __init__(self):
        super(FuturesModel, self).__init__()
        
        #Initialise Model
        self._init_futures_data()
        self.convert_to_datetime("ExpiryDate")
        
        #Add fields
        self.add_date_codes()
        self.sort_model("ExpiryDate")
        
        #Drop non used fields
        self.remove_params("Symbol", "Strike", "PutCall",
                           "Name", "Delta", "Theta", "Gamma",
                           "ActualVolatility", "ImpliedVolatility",
                           "Vega")
        
    def _init_futures_data(self):
        self.model = self.model[(self.model["Product"] == "Future")
                                & (self.model["Position"] != 0)]

        
    def add_date_codes(self):
        self.add_model_param("MonthCode", DateFunctions.add_month_code)
        self.add_model_param("ExpiryYear", DateFunctions.get_year_expiry)
        self.add_model_param("MM-YY", DateFunctions.add_month_year)
        self.add_model_param("PCC", ContractSpecification.add_contract_spec)
        self.add_model_param("FutureContract", ContractSpecification.add_future_contract_name)
        self.add_model_param("ExpiryIndex", ContractSpecification.add_fut_expiries)
        
class OptionsModel(DataModel):
    
    def __init__(self):
        super(OptionsModel, self).__init__()
        self._init_options_data()
        self.compute_theo(NormalEuroOption.price)
        
    def _init_options_data(self):
        self.model = self.model[(self.model["Product"] == "Option")
                                & (self.model["Position"] != 0)]
        
    
    def compute_theo(self, opt_model):
        self.add_model_param("bs_theo", opt_model)


fm = FuturesModel()
print(fm.model.iloc[0])


    
    