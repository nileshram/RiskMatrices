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
df = df[(df["Product"] == "Future") & (df["Symbol"] == "STERL")]
df["ExpiryDate"] = pd.to_datetime(df["ExpiryDate"])
df["MonthCode"] = df.apply(lambda x: DateFunctions.add_month_code(x), axis=1)
df["ExpiryYear"] = df.apply(lambda x: DateFunctions.get_year_expiry(x), axis=1)
print(df)
