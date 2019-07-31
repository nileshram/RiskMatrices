"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 22 Jul 2019
Author : nish

"""
import datetime
import pandas as pd

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
    def get_year_expiry(df_r):
        year = df_r["ExpiryDate"].year
        return str(year)[-2:]
    
    @staticmethod
    def add_month_year(df_r):
        mm_yy = df_r["ExpiryDate"].strftime("%m-%y")
        return mm_yy
    
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
    def add_future_contract_name(df_r):
        contract_year = "".join((df_r["MonthCode"], df_r["ExpiryYear"]))
        contract_name = " ".join((df_r["PCC"], contract_year, df_r["Product"]))
        return contract_name

    @staticmethod
    def add_option_contract_name(df_r):
        pass
    
    @staticmethod
    def add_underlying_future(df_r):
        if df_r["ExpiryDate"].month % 3 == 0:
            return datetime.datetime.strftime(df_r["ExpiryDate"], "%m-%y")
        elif df_r["ExpiryDate"].month % 3 == 1:
            return "-".join((str(df_r["ExpiryDate"].month + 2), 
                            str(df_r["ExpiryDate"].year)[-2:]))
        elif df_r["ExpiryDate"].month % 3 == 2:
            return "-".join((str(df_r["ExpiryDate"].month + 1), 
                            str(df_r["ExpiryDate"].year)[-2:]))
    
    @staticmethod
    def gen_quarterlies(max_date):
        q = (pd.date_range(pd.to_datetime(datetime.datetime.now().date()), 
            pd.to_datetime(max_date) + pd.offsets.QuarterBegin(1), freq='Q')
                           .strftime('%m-%y')
                           .tolist())
        expiry_index = {v : "".join(("ex",str(k))) for k, v in enumerate(q, start=1)}
        return expiry_index
    
    @staticmethod
    def add_fut_expiries(df_r):
        exp_index = ContractSpecification.gen_quarterlies("2025-01-01")
        return exp_index[df_r["MM-YY"]]
    


    