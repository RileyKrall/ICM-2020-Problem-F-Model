# -*- coding: utf-8 -*-
"""
CWU modeling team for the Interdiciplinery Competition in Modeling, Problem F

Model of land change of islands. 
Converts grey-scale heghtmap image to CSV, then calculates yearly precent
change of land.

Model created during a 4 day project, accompanied paper presents results found
and the rest of the model to solve the problem.
"""
from plotly.offline import plot
from IPython.display import Image
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import PIL as pil
import plotly.io as pio
import csv

#Create new island with changed heights with respect to new sea level
def raiseSeaLevel(island, change):
    changedIsland = island.copy()
    
    for indexi, Data in changedIsland.iterrows():
        for indexj, value in Data.items():
            newVal = value - change
            if newVal < 0:
                newVal = 0
            changedIsland.at[indexi, indexj] = newVal
            
    return changedIsland

#Count total land in area
def getLandCount(island):
    count = 0
    for indexi, Data in island.iterrows():
        for indexj, value in Data.items():
            if value != 0:
                count += 1
    return count

def getLandDangerZone(island, zoneMax):
    count = 0
    for indexi, Data in island.iterrows():
        for indexj, value in Data.items():
            if value > 0 and value <= zoneMax:
                count += 1
    return count

#Display island
def plotIsland(island, fileTitle, plotTitle, saveLoc):
    fig = go.Figure(data=[go.Surface(z=island.values)])
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
    fig.update_layout(title=plotTitle, autosize=False,
                  scene_camera_eye=dict(x=2, y=1, z=0.64),
                  scene = dict(
                          xaxis = dict(nticks=4, range=[0, 1000]),
                          yaxis = dict(nticks=4, range=[0, 1000]),
                          zaxis = dict(nticks=4, range=[0, 10]),),
                  width=750, height=750,
                  margin=dict(l=65, r=50, b=65, t=90))
    
    pio.write_image(fig, file=saveLoc+fileTitle+".png", format='png')
    #plot(fig)

#Main runner of model. Calculates change in island every year
def IslandModel(island, seaLevelChanges, stormSurgeRisk, cutOffSeaLevel, startingYear, runTitle, fileTitle, saveLoc):
    print(runTitle)
    
    with open(saveLoc + fileTitle + '.csv', 'w', newline='') as file:
        #Data storage and prepping
        fileWriter = csv.writer(file)
        seaLevel = 0
        initialLandCount = getLandCount(island)
        yearCount = startingYear
        for change in seaLevelChanges:
            #convert mm to m
            convertChange = change*0.001
            #Raise sea level
            seaLevel = convertChange
            #Create changed island
            changedIsland = raiseSeaLevel(island, convertChange)
            #Land Counting
            changedIslandLand = getLandCount(changedIsland)
            percentChangedFromTotal = (changedIslandLand/initialLandCount)*100
                        
            #Get danger zone count
            landInDZ = getLandDangerZone(changedIsland, stormSurgeRisk)
            ratioLandToDZ = (landInDZ/changedIslandLand)*100            
            
            #Increment year
            yearCount += 1
            #Prep next iteration
            #prevIterationIsland = changedIsland.copy()
            
            #Print and write results
            print("Year: " + str(yearCount) + "    Total landmass percent from original: " + str(percentChangedFromTotal) + "    Current land in the danger zone: " + str(ratioLandToDZ) + "%")
            fileWriter.writerow([str(yearCount), str(percentChangedFromTotal), str(ratioLandToDZ)])
            
            #Plot surface every n years
            if ((yearCount - 2000) % 10 == 0):
                plotIsland(changedIsland, fileTitle + str(yearCount), runTitle +" "+ str(yearCount), saveLoc)
            
            #Check if stopping point has been reached
            if seaLevel >= cutOffSeaLevel:
                print("Airport will be submerged by " + str(yearCount))
                break
            
            if changedIslandLand == 0:
                print("Island will be submerged by " + str(yearCount))
                break
            
            
"""
BEGIN MODEL DATA SETUP
"""            
#Get heightmap images
MaldivesImage = pil.Image.open("C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\Maldives.png")
TuvaluImage = pil.Image.open("C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\Tuvalu.png")
KiribatiImage = pil.Image.open("C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\Kiribati.png")
MarshallIslandsImage = pil.Image.open("C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\MarshallIslands.png")   

#Convert image heightmap to csv
np.savetxt('C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\Maldives.csv', MaldivesImage, delimiter=',')
np.savetxt('C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\Tuvalu.csv', TuvaluImage, delimiter=',')
np.savetxt('C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\Kiribati.csv', KiribatiImage, delimiter=',')
np.savetxt('C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\MarshallIslands.csv', MarshallIslandsImage, delimiter=',')

#Make island dataframe
Maldives = pd.read_csv('C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\Maldives.csv')
Tuvalu = pd.read_csv('C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\Tuvalu.csv')
Kiribati = pd.read_csv('C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\Kiribati.csv')
MarshallIslands = pd.read_csv('C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\MarshallIslands.csv')

#Scale down the data to fit proper measurments
for indexi, Data in Maldives.iterrows():
        for indexj, value in Data.items():
            newVal = (value*0.0008) - 2
            if newVal < 0:
                newVal = 0
            Maldives.at[indexi, indexj] = newVal
            
for indexi, Data in Tuvalu.iterrows():
        for indexj, value in Data.items():
            newVal = (value*0.0008) - 2
            if newVal < 0:
                newVal = 0
            Tuvalu.at[indexi, indexj] = newVal
        
for indexi, Data in Kiribati.iterrows():
        for indexj, value in Data.items():
            newVal = (value*0.0001) - .2
            if newVal < 0:
                newVal = 0
            Kiribati.at[indexi, indexj] = newVal
          
for indexi, Data in MarshallIslands.iterrows():
        for indexj, value in Data.items():
            newVal = (value*0.00035) - .8
            if newVal < 0:
                newVal = 0
            MarshallIslands.at[indexi, indexj] = newVal
 

#Plot current islands
plotIsland(Maldives, "Maldives2020", "Maldives 2020", "C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\")
plotIsland(Tuvalu, "Tuvalu2020", "Tuvalu 2020", "C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\")
plotIsland(Kiribati, "Kiribati2020", "Kiribati 2020", "C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\")
plotIsland(MarshallIslands, "MarshallIslands2020", "Marshall Islands 2020", "C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\")

#separate by RCP types and separate title from data
RCPType1 = "RCP2.6"
RCPType2 = "RCP4.5"
RCPType3 = "RCP8.5"

#Set sea level change data
RCP1 = [3.4734,6.9468,10.4202,13.8936,17.367,20.8404,24.3138,27.7872,31.2606,34.734,38.2074,47.559,51.52225,55.4855,59.44875,63.412,67.37525,71.3385,75.30175,79.265,83.22825,87.1915,91.15475,95.118,99.08125,103.0445,107.00775,110.971,114.93425,118.8975,122.86075,132.624,136.7685,140.913,145.0575,149.202,153.3465,157.491,161.6355,165.78,169.9245,174.069,178.2135,182.358,186.5025,190.647,194.7915,198.936,203.0805,207.225,211.3695,215.514,219.6585,223.803,227.9475,232.092,236.2365,240.381,244.5255,248.67,252.8145,256.959,261.1035,265.248,269.3925,273.537,277.6815,281.826,285.9705,290.115,294.2595]
RCP2 = [8.0706,12.1059,16.1412,20.1765,24.2118,28.2471,32.2824,36.3177,40.353,44.3883,55.611,60.24525,64.8795,69.51375,74.148,78.78225,83.4165,88.05075,92.685,97.31925,101.9535,106.58775,111.222,115.85625,120.4905,125.12475,129.759,134.39325,139.0275,143.66175,156.608,161.502,166.396,171.29,176.184,181.078,185.972,190.866,195.76,200.654,205.548,210.442,215.336,220.23,225.124,230.018,234.912,239.806,244.7,249.594,254.488,259.382,264.276,269.17,274.064,278.958,283.852,288.746,293.64,298.534,303.428,308.322,313.216,318.11,323.004,327.898,332.792,337.686,342.58,347.474]
RCP3 = [9.5984,14.3976,19.1968,23.996,28.7952,33.5944,38.3936,43.1928,47.992,52.7912,73.53,79.6575,85.785,91.9125,98.04,104.1675,110.295,116.4225,122.55,128.6775,134.805,140.9325,147.06,153.1875,159.315,165.4425,171.57,177.6975,183.825,189.9525,244.032,251.658,259.284,266.91,274.536,282.162,289.788,297.414,305.04,312.666,320.292,327.918,335.544,343.17,350.796,358.422,366.048,373.674,381.3,388.926,396.552,404.178,411.804,419.43,427.056,434.682,442.308,449.934,457.56,465.186,472.812,480.438,488.064,495.69,503.316,510.942,518.568,526.194,533.82,541.446]

"""
STABILITY ANALYSIS RUN
"""

"""
stabLow = [2.7,5.4,8.1,10.8,13.5,16.2,18.9,21.6,24.3,27,29.7,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90,93,96,99,102,105,108,111,114,117,120,123,126,129,132,135,138,141,144,147,150,153,156,159,162,165,168,171,174,177,180,183,186,189,192,195,198,201,204,207,210,213]
stabHigh = [6.4,12.8,19.2,25.6,32,38.4,44.8,51.2,57.6,64,70.4,138,149.5,161,172.5,184,195.5,207,218.5,230,241.5,253,264.5,276,287.5,299,310.5,322,333.5,345,356.5,600,618.75,637.5,656.25,675,693.75,712.5,731.25,750,768.75,787.5,806.25,825,843.75,862.5,881.25,900,918.75,937.5,956.25,975,993.75,1012.5,1031.25,1050,1068.75,1087.5,1106.25,1125,1143.75,1162.5,1181.25,1200,1218.75,1237.5,1256.25,1275,1293.75,1312.5,1331.25]

IslandModel(Maldives, stabLow, 0.3, 2, 2020, "Maldives " + RCPType1 + " Stability Low", "StabLowMaldives" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\")
IslandModel(Maldives, stabHigh, 0.3, 2, 2020, "Maldives " + RCPType1 + " Stability High", "StabHighMaldives" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\")

IslandModel(Tuvalu, stabLow, 0.3, 3, 2020, "Tuvalu " + RCPType1, "StabLowTuvalu" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\")
IslandModel(Tuvalu, stabHigh, 0.3, 3, 2020, "Tuvalu " + RCPType1, "StabHighTuvalu" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\")

IslandModel(Kiribati, stabLow, 0.3, 2, 2020, "Kiribati " + RCPType1, "StabLowKiribati" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\")
IslandModel(Kiribati, stabHigh, 0.3, 2, 2020, "Kiribati " + RCPType1, "StabHighKiribati" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\")

IslandModel(MarshallIslands, stabLow, 0.3, 2, 2020, "MarshallIslands " + RCPType2, "StabLowMarshallIslands" + RCPType2, "C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\")
IslandModel(MarshallIslands, stabHigh, 0.3, 2, 2020, "MarshallIslands " + RCPType2, "StabHighMarshallIslands" + RCPType2, "C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\")
"""

"""
RUN MODEL
"""

#Maldives
IslandModel(Maldives, RCP1, 0.3, 2, 2020, "Maldives " + RCPType1, "Maldives" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\")
IslandModel(Maldives, RCP2, 0.3, 2, 2020, "Maldives " + RCPType2, "Maldives" + RCPType2, "C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\")
IslandModel(Maldives, RCP3, 0.3, 2, 2020, "Maldives " + RCPType3, "Maldives" + RCPType3, "C:\\Users\Riley\Documents\MCM2020\Maldivesterrain\\")

#Tuvalu
IslandModel(Tuvalu, RCP1, 0.3, 3, 2020, "Tuvalu " + RCPType1, "Tuvalu" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\")
IslandModel(Tuvalu, RCP2, 0.3, 3, 2020, "Tuvalu " + RCPType2, "Tuvalu" + RCPType2, "C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\")
IslandModel(Tuvalu, RCP3, 0.3, 3, 2020, "Tuvalu " + RCPType3, "Tuvalu" + RCPType3, "C:\\Users\Riley\Documents\MCM2020\Tuvaluterrain\\")

#Kiribati
IslandModel(Kiribati, RCP1, 0.3, 2, 2020, "Kiribati " + RCPType1, "Kiribati" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\")
IslandModel(Kiribati, RCP2, 0.3, 2, 2020, "Kiribati " + RCPType2, "Kiribati" + RCPType2, "C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\")
IslandModel(Kiribati, RCP3, 0.3, 2, 2020, "Kiribati " + RCPType3, "Kiribati" + RCPType3, "C:\\Users\Riley\Documents\MCM2020\Kiribatiterrain\\")

#Marshall Islands
IslandModel(MarshallIslands, RCP1, 0.3, 2, 2020, "MarshallIslands " + RCPType1, "MarshallIslands" + RCPType1, "C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\")
IslandModel(MarshallIslands, RCP2, 0.3, 2, 2020, "MarshallIslands " + RCPType2, "MarshallIslands" + RCPType2, "C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\")
IslandModel(MarshallIslands, RCP3, 0.3, 2, 2020, "MarshallIslands " + RCPType3, "MarshallIslands" + RCPType3, "C:\\Users\Riley\Documents\MCM2020\MarshallIslandsterrain\\")
