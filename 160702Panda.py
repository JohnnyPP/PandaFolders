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
           
path = os.path.dirname(sys.argv[0]) 
dataPath = '/data'
dataFolder = path + dataPath
dataFolders = os.listdir(dataFolder)

dataList = []
allDataFolders = []

for i, folder in enumerate(dataFolders):
    dataList = []
    dataFiles = glob.glob(dataFolder + "/" + folder + "/*.csv")
    for dataFile in dataFiles:
        dataFrame = pd.read_csv(dataFile, index_col=None, header=0)
        dataList.append(dataFrame)
    allDataFolder = pd.concat(dataList)
    allDataFolders.append(allDataFolder)


dataForAnalysis = []

dfThickness=allDataFolder.ix[:,'T1_Thk(um)':'T4_Thk(um)']
dfThickness['rowMedian'] = dfThickness.median(axis=1)
dataForAnalysis.append(dfThickness)

dfTopWidth=allDataFolder.ix[:,'T1_TW(um)':'T4_TW(um)']
dfTopWidth['rowMedian'] = dfTopWidth.median(axis=1)
dataForAnalysis.append(dfTopWidth)

dfMiddleWidth=allDataFolder.ix[:,'T1_MW(um)':'T4_MW(um)']
dfMiddleWidth['rowMedian'] = dfMiddleWidth.median(axis=1)
dataForAnalysis.append(dfMiddleWidth)

dfBottomWidth=allDataFolder.ix[:,'T1_BW(um)':'T4_BW(um)']
dfBottomWidth['rowMedian'] = dfBottomWidth.median(axis=1)
dataForAnalysis.append(dfBottomWidth)

medianHigh = []
medianLow = []

def medianNumPy(lst):
    return numpy.median(numpy.array(lst))

for data in dataForAnalysis:
    medianSliced = []
    medianSlicedLow = []    # this stores first 4 values (approx 40)
    medianSlicedHigh = []   # this stores next 4 values (approx 60)
    median4High = []
    median4Low = []

    for i in xrange(0,len(data['rowMedian']),4):
        medianSliced.append(data['rowMedian'][i:4+i])
    
    for i in range(0,len(medianSliced)):
        if i % 2 == 0:
            medianSlicedLow.append(medianSliced[i])
            median4Low.append(medianNumPy(medianSliced[i]))
        else:
            medianSlicedHigh.append(medianSliced[i])
            median4High.append(medianNumPy(medianSliced[i]))
    
    medianLow.append(median4Low)
    medianHigh.append(median4High)
    



        
        
        
        
#ta = np.concatenate((median4High, median4Low), 0)





#data_to_plot = [median4Low,median4High,median4Low]
#
#fig = plt.figure(1, figsize=(9, 6))
#ax = fig.add_subplot(111)
#bp = ax.boxplot(data_to_plot)
#bp = ax.boxplot(data_to_plot, patch_artist=True)
### change outline color, fill color and linewidth of the boxes
#for box in bp['boxes']:
#    # change outline color
#    box.set( color='plum', linewidth=2)
#    # change fill color
#    box.set( facecolor = 'plum' )
#    
#for box in bp['boxes']:
#    
#    ## change color and linewidth of the whiskers
# for whisker in bp['whiskers']:
#    whisker.set(color='red', linewidth=2)
#
### change color and linewidth of the caps
#for cap in bp['caps']:
#    cap.set(color='green', linewidth=2)
#    ## change color and linewidth of the medians
#for median in bp['medians']:
#    median.set(color='#b2df8a', linewidth=2)
#
#
### change the style of fliers and their fill
#for flier in bp['fliers']:
#    flier.set(marker='o', color='#e7298a', alpha=0.5)
#    ## Custom x-axis labels
#ax.set_xticklabels(['2Mil', '3Mil'])
### Remove top axes and right axes ticks
#ax.get_xaxis().tick_bottom()
#ax.get_yaxis().tick_left()