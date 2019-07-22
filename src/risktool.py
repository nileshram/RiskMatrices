"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 18 Jul 2019
Author : nish

"""
import pandas as pd
from pricing.dataframemodel import NormalEuroOption
from contract.functions import DateFunctions
from env.constant import RISK


df = pd.read_csv(RISK)
df.drop_duplicates(inplace=True) #cleans out the dataset and removes duplicates
df = df[(df["Product"] == "Future") & (df["Symbol"] == "STERL") & (df["Position"] != 0)]
df["ExpiryDate"] = pd.to_datetime(df["ExpiryDate"])
df["MonthCode"] = df.apply(lambda x: DateFunctions.add_month_code(x), axis=1)
df["ExpiryYear"] = df.apply(lambda x: DateFunctions.get_year_expiry(x), axis=1)
df["MM-YY"] = df.apply(lambda x: DateFunctions.add_month_year(x), axis=1)
df.sort_values(by="ExpiryDate", inplace=True, ascending=True)
print(df)
