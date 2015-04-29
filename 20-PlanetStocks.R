
# --------------------------------------------------------------
# Planet Resource Stock Piles . . . .
# hijk/2015
# --------------------------------------------------------------
library(ggplot2)
library(reshape2)

rm(list=ls())
gameName = "127256-SmithsWorld"
gameRace = "Robots"

data=read.table(paste(gameName,'-PlanetStocks.txt',sep=""),sep='\t',header=T)

D <- melt(data, id=c("TURN"))
names(D)[2:3] <- c("Resource", "Quantity")
p = ggplot(D,aes(x=TURN,y=Quantity,group=Resource)) +
	geom_line(aes(colour=Resource),size=1) +
 	scale_x_continuous("Turn Number") +
 	scale_y_continuous("Quantity") +
 	labs(title=paste(gameRace, gameName, "Planet Resource Stock Piles")) 
 	#scale_colour_brewer("STOCKS",palette=4) + 
 	#facet_wrap(~Resource,ncol=1,scales="free_y" ) 	
p

ggsave(file=paste(gameName,"-PlanetResourcePlot.png",sep=""),dpi=300)

# --------------------------------------------------------------
data=read.table(paste(gameName,'-ShipLoads.txt',sep=""),sep='\t',header=T)
#data$RESOURCE <- data$TRIT + data$MOLY + data$DURA + data$NEUT + data$SUPP

e <- as.data.frame(cbind(data$TURN,data$SUPPLIES, data$MC, data$CLANS, data$MINERALS,data$NEUT, data$BURN, data$DIST))
names(e) <- c("TURN", "SUPPLIES","MCREDITS","CLANS","MINERALS","NEUT","BURN","DIST")
D <- melt(e, id=c("TURN"))
names(D)[2:3] <- c("Resource", "Quantity")
p = ggplot(D,aes(x=TURN,y=Quantity,group=Resource)) +
	geom_line(aes(colour=Resource),size=1) +
 	scale_x_continuous("Turn Number") +
 	scale_y_continuous("Quantity") +
 	labs(title=paste(gameRace, gameName, "Ship Loads in Transit")) +
 	#scale_colour_brewer("STOCKS",palette=3) + 
 	facet_wrap(~Resource,ncol=1,scales="free_y" ) 	
p

ggsave(file=paste(gameName,"-ShipLoadPlot.png",sep=""),dpi=300)

# --------------------------------------------------------------
for (i in 2:7)
{	e[,i] <- e[,i]/e$DIST	}
e$CARGO <- e$SUPPLIES + e$MCREDITS + e$CLANS + e$MINERALS
f <- as.data.frame(cbind(e$TURN, e$CARGO, e$BURN, e$DIST)) 
names(f) <- c("TURN", "CARGO","BURN","DIST")
D <- melt(f, id=c("TURN"))
names(D)[2:3] <- c("Resource", "Quantity")
p = ggplot(D,aes(x=TURN,y=Quantity,group=Resource)) +
	geom_line(aes(colour=Resource),size=1) +
 	scale_x_continuous("Turn Number", limits=c(0,60)) +
 	scale_y_continuous("Quantity") +
 	labs(title=paste(gameRace, gameName, "Ship Loads in Transit")) +
 	#scale_colour_brewer("STOCKS",palette=3) + 
 	facet_wrap(~Resource,ncol=1,scales="free_y" ) 	
p

ggsave(file=paste(gameName,"-ShipLoadPlot.png",sep=""),dpi=300)

# --------------------------------------------------------------
f$value <- f$CARGO - 2*f$BURN
p = ggplot(f,aes(x=TURN,y=value)) +
	geom_line(size=1) +
 	scale_x_continuous("Turn Number", limits=c(0,60)) +
 	scale_y_continuous("Quantity", limits=c(0,20)) +
 	labs(title=paste(gameRace, gameName, "Ship Loads in Transit")) 
 	#scale_colour_brewer("STOCKS",palette=3) + 
 	#facet_wrap(~Resource,ncol=1,scales="free_y" ) 	
p

ggsave(file=paste(gameName,"-ShipLoadPlot.png",sep=""),dpi=300)

# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------



