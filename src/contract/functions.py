"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 22 Jul 2019
Author : nish

"""
import datetime

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
    
class Expiries:
     
    @staticmethod
    def build_quarterly_expiries(df_r):
        TODAY = datetime.datetime.now()
        cur_month = TODAY.month
        pass
    
    @staticmethod
    def _build_date_str(dt):
        return "-".join((str(dt.month), str(dt.year[-2:])))


