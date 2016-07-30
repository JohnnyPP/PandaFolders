import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json

def medianNumPy(lst):
    return np.median(np.array(lst))
    
def plotColors():
    x = np.arange(10)
    ys = [i+x+(i*x)**2 for i in range(15)]
    return cm.rainbow(np.linspace(0, 1, len(ys)))

# Readng data

path = os.path.abspath(os.path.dirname(__file__))
dataPath = '/data'
dataFolder = path + dataPath
dataFolders = os.listdir(dataFolder)
print 'Script path: ' + path
print 'Data path: ' + dataFolder
print 'Subfolders in data path:'

for i, folder in enumerate(dataFolders):
    print(i, folder)

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
etchingFactor = pd.DataFrame(columns=['Thickness', 'BottomWidth', 'TopWidth', 'rowMedian'])

for dataFolder in allDataFolders:
    dataForAnalysis = []
    dfThickness=dataFolder.ix[:,'T1_Thk(um)':'T4_Thk(um)']
    dfThickness['rowMedian'] = dfThickness.median(axis=1)
    etchingFactor['Thickness'] = dfThickness.median(axis=1)
    dataForAnalysis.append(dfThickness)
    
    dfTopWidth=dataFolder.ix[:,'T1_TW(um)':'T4_TW(um)']
    dfTopWidth['rowMedian'] = dfTopWidth.median(axis=1)
    etchingFactor['TopWidth'] = dfTopWidth.median(axis=1)
    dataForAnalysis.append(dfTopWidth)
    
    dfMiddleWidth=dataFolder.ix[:,'T1_MW(um)':'T4_MW(um)']
    dfMiddleWidth['rowMedian'] = dfMiddleWidth.median(axis=1)
    dataForAnalysis.append(dfMiddleWidth)
    
    dfBottomWidth=dataFolder.ix[:,'T1_BW(um)':'T4_BW(um)']
    dfBottomWidth['rowMedian'] = dfBottomWidth.median(axis=1)
    etchingFactor['BottomWidth'] = dfBottomWidth.median(axis=1)
    dataForAnalysis.append(dfBottomWidth)

    # etchingFactor = 2*Thickness/(BottomWidth - TopWidth)
    etchingFactor['rowMedian'] = 2*etchingFactor['Thickness']/(etchingFactor['BottomWidth'] - etchingFactor['TopWidth'])

    dataForAnalysis.append(etchingFactor)   
    dataInFolders.append(dataForAnalysis)
    
# Processing

medianHigh = []
medianLow = []
resultsMedianLow = []
resultsMedianHigh = []

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
    
    resultsMedianLow.append(medianLow)
    resultsMedianHigh.append(medianHigh)

# Plotting

eThickness, eTopWidth, eMiddleWidth, eBottomWidth, eEtchingFactor= range(0, 5)
yLabel = ['Thickness', 'Top width', 'Middle width', 'Bottom width', 'Etching factor']

print resultsMedianLow

with open('median4High.json', 'w') as f:
     json.dump(resultsMedianHigh, f)

# resultsList[index of the folder name][index of the faeture to display]

for i in range(0, len(yLabel)):
    dataToPlot = [resultsMedianHigh[0][i], resultsMedianHigh[1][i], resultsMedianHigh[2][i]]
    plt.figure()
    box = plt.boxplot(dataToPlot, notch=True, patch_artist=True)
    
    for patch, color in zip(box['boxes'], plotColors()):
        patch.set_facecolor(color)
    
    plt.xticks([1, 2, 3], [dataFolders[0], dataFolders[1], dataFolders[2]])
    plt.ylabel(yLabel[i])

plt.show()