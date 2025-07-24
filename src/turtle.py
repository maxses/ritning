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


class Turtle():

	def __init__( self, host, x, y ):
		self.host = host
		# "style=\"fill:#c200c2;fill-opacity:0;stroke:#c200c2;stroke-width:0.09999994;stroke-linecap:round;stroke-linejoin:round;stroke-opacity:1\" \n"
		host.outFile.write(
			# "<g id=\"layer1\">\n"
			 "<path\n"
				 "style=\"" + host.style + "\" \n"
				 "d=\"m " + host.xstr( host.centerX + host.FOIx + x, False ) + ","
							 + host.ystr( host.centerY + host.FOIy + y, False ) + " l")
		self.tx=x
		self.ty=y
	def finish(self):
		self.host.outFile.write( "\"\n"
				 # "id=\"path630\" />\n" )
				 "id=\"path" + str( self.host.runningId ) + "\" "
				 "/>\n" )
		self.host.runningId+=1
		# self.host.outFile.write( "</g>\n" )

	def u(self,n):
		self.d(-n)
		return self

	def d(self, n):
		self.host.outFile.write( " 0," + self.host.xstr(n, False) );
		self.ty+=n
		return self

	def l(self,n):
		self.r(-n)
		return self

	def r(self, n):
		self.host.outFile.write( " " + self.host.xstr(n, False) + ",0" );
		self.tx+=n
		return self

	def expect(self, x, y):
		if not self.tx==x:
			 print( "X: " + str( self.tx ) + " != " + str(x) + "(should)" )
		if not self.ty==y:
			print( "Y: " + str( self.ty ) + " != " + str(y) + "(should)" )
		assert self.tx==x
		assert self.ty==y
		return self


#---fin------------------------------------------------------------------------
