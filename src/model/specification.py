"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 20 Jul 2019
Author : nish

"""
from abc import abstractmethod, ABCMeta

class Specification:
    
    def __init__(self, spec):
        self.spec = spec
    
    def is_satisfied(self):
        return self.spec.is_satisfied()
    

class STIRs(metaclass=ABCMeta):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def apply_curve_classification(self, symbol):
        pass
    
    @abstractmethod
    def apply_underlying_future_classification(self, exp_date):
        pass

class Euribor(STIRs):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply_curve_classification(self, symbol):
        if symbol == "0EU3":
            return "I"
        elif symbol == "0EU3MC":
            return "K"
        elif symbol == "0EU3MC2":
            return "K2"
        elif symbol == "0EU3MC3":
            return "K3"
        else:
            return "N/A"
        
    @staticmethod
    def apply_underlying_future_classification(self, symbol):
        pass