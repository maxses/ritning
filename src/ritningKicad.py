#!/usr/bin/python3.7
'''
This class helps scripted generation of svg graphics.
It can be used to calculate drawings for housings or PCBs.

There is one world center coordinate, usually the middle of the page.
The coordinates are growing towards the lower right corner.
The anchor of drawing objects are mostly defined by their center.

An frame of interest can be defined around the world center; The center of this
FOI will be used for calculation of followed drawing objects.

'''
import math
import os

padMargin=0.01
conturMargin=0.15

# just some codes. Values meaningless
right=1
left=2
top=3
bottom=4

class RitningKicad(object):
    def __init__(self, file="output", name="foo" ):
        self.outFileName = name + '.kicad_mod'
        self.outFile = open( self.outFileName, 'w')

        # header = open( os.path.dirname(__file__) + '/header.xml', 'r')
        header = open( os.path.dirname(__file__) + '/header.kicad_mod', 'r')

        header_data = header.read()
        header_data = header_data.replace("@name@", name)
        header.close()
        self.outFile.write(header_data)
        self.name = name
        self.thtPadType="circle"
        self.layer="F.Cu F.Paste F.Mask"
        self.factor=1
        self.shape="rect"

    #def __del__(self):
    def finish(self):
        footer = open( os.path.dirname(__file__) + '/footer.kicad_mod', 'r')
        footer_data = footer.read()
        footer.close()
        self.outFile.write(footer_data)
        self.outFile.close()
        print( "Created " + self.outFileName )

    def writeRect(self, id, x, y, width, height):

        if id==-1:
           sid="\"\""
        else:
           sid=str(id)
        self.outFile.write( "  (pad "
               + sid + " smd " + self.shape + " (at "
               + str( x * self.factor ) + " " + str( y  * self.factor ) + ") (size "
               + str( width * self.factor ) + " " + str( height * self.factor ) +
               ") (layers " + self.layer + "))\n" )
    def writeLine(self, x1, y1, x2, y2, layer="F.SilkS"):
        self.outFile.write( "  (fp_line (start "
               + str( x1 * self.factor ) + " " + str( y1  * self.factor ) + ") (end "
               + str( x2 * self.factor ) + " " + str( y2  * self.factor )
               + ") (layer " + layer + ") (width 0.15))\n" )
    def circle(self, x, y, r):
        self.outFile.write( "  (fp_circle (center "
        + str( x * self.factor ) + " " + str( y  * self.factor ) + ") (end "
        + str( r * self.factor ) + " 0 ) (layer \"F.SilkS\") (width 0.12) (fill none))\n" )

    def text(self, x, y, text):
       self.outFile.write( "  (fp_text user \"" + text +"\" (at "
       + str( x * self.factor ) + " " + str( y  * self.factor )+ " unlocked) (layer \"F.SilkS\")\n"
           +"    (effects (font (size 1 1) (thickness 0.15)))\n"
           +"  )" )

    def smdPad(self, id, x, y, width, height):
         self.writeRect(id, x, y, width, height)
         
    def smdPads(self, x, y, width, height, padWidth, padHeight, numbers):
         self.smdPad( numbers[0],  x - (width/2), y + (height/2)
                                                         , padWidth, padHeight)
         self.smdPad( numbers[1],  x + (width/2), y + (height/2)
                                                         , padWidth, padHeight)
         self.smdPad( numbers[2],  x + (width/2), y - (height/2)
                                                         , padWidth, padHeight)
         self.smdPad( numbers[3],  x - (width/2), y - (height/2)
                                                         , padWidth, padHeight)

    def smdPadRound(self, id, x, y, size):
        self.shape="oval"
        self.writeRect(id, x, y, size, size)
        self.shape="rect"
        #if id==-1:
        #    sid="\"\""
        #else:
        #    sid=str(id)
        #self.outFile.write( "  (pad "
        #      + sid + " smd oval (at "
        #      + str( x * self.factor ) + " " + str( y  * self.factor ) + ") (size "
        #      + str( width * self.factor ) + " " + str( height * self.factor ) +
        #      ") (layers " + self.layer + "))\n" )

    def npthPadSize(self, x, y, size):
         self.outFile.write( "  (pad "
                + "\"\"" + " np_thru_hole circle (at "
                + str( x * self.factor ) + " " + str( y  * self.factor ) + ") "
                + "(size " + str( size  * self.factor ) + " " + str( size  * self.factor ) + ") "
                + "(drill " + str( size  * self.factor ) + ") "
                + "(layers *.Cu *.Mask))\n" )

    def npthPad(self, x, y):
         self.npthPadSize(x, y, 0.762)

    def thtPad(self, id, x, y):
         self.outFile.write( "  (pad "
                + str(id) + " thru_hole " + self.thtPadType + " (at "
                + str( x * self.factor ) + " " + str( y  * self.factor ) + ") "
                + "(size 1.524 1.524) (drill 0.762) "
                + "(layers *.Cu *.Mask))\n" )

    def line(self, x1, y1, x2, y2):
         self.writeLine(x1, y1, x2, y2)

    def rect(self, x1, y1, x2, y2):
         self.writeLine(x1, y1, x2, y1)
         self.writeLine(x2, y1, x2, y2)
         self.writeLine(x1, y1, x1, y2)
         self.writeLine(x1, y2, x2, y2)
         
    def boundaryBox(self, x1, y1, x2, y2):
        self.writeLine(x1, y1, x2, y1, "F.CrtYd")
        self.writeLine(x2, y1, x2, y2, "F.CrtYd")
        self.writeLine(x1, y1, x1, y2, "F.CrtYd")
        self.writeLine(x1, y2, x2, y2, "F.CrtYd")

    def openRect(self, x1, y1, x2, y2, side):
        # top
        if side != top:
            self.writeLine(x1, y1, x2, y1)
        # right
        if side != right:
            self.writeLine(x2, y1, x2, y2)
        if side != left:
            self.writeLine(x1, y1, x1, y2)
        # bottom
        if side != bottom:
            self.writeLine(x1, y2, x2, y2)

    def rectCentered(self, x1, y1, width, height):
        self.writeLine(x1-(width/2), y1-(height/2), x1+(width/2), y1-(height/2))
        self.writeLine(x1+(width/2), y1-(height/2), x1+(width/2), y1+(height/2))
        self.writeLine(x1-(width/2), y1-(height/2), x1-(width/2), y1+(height/2))
        self.writeLine(x1-(width/2), y1+(height/2), x1+(width/2), y1+(height/2))

    def nameLabel(self, x, y):
        self.outFile.write( "  (fp_text value " + self.name + " "
            + "(at " + str(x) + " " + str(y) + ") (layer F.Fab) "
            + "(effects (font (size 1 1) (thickness 0.15))) "
            + ")" )

    def reference(self, x, y):
        self.outFile.write( "  (fp_text reference REF** "
            + "(at " + str(x) + " " + str(y) + ") (layer F.SilkS) "
            + "(effects (font (size 1 1) (thickness 0.15))) "
            + ")" )

    def attribute(self, attr):
        self.outFile.write( "  (attr " + str(attr) + ")\n" )
         
    def front(self):
        self.layer="F.Cu F.Paste F.Mask"

    def back(self):
        self.layer="B.Cu B.Paste B.Mask"

    def frontMasked(self):
        self.layer="F.Cu"

    def backMasked(self):
        self.layer="B.Cu"


#---fin------------------------------------------------------------------------
