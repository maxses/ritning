#!/usr/bin/python
'''
Creates SVG of the cover plate for pumping housing
    0-->
    |
   \ /
'''

import math
import sys

sys.path.append('..')
import ritning


ritning = ritning.Ritning(0, 40)

# RND 455-00096
# The inner space is 123.8x58 (spec); The space for drills is 121x57 (measured)
# The inner space  equals the available seating on the front
width=123.8
height=58
# Spec says 29.00mm; measured:
pumpDiameter = 30.0
pumpPcbXSize=31.75
pumpPcbYSize=49.53
pumpPcbHolesXDist=25.40
pumpPcbHolesYDist=43.18
pumpBorderDist = 6
pumpScrewRadius=24.25
ledX=5.08
ledY=8.85
ledYDist=5.08
# Button dist: 10,16
buttonX=10.16/2
buttonY=ritning.triangleHeight(21.69, 10.16)
canXPos=8.89
canYPos=ritning.triangleHeight(6.07, 8.60)
uartYPos=ritning.triangleHeight(18.76, 8.60)
sensorWireRadius=26.50

ritning.rectParam="rx=\"5mm\""
ritning.rect(0,0,width,height)
ritning.rect(0,0, 121, 57)
ritning.setFrameOfInterest(0,0,width,height)
ritning.rectParam="rx=\"0.5mm\""

# These are the measured values for the screw bolts for the housing
ritning.quadCircle( 0.0 , 0.0, 112.5/2.0, 48/2.0, 5.6)

# The pumps
ritning.circle( ritning.left() + (pumpDiameter/2) + pumpBorderDist, 0, pumpDiameter, 20*2)
ritning.circle( ritning.right() - (pumpDiameter/2) - pumpBorderDist, 0, pumpDiameter, 20*2)

# Pump screws left
ritning.circle( ritning.left() + (pumpDiameter/2) + pumpBorderDist + (math.cos(math.pi/4)*pumpScrewRadius) , 0 - (math.cos(math.pi/4)*pumpScrewRadius), 2.7, 7 )
ritning.circle( ritning.left() + (pumpDiameter/2) + pumpBorderDist - (math.cos(math.pi/4)*pumpScrewRadius) , 0 + (math.cos(math.pi/4)*pumpScrewRadius), 2.7, 7 )

# Pump screws
ritning.circle( ritning.right() - (pumpDiameter/2) - pumpBorderDist - (math.cos(math.pi/4)*pumpScrewRadius), 0 - (math.cos(math.pi/4)*pumpScrewRadius), 2.7, 7 )
ritning.circle( ritning.right() - (pumpDiameter/2) - pumpBorderDist + (math.cos(math.pi/4)*pumpScrewRadius), 0 + (math.cos(math.pi/4)*pumpScrewRadius), 2.7, 7 )

# Sensors
ritning.circle( ritning.left() + (pumpDiameter/2) + pumpBorderDist + (math.cos(math.pi/4)*sensorWireRadius) , 0 + (math.cos(math.pi/4)*sensorWireRadius), 8.6, 12.54 )
ritning.circle( ritning.right() - (pumpDiameter/2) - pumpBorderDist - (math.cos(math.pi/4)*sensorWireRadius), 0 + (math.cos(math.pi/4)*sensorWireRadius), 8.6, 12.54 )


#--- The pumping PCB

ritning.setFrameOfInterest(0,0,pumpPcbXSize,pumpPcbYSize)
ritning.rect(0,0,pumpPcbXSize,pumpPcbYSize)

# Mounting screws for PCB
ritning.quadCircle( 0.0 , 0.0, (pumpPcbHolesXDist/2.0), (pumpPcbHolesYDist/2.0), 2.7, 5)

# Buttons
ritning.circle( -buttonX, -buttonY, 3.2)
ritning.circle( +buttonX, -buttonY, 3.2)


# Lightguide for LEDs
# Drill 2.6, outer diameter 3.2 (datasheet)
ritning.circle( -ledX, -ledY, 2.6, 3.2)
ritning.circle( 0    , -ledY, 2.6, 3.2)
ritning.circle( +ledX, -ledY, 2.6, 3.2)

ritning.circle( -ledX, -ledY - ledYDist, 2.6, 3.2)
ritning.circle( 0    , -ledY - ledYDist, 2.6, 3.2)
ritning.circle( +ledX, -ledY - ledYDist, 2.6, 3.2)


# CAN connectors
ritning.circle( -canXPos, canYPos, 8.5, 12.54)
ritning.circle( +canXPos, canYPos, 8.5, 12.54)

# Uart connector
ritning.circle( 0, uartYPos, 8.5, 12.54)


#---fin------------------------------------------------------------------------
