# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import glob
import sys, os
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def medianNumPy(lst):
    return np.median(np.array(lst))
    
def plotColors():
    x = np.arange(10)
    ys = [i+x+(i*x)**2 for i in range(15)]
    return cm.rainbow(np.linspace(0, 1, len(ys)))

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
dataInFolders = []

for dataFolder in allDataFolders:
    dataForAnalysis = []
    dfThickness=dataFolder.ix[:,'T1_Thk(um)':'T4_Thk(um)']
    dfThickness['rowMedian'] = dfThickness.median(axis=1)
    dataForAnalysis.append(dfThickness)
    
    dfTopWidth=dataFolder.ix[:,'T1_TW(um)':'T4_TW(um)']
    dfTopWidth['rowMedian'] = dfTopWidth.median(axis=1)
    dataForAnalysis.append(dfTopWidth)
    
    dfMiddleWidth=dataFolder.ix[:,'T1_MW(um)':'T4_MW(um)']
    dfMiddleWidth['rowMedian'] = dfMiddleWidth.median(axis=1)
    dataForAnalysis.append(dfMiddleWidth)
    
    dfBottomWidth=dataFolder.ix[:,'T1_BW(um)':'T4_BW(um)']
    dfBottomWidth['rowMedian'] = dfBottomWidth.median(axis=1)
    dataForAnalysis.append(dfBottomWidth)
    
    dataInFolders.append(dataForAnalysis)

medianHigh = []
medianLow = []
folderMedianLow = []
folderMedianHigh = []

for dataInFolder in dataInFolders:
    medianLow = []
    medianHigh = []
    
    for data in dataInFolder:
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
    
    folderMedianLow.append(medianLow)
    folderMedianHigh.append(medianHigh)

dataToPlot = [folderMedianLow[0][1], folderMedianLow[1][1]]

#for result in medianLow:
#    dataToPlot.append(result)

box = plt.boxplot(dataToPlot, notch=True, patch_artist=True)

for patch, color in zip(box['boxes'], plotColors()):
    patch.set_facecolor(color)

plt.show()


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
#    for whisker in bp['whiskers']:
#        whisker.set(color='red', linewidth=2)
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
#ax.set_xticklabels(['Thickness', 'TopWidth', 'MiddleWidth', 'BottomWidth'])
### Remove top axes and right axes ticks
#ax.get_xaxis().tick_bottom()
#ax.get_yaxis().tick_left()