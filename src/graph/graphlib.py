'''
Created on 11 Feb 2020

@author: anant.srivastava
'''

import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib
#comment the following line to show heatplots visbly
matplotlib.use('Agg')
import numpy as np
from graph.graph_properties import MidpointNormalize

class GraphEngine:
    
    def plot_heatmap(self, graph_model):
        #commented for new size
        #self.size = 12
        self.size = 6
        self.fig, self.ax = plt.subplots()
        cm = mplc.LinearSegmentedColormap.from_list("", ["red","white","green"])
        
        # Get the midpoint of the colormap here
        vals = np.array(graph_model)
        vmin = vals.min()
        vmax = vals.max()
        norm = MidpointNormalize(vmin=vmin, vmax=vmax, midpoint=0)
        
        #attempt to plot image
        try:
            im = self.ax.imshow(graph_model, cmap=cm, norm=norm)
        except TypeError:
            return None
        
        # Display all of the ticks
        self.ax.set_xticks(np.arange(self.size))
        self.ax.set_yticks(np.arange(self.size))
        # Label each of the x/y tick labels
        self.ax.set_xticklabels(["-", "-", 0, 0, "+", "+"])
        self.ax.set_yticklabels(["-", "-", 0, 0, "+", "+"][::-1])
        
#         #12 bucket size
#         self.ax.set_xticklabels(["-", "-", "-", "-", "-", 0, 0, "+", "+", "+", "+", "+"])
#         self.ax.set_yticklabels(["-", "-", "-", "-", "-", 0, 0, "+", "+", "+", "+", "+"][::-1])
                
        self.ax.set_xlabel("Futures step")
        self.ax.set_ylabel("Volatility")
        
        # Loop over data dimensions and create text annotations.
        for i in range(self.size):
            for j in range(self.size):
                try:
                    text = self.ax.text(j, i, int(round(graph_model[i, j]/1000, 0)),
                                   ha="center", va="center", color="black",
                                   size=12, fontweight='bold')
                except IndexError:
                    continue
        self.ax.set_title("P&L Portfolio Heatmap ('000s)")
        self.fig.colorbar(im)
        #uncomment this line to show the heatplots visibly locally
#         plt.show()
        return self.fig
