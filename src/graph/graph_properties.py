'''
Created on 11 Feb 2020

@author: anant.srivastava
'''

import matplotlib.colors as mplc
import numpy as np
import scipy as sp


class MidpointNormalize(mplc.Normalize):

    """
    Class docs: Auxihillary module from github to add a midpoint normalise
    to a color scale in a heatplot in matplotlib
    """

    def __init__(self, vmin, vmax, midpoint=0, clip=False):
        self.midpoint = midpoint
        mplc.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
        return np.ma.masked_array(sp.interp(value, x, y))