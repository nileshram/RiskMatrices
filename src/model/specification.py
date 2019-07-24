"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 20 Jul 2019
Author : nish

"""

class Specification:
    
    def __init__(self, spec):
        self.spec = spec
    
    def is_satisfied(self):
        return self.spec.is_satisfied()