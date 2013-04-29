'''Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.'''
   
#               #
# configuration #
#               #

csv5FileName = "CSV_5_HRP_residue_filtered.csv"
compoundResultsFileName = "residue_intensitites.csv"


ppmError = 20
rtErrorMins = 1

intensityKey = "Height"

#            #
# end config #
#            #


#import libraries
import csv


##                   ##
## read compound CSV ##
##                   ##
inputFile = open(csv5FileName, 'r')
csvInputFileTemp = csv.reader(inputFile, dialect='excel')
csvInputFile = []
for row in csvInputFileTemp:
    if len(row) >= 2:
        csvInputFile.append(row)



#find headers
row = 0
notFoundHeaders = True
while notFoundHeaders:
    if len(csvInputFile[row]) > 0 and csvInputFile[row][0] == "Feature No.":
        csvHeaders = csvInputFile[row]
        notFoundHeaders = False
        outputOrder = csvHeaders
        row += 1
    else:
        row += 1
        
#make compound dictionary List
compoundList = []
while row < len(csvInputFile):
    newCompoundDict = {}
    for i in range(len(csvInputFile[row])):
        newCompoundDict[csvHeaders[i]] = csvInputFile[row][i]
    newCompoundDict["Mass Match Intensity"] = 0
    compoundList.append(newCompoundDict)
    row += 1
    
##                  ##
## read results CSV ##
##                  ##
inputFile = open(compoundResultsFileName, 'r')
csvInputFileTemp = csv.reader(inputFile, dialect='excel')
csvInputFile = []
for row in csvInputFileTemp:
    if len(row) >= 2:
        csvInputFile.append(row)

csvHeaders = csvInputFile.pop(0)

foundCompoundList = []
row = 0
while row < len(csvInputFile):
    newCompoundDict = {}
    for i in range(len(csvInputFile[row])):
        newCompoundDict[csvHeaders[i]] = csvInputFile[row][i]
    newCompoundDict["notUsedYet"] = True
    foundCompoundList.append(newCompoundDict)
    row += 1
        
##              ##
## compare two  ##
##              ##

ppmError = 4*float(ppmError)/1000000
ppmNeg = 1.0 - ppmError
ppmPos = 1.0 + ppmError
rtErrorMins = float(rtErrorMins)

print len(compoundList)
print len(foundCompoundList)

for i in range(len(compoundList)):
    realRT = float(compoundList[i]["RT"])
    realMass = float(compoundList[i]["GP Actual Mass"])
    for found in foundCompoundList:
        rtPotential = float(found["RT"])
        massPotential = float(found["Mass"])
        rtMatch = False
        massMatch = False
        #print("rtpotential, rtReal = %f, %f"%(rtPotential, realRT))
        #print("masspotential, massReal = %f, %f"%(massPotential,realMass))
        if rtPotential-rtErrorMins <= realRT <= rtPotential+rtErrorMins:
            rtMatch = True
        if massPotential*ppmNeg <= realMass <= massPotential*ppmPos:
            massMatch = True
        if rtMatch and massMatch and found["notUsedYet"]:
            compoundList[i]["Mass Match Intensity"] += float(found[intensityKey])
            print("updating intensity, mass, potential mass = %f, %f"%(realMass,massPotential) )
            found["notUsedYet"] = False
            


csv5_with_intensitiy_name = csv5FileName[:-4] + "-WITH-INTENSITY.csv" 

#write file
with open(csv5_with_intensitiy_name, 'w') as csvfile:
    compoundCsvWriter = csv.writer(csvfile, lineterminator="\n")
    compoundCsvWriter.writerow(outputOrder)
    for compoundDict in compoundList:
        listStyleCompound = []
        for outputKey in outputOrder:
            listStyleCompound.append(str(compoundDict[outputKey]))
        compoundCsvWriter.writerow(listStyleCompound)