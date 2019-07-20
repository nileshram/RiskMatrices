"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 18 Jul 2019
Author : nish

"""
import pandas as pd
from math import sqrt, pi, exp, log
from scipy.stats import norm
from pricing.dataframemodel import NormalEuroOption


path = "/home/nish/live_risk_matrices/se_static2.csv"

df = pd.read_csv(path)
df = df[df["Name"] == "OEU3MC2 Dec Option"]
df["type"] = [r[:1].lower() for r in df["PutCall"]]
df["fut_px"] = [100.4175 for _ in df["PutCall"]]
df["rate"] = [0 for _ in df["PutCall"]]
df["bs_theo"] = df.apply(NormalEuroOption.price, axis=1)
#df = df[["Theo", "bs_theo"]]
#add new columns
print(df)
