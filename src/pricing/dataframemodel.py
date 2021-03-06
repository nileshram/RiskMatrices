"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 20 Jul 2019
Author : nish

"""

from abc import ABCMeta, abstractmethod
from math import sqrt, exp, log
from scipy.stats import norm
import numpy as np
import logging
logger = logging.getLogger("risk_matrix_log")

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
            logger.info("Error computing option price for {}".format(df_r["ContractName"]))
            return 0
        if df_r["PutCall"] == "Call":
            bs = (df_r["FuturesPrice"] * norm.cdf(d1)) - (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(d2))
        elif df_r["PutCall"] == "Put":
            bs = (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(-d2)) - (df_r["FuturesPrice"] * norm.cdf(-d1))
        else:
            logger.info("N/A")
#         if bs < 0:
#             bs = 0
        return bs

    @staticmethod    
    def array_pricer(strike=None, time_to_expiry=None, rate=None, opt_type=None, fut_arr=None, vol_arr=None, c_name=None):
        try:
            d1 = (np.log(fut_arr / strike) + (rate + (vol_arr**2)/2) * time_to_expiry) / (vol_arr * sqrt(time_to_expiry))
            d2 = d1 - (vol_arr * sqrt(time_to_expiry))
        except (ZeroDivisionError, TypeError, RuntimeWarning) as e:
            logger.info("Encountered exception {} for contract {}".format(e, c_name))
            return 0
        if opt_type == "Call":
            bs = (fut_arr * norm.cdf(d1)) - (strike * exp(-rate * time_to_expiry) * norm.cdf(d2))
        elif opt_type == "Put":
            bs = (strike * exp(-rate * time_to_expiry) * norm.cdf(-d2)) - (fut_arr * norm.cdf(-d1))
        else:
            print("Invalid option type specified please check if calls or puts")
        return bs

    @staticmethod    
    def shock_pricer_generic(df_r, fut_direction, vol_direction):
        fut_price_shock = df_r["FuturesPrice"] + df_r["fut_shock_{}".format(fut_direction)]
        vol_shock = df_r["ActualVolatility"] * (1 + df_r["vol_shock_{}".format(vol_direction)])
        try:
            d1 = (log(fut_price_shock / df_r["Strike"]) + (df_r["rate"] + (vol_shock**2)/2) * df_r["TimeToExpiry"]) / (vol_shock * sqrt(df_r["TimeToExpiry"]))
            d2 = d1 - (vol_shock * sqrt(df_r["TimeToExpiry"]))
        except ZeroDivisionError:
            logger.info("Error computing option price for {}".format(df_r["ContractName"]))
            return 0
        if df_r["PutCall"] == "Call":
            bs = (fut_price_shock * norm.cdf(d1)) - (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(d2))
        elif df_r["PutCall"] == "Put":
            bs = (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(-d2)) - (fut_price_shock * norm.cdf(-d1))
        else:
            logger.info("N/A")
        #Compute the p&l of the move here
        pl = (bs - df_r["Theo"]) * df_r["Position"] * df_r["TickValue"] * df_r["Multiplier"]
        return pl

#     @staticmethod    
#     def shock_pricer_upper(df_r):
#         fut_price_upper = df_r["FuturesPrice"] + df_r["fut_shock_upper"]
#         vol_upper = df_r["ActualVolatility"] * (1 + df_r["vol_shock_upper"])
#         try:
#             d1 = (log(fut_price_upper / df_r["Strike"]) + (df_r["rate"] + (vol_upper**2)/2) * df_r["TimeToExpiry"]) / (vol_upper * sqrt(df_r["TimeToExpiry"]))
#             d2 = d1 - (vol_upper * sqrt(df_r["TimeToExpiry"]))
#         except ZeroDivisionError:
#             logger.info("Error computing option price for {}".format(df_r["ContractName"]))
#             return 0
#         if df_r["PutCall"] == "Call":
#             bs = (fut_price_upper * norm.cdf(d1)) - (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(d2))
#         elif df_r["PutCall"] == "Put":
#             bs = (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(-d2)) - (fut_price_upper * norm.cdf(-d1))
#         else:
#             logger.info("N/A")
#         #Compute the p&l of the move here
#         pl = (bs - df_r["Theo"]) * df_r["Position"] * df_r["TickValue"] * df_r["Multiplier"]
#         return pl
# 
#     @staticmethod    
#     def shock_pricer_lower(df_r):
#         fut_price_lower = df_r["FuturesPrice"] + df_r["fut_shock_lower"]
#         vol_lower = df_r["ActualVolatility"] * (1 + df_r["vol_shock_lower"])
#         try:
#             d1 = (log(fut_price_lower / df_r["Strike"]) + (df_r["rate"] + (vol_lower**2)/2) * df_r["TimeToExpiry"]) / (vol_lower * sqrt(df_r["TimeToExpiry"]))
#             d2 = d1 - (vol_lower * sqrt(df_r["TimeToExpiry"]))
#         except ZeroDivisionError:
#             logger.info("Error computing option price for {}".format(df_r["ContractName"]))
#             return 0
#         if df_r["PutCall"] == "Call":
#             bs = (fut_price_lower * norm.cdf(d1)) - (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(d2))
#         elif df_r["PutCall"] == "Put":
#             bs = (df_r["Strike"] * exp(-df_r["rate"] * df_r["TimeToExpiry"]) * norm.cdf(-d2)) - (fut_price_lower * norm.cdf(-d1))
#         else:
#             logger.info("N/A")
#         #Compute the p&l of the move here
#         pl = (bs - df_r["Theo"]) * df_r["Position"] * df_r["TickValue"] * df_r["Multiplier"]
#         return pl
    
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

class FuturesPricer(DataFramePricingModel):
    
    def __init__(self, df):
        super(NormalEuroOption, self).__init__(df)
        #Here we have the optionality to return an instance of the model
        #But if we dont want this and only wish to compute greeks individually
        #We call the static methods to compute prices
    

    @staticmethod    
    def shock_pricer_generic(df_r, fut_direction, vol_direction):
        fut_price_shock = df_r["fut_shock_{}".format(fut_direction)]
        pl = (fut_price_shock) * df_r["Position"] * df_r["TickValue"] * df_r["Multiplier"]
        return pl


