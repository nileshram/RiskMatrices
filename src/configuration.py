'''
Created on 22 Jul 2019

@author: Nilesh Ramnarain
'''

import json
from env.constant import CONFIG
  
class ConfigurationFactory:
      
    @staticmethod
    def create_config():
        try:
            with open(CONFIG, "r") as config:
                config_file = json.load(config)
        except IOError:
            print("Error with config filename/location please check the constant.py file")
        config_file["system"]["test_file_path"] = CONFIG
        return config_file         
