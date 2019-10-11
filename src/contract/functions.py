"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 22 Jul 2019
Author : nish

"""
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import logging

class DateFunctions:

    @staticmethod
    def add_month_code(df_r):
        mth = df_r["ExpiryDate"].month
        if mth  == 1:
            return "F"
        elif mth == 2:
            return "G"
        elif mth == 3:
            return "H"
        elif mth == 4:
            return "J"
        elif mth == 5:
            return "K"
        elif mth == 6:
            return "M"
        elif mth == 7:
            return "N"
        elif mth == 8:
            return "Q"
        elif mth == 9:
            return "U"
        elif mth == 10:
            return "V"
        elif mth == 11:
            return "X"
        elif mth == 12:
            return "Z"
    
    @staticmethod
    def add_underlying_future_month_code(df_r):
        mth = df_r["ExpiryDate"].month
        if mth  == 1:
            return "H"
        elif mth == 2:
            return "H"
        elif mth == 3:
            return "H"
        elif mth == 4:
            return "M"
        elif mth == 5:
            return "M"
        elif mth == 6:
            return "M"
        elif mth == 7:
            return "U"
        elif mth == 8:
            return "U"
        elif mth == 9:
            return "U"
        elif mth == 10:
            return "Z"
        elif mth == 11:
            return "Z"
        elif mth == 12:
            return "Z"
        
    @staticmethod
    def get_year_expiry(df_r):
        year = df_r["ExpiryDate"].year
        return str(year)[-2:]

    @staticmethod
    def add_mm_yy(df_r):
        return datetime.datetime.strftime(df_r["ExpiryDate"], "%m-%y")
    
class ContractSpecification:
    
    @staticmethod
    def add_contract_spec(df_r):
        if df_r["Symbol"] == "STERL":
            return "L"
        elif df_r["Symbol"] == "FEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3MC":
            return "K"
        elif df_r["Symbol"] == "OEU3MC2":
            return "K2"
        elif df_r["Symbol"] == "OEU3MC3":
            return "K3"
        elif df_r["Symbol"] == "OSTERL":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC":
            return "M"
        elif df_r["Symbol"] == "OSTERLMC2":
            return "M2"
        elif df_r["Symbol"] == "OSTERLMC3":
            return "M3"
        
    @staticmethod   
    def add_underlying_contract_spec(df_r):
        if df_r["Symbol"] == "STERL":
            return "L"
        elif df_r["Symbol"] == "OSTERL":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC2":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC3":
            return "L"
        elif df_r["Symbol"] == "FEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3MC":
            return "I"
        elif df_r["Symbol"] == "OEU3MC2":
            return "I"
        elif df_r["Symbol"] == "OEU3MC3":
            return "I"

    
    @staticmethod
    def add_future_contract_name(df_r):
        contract_year = "".join((df_r["UnderlyingFutureMonthCode"], df_r["UnderlyingFutureYY"]))
        contract_name = " ".join((df_r["UnderlyingFuturePCC"], contract_year, df_r["Product"]))
        return contract_name

    @staticmethod
    def add_option_contract_name(df_r):
        contract_year = "".join((df_r["MonthCode"], df_r["ExpiryYear"]))
        contract_kind = "".join((str(df_r["Strike"]), df_r["PutCall"][0]))
        contract_name = " ".join((df_r["PCC"], contract_year, contract_kind))
        return contract_name
    
    @staticmethod
    def add_underling_future_expiry_year(df_r):
        if df_r["PCC"] in ["L", "I"]:
            return datetime.datetime.strftime(df_r["ExpiryDate"], "%y")
        elif df_r["PCC"] in ["M", "K"]:
            return datetime.datetime.strftime(df_r["ExpiryDate"] + relativedelta(years=1),
                                              "%y")
        elif df_r["PCC"] in ["M2", "K2"]:
            return datetime.datetime.strftime(df_r["ExpiryDate"] + relativedelta(years=2),
                                              "%y")
        elif df_r["PCC"] in ["M3", "K3"]:
            return datetime.datetime.strftime(df_r["ExpiryDate"] + relativedelta(years=3),
                                              "%y")
                
    @staticmethod
    def gen_quarterlies(max_date):
        q = (pd.date_range(pd.to_datetime(datetime.datetime.now().date()), 
            pd.to_datetime(max_date) + pd.offsets.QuarterBegin(1), freq='Q')
                           .strftime('%m-%y')
                           .tolist())
        expiry_index = {v : "".join(("ex",str(k))) for k, v in enumerate(q, start=1)}
        return expiry_index
    
    @staticmethod
    def add_product(df_r):
        if df_r["UnderlyingFuturePCC"] == "L":
            return "sterling"
        elif df_r["UnderlyingFuturePCC"] == "I":
            return "euribor"
    
    @staticmethod
    def add_fut_expiries(df_r):
        exp_index = ContractSpecification.gen_quarterlies("2025-01-01")
        return exp_index[df_r["UnderlyingFutureMM-YY"]]
    
    @staticmethod
    def add_fut_shock_upper(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["fut"]["up"][df_r["ExpiryIndex"]]

    @staticmethod
    def add_fut_shock_lower(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["fut"]["down"][df_r["ExpiryIndex"]]

    @staticmethod
    def add_vol_shock_upper(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["vol"]["up"][df_r["ExpiryIndex"]]

    @staticmethod
    def add_vol_shock_lower(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["vol"]["down"][df_r["ExpiryIndex"]]
    
    @staticmethod
    def add_tick_value(df_r):
        if df_r["ProductName"] == "sterling":
            return 12.5
        elif df_r["ProductName"] == "euribor":
            return 25
    
    @staticmethod
    def add_multiplier(df_r):
        if df_r["Product"] in ["Option", "Future"]:
            return 1000