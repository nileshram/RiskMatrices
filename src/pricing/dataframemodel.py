"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 20 Jul 2019
Author : nish

"""

from abc import ABCMeta, abstractmethod
from math import sqrt, exp, log
from scipy.stats import norm

class DataFramePricingModel(metaclass=ABCMeta):
    
    def __init__(self, df):
        self._init_params(df)
        
    def _init_params(self, df):
        self.s = df.s
        self.k = df.k
        self.v = df.v
        self.t = df.t
        self.r = df.r

    @abstractmethod
    def price(self):
        raise NotImplementedError("Should implement price()")
    
    @abstractmethod
    def delta(self):
        raise NotImplementedError("Should implement delta()")

    @abstractmethod
    def gamma(self):
        raise NotImplementedError("Should implement gamma()")

    @abstractmethod
    def vega(self):
        raise NotImplementedError("Should implement vega()")

    @abstractmethod
    def theta(self):
        raise NotImplementedError("Should implement theta()")
    
    @classmethod
    def generate_model_obj(cls, df_r):
        return cls(df_r)

    def add_model_param(self, model, param, label, df):
        if hasattr(model, param):
            model_param = getattr(model, param)
            setattr(self, label, model_param(df))

class LeisnerBinomial(DataFramePricingModel):
    
    def __init__(self, df):
        super(LeisnerBinomial, self).__init__(df)
    
    @staticmethod    
    def price():
        pass
     
    @staticmethod
    def delta():
        pass
     
    @staticmethod
    def gamma():
        pass
    @staticmethod
    def vega():
        pass
     
    @staticmethod
    def theta():
        pass
    

class NormalEuroOption(DataFramePricingModel):
    
    def __init__(self, df):
        super(NormalEuroOption, self).__init__(df)
        #Here we have the optionality to return an instance of the model
        #But if we dont want this and only wish to compute greeks individually
        #We call the static methods to compute prices
    
    @staticmethod    
    def price(df_r):
        try:
            d1 = (log(df_r["FuturesPrice"] / df_r["Strike"]) + (df_r["rate"] + (df_r["ActualVolatility"]**2)/2) * df_r["TimeToExpiry"]) / (df_r["ActualVolatility"] * sqrt(df_r["TimeToExpiry"]))
            d2 = d1 - (df_r["ActualVolatility"] * sqrt(df_r["TimeToExpiry"]))
        except ZeroDivisionError:
            print("Error computing option price for {}".format(df_r["ContractName"]))
            d1 = 0
            d2 = 0
        if df_r["PutCall"] == "Call":
            bs = (df_r["FuturesPrice"] * norm.cdf(d1)) - (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(d2))
        elif df_r["PutCall"] == "Put":
            bs = (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(-d2)) - (df_r["FuturesPrice"] * norm.cdf(-d1))
        else:
            print("N/A")
        if bs < 0:
            bs = 0
        return bs
    
    @staticmethod
    def delta(df_r):
        pass
     
    @staticmethod
    def gamma(df_r):
        pass
     
    @staticmethod
    def vega(df_r):
        pass
     
    @staticmethod
    def theta(df_r):
        pass

class OrcNEOModel(DataFramePricingModel):
    pass


