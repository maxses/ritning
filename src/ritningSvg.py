#!/usr/bin/python
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


class Ritning(object):
    def __init__(self, centerX = 0, centerY = 0, name = "output", feature = "portrait"):
        self.outFile = open( name + '.svg', 'w')
        header = open( os.path.dirname(__file__) + '/../data/header_' + feature + '.xml', 'r')
        header_data = header.read()
        header.close()
        self.outFile.write(header_data)
        if( feature == "horizontal" or feature == "landscape" ):
           self.width = 297.0
           self.widthPx = 1052.3622047
           self.height = 210.0
           self.heightPx = 744.09448819
           print("horizontal")
        elif( feature == "vertical" or feature == "portrait" ):
           self.width = 210.0
           self.widthPx = 744.09448819
           self.height = 297.0
           self.heightPx=1052.3622047
           print("vertical")
        elif( feature == "big_square" ):
           self.width = 600.0
           # self.r=3.543307087
           self.r=10
           self.widthPx = self.width * self.r
           self.height = 600.0
           self.heightPx = self.height * self.r
           print("big_square")
        else:
           print("unknown layout: ", feature)
           exit(22)

        if(centerX):
            self.centerX = centerX
        else:
            self.centerX = self.width/2.0
        if(centerY):
            self.centerY = centerY
        else:
            self.centerY = self.height/2.0

        self.runningId=4174
        self.unit="px"
        self.FOIx=0
        self.FOIy=0
        self.FOIwidth = 100
        self.FOIheight = 100
        self.drawCircleCenter = True
        self.drawCircleDiameter = True
        self.pxPerMmX = self.widthPx / self.width
        self.pxPerMmY = self.heightPx / self.height
        self.rectParam = ""
        self.fontSize = 8
        self.charSize=3
        self.textBorder=1
        self.font = "sans-serif"
        self.fontStyle = "fill:#000000;stroke:none"
        self.style="fill:none;fill-opacity:1;stroke:#0000ff;stroke-width:1px;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        self.singleAdd=""
        if( False and ( self.pxPerMm != self.pxPerMmY ) ):
            print("X-Y-ration not equeal: " +
                str(self.pxPerMmX) + " / " +
                str(self.pxPerMmY) )
            raise

    def __del__(self):
        self.finish()

    def finish(self):
        print("__DEL__" )
        footer = open( os.path.dirname(__file__) + '/../data/footer.xml', 'r')
        footer_data = footer.read()
        footer.close()
        self.outFile.write(footer_data)
        self.outFile.close()
        print("Use Inkscape and convert the textx fields from 'Object to path' (mark object, CTRL+Shift+C)")

    def rect(self, rX, rY, width, height):
        print("Rect " + str( width ) + "/" + str( height ) )
        # "style=\"fill:none;stroke:#000000;stroke-opacity:1\" "
        self.outFile.write("     <rect "
            "style=\"" + self.style + "\" "
            "id=\"rect" + str( self.runningId ) + "\" "
            "width=\"" + self.xstr(width) + "\" "
            "height=\"" + self.ystr(height) + "\" "
            "x=\"" + self.xstr( ( self.centerX + self.FOIx - (width/2.0) ) + rX ) + "\" "
            "y=\"" + self.ystr( ( self.centerY + self.FOIy - (height/2.0) ) + rY ) + "\" "
            + self.rectParam +
            " />\n")
        self.runningId += 1

    def textSingleSpan(self, text):
        self.outFile.write("<tspan "
            "sodipodi:role=\"line\" "
            "id=\"text" + str( self.runningId+1 ) + "\" "
            ">" + text +
            "</tspan>")
        self.runningId += 1

    def textSpan(self, x, y, text):
        # "x=\"" + self.xstr( ( self.centerX + self.FOIx ) + rX ) + "\" "
        # "y=\"" + self.ystr( ( self.centerY + self.FOIy ) + rY ) + "\" "
        self.outFile.write("<tspan "
            "sodipodi:role=\"line\" "
            "id=\"text" + str( self.runningId+1 ) + "\" "
            "x=\"" + self.xstr( ( self.centerX + self.FOIx ) + x ) + "\" "
            "y=\"" + self.ystr( ( self.centerY + self.FOIy ) + y ) + "\" "
            ">" + text +
            "</tspan>")
        self.runningId += 1

    def text(self, rX, rY, text):
        self.outFile.write("     <text "
            "style=\"font-style:normal;font-weight:normal;font-size:" + str(self.fontSize) + "px;line-height:125%;"
            "font-family:" + self.font + ";letter-spacing:0px;word-spacing:0px;"
            + self.fontStyle + ";fill-opacity:1;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" "
            "id=\"text" + str( self.runningId ) + "\" "
            + self.singleAdd +
            "x=\"" + self.xstr( ( self.centerX + self.FOIx ) + rX ) + "\" "
            "y=\"" + self.ystr( ( self.centerY + self.FOIy ) + rY ) + "\" "
            "sodipodi:linespacing=\"125%\" "
            ">")
        line=0
        if type(text) == list:
            print("Text is NO list")
            for e in text:
                offset = len(text) * self.charSize
                self.textSpan( rX + self.textBorder
                        , rY - offset + ( line * self.charSize) + self.textBorder, e )
                line+=1
                # self.textSingleSpan( e )
        else:
            self.textSingleSpan( text )
        self.outFile.write("</text>\n")
        self.runningId += 1

    def textCentered(self, cX, cY, width, height, text):
        self.text( cX -( width/2), cY+(height/2), text)

    def textFlipped(self, cX, cY, width, height, text):
        self.singleAdd="transform=\"translate(" + str( self.mmToPxX( self.centerX + self.FOIx + cX )*2 ) + ",0) scale (-1, 1)\" "
        self.text( cX -( width/2), cY+(height/2), text)
    def textFlippedRotated(self, cX, cY, width, height, text):
        self.singleAdd="transform=\"translate(" + str( self.mmToPxX( self.centerX + self.FOIx + cX )*2 ) + ",0) scale (-1, 1) " \
             "rotate(90," + str( self.mmToPxX( ( self.centerX + self.FOIx ) + cX ) ) + ", " \
             + str( self.mmToPxY( ( self.centerY + self.FOIy ) + cY ) ) + ")\" "
        self.text( cX -( width/2), cY+(height/2), text)
    def plainCircle(self, rX, rY, d ):
        # fill:none;stroke:#000000;stroke-opacity:1
        self.outFile.write("     <circle "
             "style=\"" + self.style + "\" "
             "id=\"rect" + str( self.runningId ) + "\" "
             "cx=\"" + self.xstr( ( self.centerX + self.FOIx ) + rX ) + "\" "
             "cy=\"" + self.ystr( ( self.centerY + self.FOIy ) + rY ) + "\" "
             "r=\"" + self.xstr( d/2 ) + "\" "
             "/>\n")
        self.runningId += 1
    def mark(self, rX, rY):
        # fill:none;stroke:#000000;stroke-opacity:1
        self.outFile.write("     <circle "
             "style=\"" + "fill:none;fill-opacity:1;stroke:#00AFAF;" + "\" "
             "id=\"rect" + str( self.runningId ) + "\" "
             "cx=\"" + self.xstr( ( self.centerX + self.FOIx ) + rX ) + "\" "
             "cy=\"" + self.ystr( ( self.centerY + self.FOIy ) + rY ) + "\" "
             "r=\"" + self.xstr( 0.6 ) + "\" "
             "/>\n")
        self.runningId += 1
    def arc(self, rX, rY, d, start, end ):
        # 85 350 A 150 180 0 0 0  280 79"
        self.outFile.write("     <path "
            "style=\"" + self.style + "\" "
            "id=\"path" + str( self.runningId ) + "\" "
            "d=\"" +
            "M " + self.xstr( self.centerX + self.FOIx + rX + ( math.cos( math.radians(start))*d/2 ), False ) + " "
                 + self.ystr( self.centerY + self.FOIy + rY + ( math.sin( math.radians(start))*d/2 ), False ) + " " +
            "A " + self.xstr( d/2, False ) + " " + self.ystr( d/2, False ) + " 0 0 0" +
            " " +  self.xstr( self.centerX + self.FOIx + rX + ( math.cos( math.radians(end)  )*d/2 ), False ) + " " +
                   self.ystr( self.centerY + self.FOIy + rY + ( math.sin( math.radians(end)  )*d/2 ), False ) + "\" "
            "/>\n")
        self.runningId += 1
        # <path style="fill:none;stroke:#0000ff;stroke-width:0.0377953" id="path1307" sodipodi:type="arc" sodipodi:cx="316.7918090820312" sodipodi:cy="292.9497680664062"
        # sodipodi:rx="5.706301212310791" sodipodi:ry="5.117842197418213" sodipodi:start="2.6555358118976" sodipodi:end="1.661704910991306" sodipodi:open="true" sodipodi:arc-type="arc" />
    def comment(self, text ):
        self.outFile.write("     <comment "
             "value=\"" + text + "\" "
             "/>\n")

    def circle(self, rX, rY, d, d2=0 ):
        self.plainCircle(rX, rY, d)
        if(d2):
            self.plainCircle(rX, rY, d2)
        if( self.drawCircleDiameter ):
            self.text(  rX + ( ( ( d / 2.0 ) + 2 ) * math.cos( math.pi / 4) ),
                        rY - ( ( ( d / 2.0 ) + 2 ) * math.sin( math.pi / 4) ),
                        ""+ str(d) + "mm")
        if( self.drawCircleCenter ):
            # self.line(  rX - 5.0, rY - 5.0, 10.0, 10.0)
            # self.line(  rX - 5.0, rY + 5.0, 10.0, -10.0)
            self.line(  rX - 2.0, rY - 2.0, rX + 2.0, rY + 2.0)
            self.line(  rX - 2.0, rY + 2.0, rX + 2.0, rY - 2.0)
    def line(self, _x1, _y1, _x2, _y2):
        # fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1
        self.outFile.write("     <path "
            "style=\"" + self.style + "\" "
            "id=\"path" + str( self.runningId ) + "\" "
            "d=\"M " + self.xstr( ( self.centerX + self.FOIx ) + _x1 , False ) + ","
                     + self.ystr( ( self.centerY + self.FOIy ) + _y1 , False ) + " L "
                     + self.xstr( ( self.centerX + self.FOIx ) + _x2 , False ) + ","
                     + self.ystr( ( self.centerY + self.FOIy ) + _y2 , False ) + "\" "
             "/>\n")
        self.runningId += 1

    def setFrameOfInterest(self, rX, rY, width, height):
        self.FOIx = rX
        self.FOIy = rY
        self.FOIwidth = width
        self.FOIheight = height
    def left(self):
        return ( - ( self.FOIwidth / 2.0 ) )
    def right(self):
        return ( self.FOIwidth / 2.0 )
    def top(self):
        return( - ( self.FOIheight / 2.0 ) )
    def bottom(self):
        return( self.FOIheight / 2.0 )
    def center(self):
        return(0)
    def quadCircle( self, cX , cY, rX, rY, d, d2=0 ):
        self.circle( cX + rX, cY - rY, d, d2 )
        self.circle( cX + rX, cY + rY, d, d2 )
        self.circle( cX - rX, cY - rY, d, d2 )
        self.circle( cX - rX, cY + rY, d, d2 )
    def mmToPxX(self, value):
        # return(value);
        return(value*self.pxPerMmX);
    def mmToPxY(self, value):
        # return(value);
        return(value*self.pxPerMmY);
    def xstr(self, x, addUnit = True ):
        _xstr=str( self.mmToPxX(x) )
        if(addUnit):
            _xstr+=self.unit
        return(_xstr)
    def ystr(self, y, addUnit = True ):
        _ystr=str( self.mmToPxY(y) )
        if(addUnit):
            _ystr+=self.unit
        return(_ystr)
    def triangleHeight(self, a, c ):
         h=math.sqrt( math.pow(a,2) - math.pow(c/2,2) )
         return(h)
    def setStyle(self, style):
         self.style=style
    def wallMount(self, x, y, headSize, coreSize):
         self.plainCircle( x , y , coreSize )
         self.plainCircle( x , y + headSize, headSize )
         self.line( x - (3/2) , y,
                   x - (3/2) , y + headSize )
         self.line( x + (3/2) , y,
                   x + (3/2) , y + headSize )
    def infoBox(self, x, y, a):
        print("Array size: ", len(a))
        maxlen=0
        for e in a:
            print( "Element: ", e)
            maxlen=max(maxlen, len(e))
        width=maxlen * 1.2
        # * self.charSize
        height=( len(a) * self.charSize ) + ( self.textBorder * 2 )
        print("Width: ", width)
        print("Height: ", height)
        self.rect( x, y, width, height )
        self.textCentered(x, y, width, height, a)


#---fin------------------------------------------------------------------------
