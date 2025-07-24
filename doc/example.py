#!/usr/bin/python3
'''
   Creates examples for the cheet-sheet document
'''

import math
import subprocess
import sys
sys.path.append('../src')
import ritningSvg as ritning


defaultArgs=[ "convert", "example.svg" \
   , "-trim" \
   , "-bordercolor", "white" \
   , "-border", "5" \
   , "-bordercolor", "magenta" \
   , "-border", "1" \
   ]

width=15.0

def quadCircle():
   r = ritning.Ritning(0, 0, "example")
   pumpPcb=20.0
   r.quadCircle( 0.0 , 0.0, (width/2.0)-2.0, (width/2.0)-2.0, 2.6)
   r.mark(0,0)

def rect():
   r = ritning.Ritning(0, 0, "example")
   r.rect( 0.0 , 0.0, width, width )
   r.mark(0,0)

def rectRounded():
   r = ritning.Ritning(0, 0, "example")
   r.rectParam="rx=\"5mm\""
   r.rect( 0.0 , 0.0, width, width )
   r.mark(0,0)

def circle():
   r = ritning.Ritning(0, 0, "example")
   r.circle( 0.0 , 0.0, width )
   r.mark(0,0)

def text():
   r = ritning.Ritning(0, 0, "example")
   r.text( 0, 0, "This is a text box" )
   r.mark(0,0)

def line():
   r = ritning.Ritning(0, 0, "example")
   r.line( -2, 2, 2, -2 )
   r.mark(0,0)

def infoBox():
   r = ritning.Ritning(0, 0, "example")
   r.infoBox( 0, 0, ["This is a multiline", "Info box", "Put notes here"] )
   r.mark(0,0)

quadCircle()
subprocess.run( defaultArgs + [ "example_quadCircle.png" ] )
rect()
subprocess.run( defaultArgs + [ "example_rect.png" ] )
rectRounded()
subprocess.run( defaultArgs + [ "example_rect_rounded.png" ] )
circle()
subprocess.run( defaultArgs + [ "example_circle.png" ] )
text()
subprocess.run( defaultArgs + [ "example_text.png" ] )
line()
subprocess.run( defaultArgs + [ "example_line.png" ] )
infoBox()
subprocess.run( defaultArgs + [ "example_info_box.png" ] )


#---fin------------------------------------------------------------------------
