'''Copyright 2013 Evan A. Parker

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.'''

import math
from PIL import Image


csv3FileName = "CSV_5_HRP_control_filtered-WITH-INTENSITY.csv"
imageResourcesFolderName = "plantGlycanImages"

reduceCompositionListToSingleSpecies = True
drawOglycans = False
sortSiteAbundanceByIntensity = False

#import libraries
import csv

##          ##
## read CSV ##
##          ##
inputFile = open(csv3FileName, 'r')
csvInputFileTemp = csv.reader(inputFile, dialect='excel')
csvInputFile = []
for row in csvInputFileTemp:
    csvInputFile.append(row)

#find headers
row = 0
notFoundHeaders = True
while notFoundHeaders:
    if csvInputFile[row][0] == "Feature No.":
        print("found")
        csvHeaders = csvInputFile[row]
        notFoundHeaders = False
        row += 1
    else:
        print("not found")
        print(row)
        row += 1

#
#compose list of desired headers and assign the list values
#
indexDict = {"GP Actual Mass":0,
             "RT":0,
             "Hex":0,
             "HexNAc":0,
             "DeoxyHex":0,
             "Sialic Acid (Neu5Ac and Neu5Gc)":0,
             "Nonstandard Glycan Components":0,
             "Glycosylation Site Position":0,
             "Mass Match Intensity":0}
for i in range(len(csvHeaders)):
    for index in indexDict:
        if csvHeaders[i] == index:
            indexDict[index] = i
            
siteCompositionLibrary = {}
siteAbundanceLibrary = {}
       
while row < len(csvInputFile):
    newCompound = [""]
    rt = csvInputFile[row][indexDict["RT"]]
    mass = csvInputFile[row][indexDict["GP Actual Mass"]]
    
    #generate name
    site = csvInputFile[row][indexDict["Glycosylation Site Position"]]
    hex = csvInputFile[row][indexDict["Hex"]]
    hexNac = csvInputFile[row][indexDict["HexNAc"]]
    DeoxyHex = csvInputFile[row][indexDict["DeoxyHex"]]
    sialicAcid = csvInputFile[row][indexDict["Sialic Acid (Neu5Ac and Neu5Gc)"]]
    nonstandard = csvInputFile[row][indexDict["Nonstandard Glycan Components"]]
    intensity = csvInputFile[row][indexDict["Mass Match Intensity"]]
    if "entose" in nonstandard:
        nonstandard = "1"
    else:
        nonstandard = "0"
    compositionTuple = (int(hex), int(hexNac), int(DeoxyHex), int(sialicAcid), int(nonstandard))
    
    if site in siteCompositionLibrary and not reduceCompositionListToSingleSpecies:
        siteCompositionLibrary[site].append(compositionTuple)
        siteAbundanceLibrary[site].append(float(intensity))
        
    elif site in siteCompositionLibrary and reduceCompositionListToSingleSpecies:
        if compositionTuple in siteCompositionLibrary[site]:
            compIndex = siteCompositionLibrary[site].index(compositionTuple)
            siteAbundanceLibrary[site][compIndex] += float(intensity)
        else:
            siteCompositionLibrary[site].append(compositionTuple)
            siteAbundanceLibrary[site].append(float(intensity))
        
    else:
        siteCompositionLibrary[site] = [compositionTuple]
        siteAbundanceLibrary[site] = [float(intensity)]
        
    row += 1
            



def arrangeInBlock(site, compositions, abundances, drawOglycans):
    
    #re-sort
    pairs = []
    for i in range(len(compositions)):
        AbundCompPair = (-1*abundances[i], compositions[i])
        pairs.append(AbundCompPair)
    pairs.sort()
    
    compositions = []
    abundances = []
    for pair in pairs:
        compositions.append(pair[1])
        abundances.append(-1*pair[0])
        
    
    
    # import glycan images
    glycanCompositions = [[str(x) for x in glyTuple] for glyTuple in compositions]
    glycanImageFilenames = [imageResourcesFolderName+ "/" + '-'.join(comp) + ".png" for comp in glycanCompositions]
    glycanImagesToArrange = [Image.open(filename) for filename in glycanImageFilenames]
    
    #normalise abundances
    sumAbund = float(sum(abundances))
    abundancesNorm = [100*abund/sumAbund for abund in abundances]
    
    #import composition images
    sizes = [100, 99, 95, 90, 80, 75, 70, 60, 50, 40, 30, 25, 20, 10, 5, 2, 1]
    orderedAbundancesToArrange = []
    for abundance in abundancesNorm:
        diff = [abs(abundance - size) for size in sizes]
        diffIdx = diff.index(min(diff))
        diffFileName = imageResourcesFolderName + "/" + str(sizes[diffIdx]) + "ppc.png"
        orderedAbundancesToArrange.append(Image.open(diffFileName))
        
    
    if drawOglycans:
        quantAdjustment = 40
    else:
        quantAdjustment = 10
    largestWidth = max(img.size[0] for img in glycanImagesToArrange)
    largestHeight = max(img.size[1] for img in glycanImagesToArrange) + quantAdjustment
    
    count = len(glycanImagesToArrange)
    if count < 6:
        glycansImageWidth = count
        modForImageGrid = 0
    else:
        mod6 = count%6
        mod5 = count%5
        maxMod = max(mod5, mod6)
        if maxMod == mod5:
            glycansImageWidth = 5
            modForImageGrid = mod5
        else:
            glycansImageWidth = 6
            modForImageGrid = mod6
    
    heightModifer = 0
    if modForImageGrid != 0:
        heightModifer = 1
            
    height = int(count/glycansImageWidth) + heightModifer 
    
    imgHeight = height*largestHeight
    imgWidth = glycansImageWidth*largestWidth
    
    masterImage = Image.new("RGB", (imgWidth,imgHeight), (255,255,255))
    #imgWidth, imgHeight = masterImage.size #redundant
   
    
    #arranges 
    halfStep = int(largestWidth/2.0)
    for i in range(len(glycanImagesToArrange)):
        imgDrop = largestHeight*(int(i/float(glycansImageWidth))+1) - quantAdjustment - glycanImagesToArrange[i].size[1]
        
        #checks if image is in the main grid (True) or in the last several (False)
        if i < (len(glycanImagesToArrange)-modForImageGrid):
            stepPosition = halfStep - int(glycanImagesToArrange[i].size[0]/2.0)
            imgStep = stepPosition + largestWidth*(i%glycansImageWidth)
        
        #equally spaces the last several images
        else:
            tempStep = int(imgWidth/float(modForImageGrid))
            largeImageRemainder = imgWidth - (tempStep*(modForImageGrid-1) + largestWidth)
            beginSpace = int(largeImageRemainder/2.0) + halfStep
            imgStep = beginSpace + tempStep*(i%modForImageGrid) - int(glycanImagesToArrange[i].size[0]/2.0)
        
        curImg = glycanImagesToArrange[i]
        print(imgDrop,imgStep)
        pos = (imgStep, imgDrop)
        masterImage.paste(curImg, pos)
        
    for i in range(len(orderedAbundancesToArrange)):
        imgDrop = largestHeight*(int(i/float(glycansImageWidth))+1) - orderedAbundancesToArrange[i].size[1]
        
        #checks if image is in the main grid (True) or in the last several (False)
        if i < (len(orderedAbundancesToArrange)-modForImageGrid):
            stepPosition = halfStep - int(orderedAbundancesToArrange[i].size[0]/2.0)
            imgStep = stepPosition + largestWidth*(i%glycansImageWidth)
        
        #equally spaces the last several images
        else:
            tempStep = int(imgWidth/float(modForImageGrid))
            largeImageRemainder = imgWidth - (tempStep*(modForImageGrid-1) + largestWidth)
            beginSpace = int(largeImageRemainder/2.0) + halfStep
            imgStep = beginSpace + tempStep*(i%modForImageGrid) - int(orderedAbundancesToArrange[i].size[0]/2.0)
        
        curImg = orderedAbundancesToArrange[i]
        print(imgDrop,imgStep)
        pos = (imgStep, imgDrop)
        masterImage.paste(curImg, pos)
    masterImageName = str(site) + "-figure.png"
    masterImage.save(masterImageName)


for site in siteCompositionLibrary:
    compositionList = siteCompositionLibrary[site]
    abundanceList = siteAbundanceLibrary[site]
    arrangeInBlock(site, compositionList, abundanceList, drawOglycans)

plottingList = []
for site, intens in siteAbundanceLibrary.iteritems():
    plottingList.append((site,sum(intens)))

if sortSiteAbundanceByIntensity:
    plottingList.sort(key = lambda x: -1*x[1])
else:
    plottingList.sort(key = lambda x: int(x[0]))
siteList, intenList = zip(*plottingList)

import numpy as np
import matplotlib.pyplot as plt


N = len(siteList)
menMeans   = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)
menStd     = (2, 3, 4, 1, 2)
womenStd   = (3, 5, 2, 3, 3)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, intenList,   width, color='b')

plt.ylabel('Intensity')
plt.title('Site vs MS Intensity')
plt.xticks(ind+width/2., siteList )

plt.show()
