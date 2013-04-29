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
#define input
chromatogramFileName = "HRP_cleaned.CSV"


#imports
import matplotlib.pyplot as plt
from math import sqrt


#import chromatogram names
chromatogramFile = open(chromatogramFileName, 'r')
chromatogramTimeIntensityList = []
for line in chromatogramFile:
    if line[0] == "#" or len(line) < 3:
        continue 
    else:
        time, intensity = line.split(",")[1:]
        time, intensity = float(time), float(intensity)
        chromatogramTimeIntensityList.append((time,intensity))
timeList, intensityList = zip(*chromatogramTimeIntensityList)


compoundsTime = [9.48415, 12.12495, 12.15826667, 12.63178333, 13.00073333, 13.32195, 13.43303333,
                13.46635, 13.70683333, 14.0256, 14.23343333, 14.27666667, 14.42561667, 14.45965, 
                14.59673333, 14.8657, 15.19943333, 15.79695, 15.83026667, 15.88966667, 15.99233333, 16.42835, 
                16.51211667, 16.59265, 16.6641, 17.49545, 17.88721667, 17.94296667, 17.94983333, 18.3766, 
                18.6484, 19.0237, 19.17233333, 19.29883333, 19.36668333, 20.31423333, 20.77405, 21.23871667, 
                21.63455, 22.18556667, 22.21831667, 22.29403333, 22.40125, 23.14806667, 24.79771667, 24.80935, 
                25.04578333, 26.76058333, 27.48026667]
compoundsTime = [t+0.2 for t in compoundsTime]
compoundsInten = [14443, 10767, 18726, 41104, 38672, 90220, 25903, 14384, 19667, 31005, 63420, 110485, 
                1944261, 31751, 187545, 120975, 113425, 23768, 69692, 214842, 188310, 235836, 392017, 
                152847, 150980, 45553, 42352, 1257708, 137919, 43295, 302226, 501044, 526671, 268310, 
                139510, 238617, 288849, 354376, 101532, 65998, 152504, 3184394, 333137, 291747, 884479, 
                108341, 278688, 43830, 211814]
compoundsInten = [float(a)*0.6 for a in compoundsInten]
compoundIntenZeroes = [0 for a in compoundsInten]
                

plt.plot(timeList, intensityList, 'k-')
plt.vlines(compoundsTime,compoundIntenZeroes,compoundsInten, color='b', lw=2.0)
plt.show()
