'''
Created on 30 May 2019

@author: nilesh
'''

import sys
import os

module_path = os.path.join(os.path.dirname(os.path.dirname(str(__file__))), "src")

if module_path not in sys.path:
    sys.path.append(module_path)
