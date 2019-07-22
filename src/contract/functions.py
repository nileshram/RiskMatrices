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

#aim is to build all of the expiries from
#todays date in the format MM-YY
#mm-yy : ex1,    
    @staticmethod
    def build_expiries(df_r):

        pass
    
now = datetime.datetime.now()
print(now.month)


