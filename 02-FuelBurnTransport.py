#!/usr/bin/python

'''
NEUTRONIUM FUEL BURN and ECONOMIC EFFICIENCY

The eventual goal of this script will be to provide an analysis tool for economic
development and transport efficiency. At present, it is just a data extraction
and plotting set of code loops.

Functionally, you can extract TURN data from JSON files and build data tables for
the variables and information you would like to analyze. End result is to produce
a tab-delimited txt file that could be read by an R script for plotting/analysis.
The script file "20-PlanetStocks.R" will read the data table generated here and
you can define plots in R using the ggplot2 module.

This script is a work in progress. It is not focused on producing any one specific
result at the moment. It just contains all the code loops and logic for getting
at the data you would like to use contained within turn files.

hijk/2015

'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, re, os, time
import json, urllib, urllib2, gzip, StringIO

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# To better look inside the json file, here's a quick way to dump contents
#   with an indented format that makes the nested data structure easier
#   to interpret.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
gameData = '00-GameData/'
gameName = '127256-SmithsWorld'
testDump = 0    # flag to output formatted data file


gameFolder = gameData + gameName        #  '00-GameData/127256-SmithsWorld'
turnFolders = os.listdir(gameFolder)

resourceKEYS = ["tritanium", "molybdenum", "duranium", "neutronium", "supplies", "megacredits", "clans"]
shipKEYS = ["tritanium", "molybdenum", "duranium", "neutronium", "supplies", "megacredits", "clans", "minerals",  "ammo", "burn", "dist"]
massKEYS = ["tritanium", "molybdenum", "duranium", "neutronium", "supplies", "clans", "ammo" ]
mineralKEYS = ["tritanium", "molybdenum", "duranium" ]

OUT=open("%s-PlanetStocks.txt" % gameName,'w')
OUT.write("TURN\tTRIT\tMOLY\tDURA\tNEUT\tSUPP\tMC\tCLANS\n")
OUT.close()
OUT=open("%s-ShipLoads.txt" % gameName,'w')
OUT.write("TURN\tTRIT\tMOLY\tDURA\tNEUT\tSUPPLIES\tMC\tCLANS\tMINERALS\tAMMO\tBURN\tDIST\n")
OUT.close()

for numTag in turnFolders:
    print numTag
    IN=open("%s/%s/01-RawDataDump.txt" % (gameFolder, numTag), 'r')
    jsonRaw = IN.readline()
    IN.close()
    gameJson = json.loads(jsonRaw)
    playerID = gameJson['rst']['player']['id']

    #OUT=open("%s/%s/02-FormattedDataDump.txt" % (gameFolder, numTag), 'w')
    #OUT.write(json.dumps(gameJson, indent=4))
    #OUT.close()
    
    if testDump == 1:
        OUT=open("%s/%s/02-FormattedDataDump.txt" % (gameFolder, numTag), 'w')
        OUT.write(json.dumps(gameJson, indent=4))
        OUT.close()
        print "username              = ", gameJson['rst']['player']['username']
        print "race id num           = ", gameJson['rst']['player']['raceid']
        print "player number in game = ", gameJson['rst']['player']['id']
        #print gameJson['rst']['ships'][0]['name']
        print len(gameJson['rst']['ships'])
        for i in range(len(gameJson['rst']['ships'])):
            print gameJson['rst']['ships'][i]['name'], gameJson['rst']['ships'][i]['ownerid']
        sys.exit()
        
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Test Calculation - dump planet inventories for all turns
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    resourcePILE = {}
    resourceSHIP = {}
    for res in resourceKEYS:
        resourcePILE[res] = 0
    for res in shipKEYS:
        resourceSHIP[res] = 0

    
    # Compile table of PLANET stock piles for all resources . . . . . . . 
    OUT1=open("%s/%s/03-PlanetStockPileDump.txt" % (gameFolder, numTag), 'w')
    OUT1.write("Planet\tTRIT\tMOLY\tDURA\tNEUT\tSUPP\tMC\tCLANS\n")
    for i in range(len(gameJson['rst']['planets'])):
        if gameJson['rst']['planets'][i]['ownerid'] == playerID:
            OUT1.write("%s" % gameJson['rst']['planets'][i]['id'])
            for res in resourceKEYS:
                resourcePILE[res] += gameJson['rst']['planets'][i][res]
                OUT1.write("\t%d" % (gameJson['rst']['planets'][i][res]))
            OUT1.write("\n")
    OUT1.close()
    
    # Compile table of SHIP loads for all resources . . . . . . . 
    OUT2=open("%s/%s/04-ShipLoadFrieghter.txt" % (gameFolder, numTag), 'w')
    OUT2.write("Ship\tTRIT\tMOLY\tDURA\tNEUT\tSUPP\tMC\tCLANS\tMINERALS\tAMMO\tBURN\tDIST\n") 
    for i in range(len(gameJson['rst']['ships'])):
        if gameJson['rst']['ships'][i]['ownerid'] == playerID:
            beamNum = gameJson['rst']['ships'][i]['beams']
            torpNum = gameJson['rst']['ships'][i]['torps']
            # Filter Calculation on cargo transit vessels, not warships . . . . . 
            if beamNum <= 4 and torpNum <= 2:
                OUT2.write("%d" % gameJson['rst']['ships'][i]['id'])
                loadMass = 0
                mineralShip = 0
                for res in resourceKEYS:
                    resourceSHIP[res] += gameJson['rst']['ships'][i][res]
                    OUT2.write("\t%d" % (gameJson['rst']['ships'][i][res]))
                for res in mineralKEYS:
                    mineralShip += gameJson['rst']['ships'][i][res]
                resourceSHIP['minerals'] += mineralShip
                OUT2.write("\t%d" % mineralShip)
                resourceSHIP['ammo'] += gameJson['rst']['ships'][i]['ammo']
                OUT2.write("\t%d" % (gameJson['rst']['ships'][i]['ammo']))
                # Fuel and Distance . . . . .
                # Did the ship move last turn . . . . .
                burn = 0
                dist = 0
                if len(gameJson['rst']['ships'][i]['history']) > 0:
                    xnow  = float(gameJson['rst']['ships'][i]['x'])
                    ynow  = float(gameJson['rst']['ships'][i]['y'])
                    xlast = float(gameJson['rst']['ships'][i]['history'][0]['x'])
                    ylast = float(gameJson['rst']['ships'][i]['history'][0]['y'])
                    if (xnow != xlast or ynow != ylast) and gameJson['rst']['ships'][i]['warp'] != 0:
                        shipID = gameJson['rst']['ships'][i]['id']
                        hullID = gameJson['rst']['ships'][i]['hullid']
                        beamID = gameJson['rst']['ships'][i]['beamid']
                        torpID = gameJson['rst']['ships'][i]['torpedoid']
                        hullMass = gameJson['rst']['hulls'][hullID-1]['mass']
                        beamMass = 0
                        if beamID > 0:
                            beamMass = beamNum * gameJson['rst']['beams'][beamID-1]['mass']
                        torpMass = 0
                        if torpID > 0:
                            torpMass = torpNum * gameJson['rst']['torpedos'][torpID-1]['mass']
                        loadMass = 0
                        for load in massKEYS:
                            loadMass += gameJson['rst']['ships'][i][load]
                            
                        # First pass calcs based on current ship mass in Turn X
                        ShipMass = hullMass + beamMass + torpMass + loadMass   
                        dist = int(((xlast-xnow)**2  + (ylast-ynow)**2)**0.5)
                        warpX   = "warp" +  str(gameJson['rst']['ships'][i]['warp'])   # key string for warp speed
                        engineX = gameJson['rst']['ships'][i]['engineid']    # engine tech level 
                        fuelfactor = gameJson['rst']['engines'][engineX-1][warpX]
                        burn = int(fuelfactor * (int(ShipMass/10))/10000)
                        
                        # Now back correct for ship mass in Turn X-1 by adding burned fuel mass
                        ShipMass += burn
                        burn = int(fuelfactor * (int(ShipMass/10))/10000)
    
                                  
                resourceSHIP['burn'] += burn
                resourceSHIP['dist'] += dist
            OUT2.write("\t%d\t%d" % (burn, dist))    
            OUT2.write("\n")
    OUT2.close()
    
    
    OUT3=open("%s-PlanetStocks.txt" % gameName ,'a')
    OUT3.write(numTag)
    for res in resourceKEYS:
        OUT3.write("\t%d" % resourcePILE[res])
    OUT3.write("\n")
    OUT3.close()
    
    OUT4=open("%s-ShipLoads.txt" % gameName ,'a')
    OUT4.write(numTag)
    for res in resourceKEYS:
        OUT4.write("\t%d" % resourceSHIP[res])
    OUT4.write("\t%d\t%d\t%d\t%d\n" % (resourceSHIP['minerals'],resourceSHIP['ammo'],resourceSHIP['burn'],resourceSHIP['dist']))
    OUT4.close()

print "\n\n\n *  *  *  *  *      D O N E     *  *  *  *  **  \n\n"

