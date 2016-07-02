# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy 
import pandas as pd
import glob
import sys, os
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from pylab import plot, show, savefig, xlim, figure, \
                hold, ylim, legend, boxplot, setp, axes
          
#path = "L:\\ale\\substrate_core\\35 Etching Trials\\Misch-d"   # gets the path automatically   
path = os.path.dirname(sys.argv[0]) 

def medianNumPy(lst):
    return numpy.median(numpy.array(lst))

#glob.glob('/Misch-d_*.csv')
allFiles = glob.glob(path + "/Misch-d_*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
MischD = pd.concat(list_)


Thk=MischD.ix[:,'T1_Thk(um)':'T4_Thk(um)']
Thk['median'] = Thk.median(axis=1)

Twid=MischD.ix[:,'T1_TW(um)':'T4_TW(um)']
Twid['median'] = Twid.median(axis=1)

middleW=MischD.ix[:,'T1_MW(um)':'T4_MW(um)']
middleW['median'] = middleW.median(axis=1)

bottomW=MischD.ix[:,'T1_BW(um)':'T4_BW(um)']
bottomW['median'] = bottomW.median(axis=1)

median = Twid['median']

medianLenght = len(median)

medianSliced = []
medianSlicedLow = []    # this stores first 4 values (approx 40)
medianSlicedHigh = []   # this stores next 4 values (approx 60)
median4High = []
median4Low = []



for i in xrange(0,medianLenght,4):
    medianSliced.append(median[i:4+i])

for i in range(0,len(medianSliced)):
    if i % 2 == 0:
        medianSlicedLow.append(medianSliced[i])
        median4Low.append(medianNumPy(medianSliced[i]))
    else:
        medianSlicedHigh.append(medianSliced[i])
        median4High.append(medianNumPy(medianSliced[i]))
        
#ta = np.concatenate((median4High, median4Low), 0)

data_to_plot = [median4Low,median4High,median4Low]

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(data_to_plot)
bp = ax.boxplot(data_to_plot, patch_artist=True)
## change outline color, fill color and linewidth of the boxes
for box in bp['boxes']:
    # change outline color
    box.set( color='plum', linewidth=2)
    # change fill color
    box.set( facecolor = 'plum' )
    
for box in bp['boxes']:
    
    ## change color and linewidth of the whiskers
 for whisker in bp['whiskers']:
    whisker.set(color='red', linewidth=2)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='green', linewidth=2)
    ## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='#b2df8a', linewidth=2)


## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='#e7298a', alpha=0.5)
    ## Custom x-axis labels
ax.set_xticklabels(['2Mil', '3Mil'])
## Remove top axes and right axes ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()