'''
Created on 22 Jul 2019

@author: Nilesh Ramnarain
'''

import json
from env.constant import CONFIG, RISK, LOG
  
class ConfigurationFactory:
      
    @staticmethod
    def create_config(name=None):
        config = {"LOG" : LOG, "RISK" : CONFIG}
        try:
            with open(config[name], "r") as config:
                config_file = json.load(config)
        except IOError:
            print("Error with config filename/location please check the constant.py file")
        return config_file      
