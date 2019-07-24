'''
Created on 24 Jul 2019

@author: nish
'''

import pandas as pd
from env.constant import RISK
from contract.functions import DateFunctions

class FileManager:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_csv_data():
        df = pd.read_csv(RISK)
        clean_df = FileManager._remove_duplicates_rows(df)
        return clean_df
    
    @staticmethod
    def _remove_duplicates_rows(dataframe):
        dataframe.drop_duplicates(inplace=True)
        return dataframe
    
    
    