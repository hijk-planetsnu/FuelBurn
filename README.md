# FuelBurn
Random analytical stabs to describe what makes a good economy.

Planets Nu Game Data Analysis
Just some attempts to use the API to gather game data files by turn and generate some plots and a look at resource utilization. The main battle early on in Planets is all about developing an efficient transportation network. I started by trying to figure out how to measure transport efficiency in terms of costs (time and fuel burned) vs. value (production). No analytical tool has yet been produced, but playing with the data is cool. 

01-DownLoadTurnFiles.py
    Use the API to locate player info and download either: 1) active current game files, or 2) public completed game files. A local folder is established and turn files for each target game are dowloaded and stored.

02-FuelBurnTransport.py
    In progress. Script has basic py code for accessing data in each turn from the json file. Any analytical scheme can be quickly executed across all turns in a game. Output is a data table for input into R.


20-PlanetStocks.R
    Simple plotting script to look at what resources are accumulating on planets or what resources are being transported by frieghters. Uses ggplot2 package. 
    
