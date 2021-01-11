
from collections import namedtuple

Pt = namedtuple("Pt", "x y")


class Envelope(object):
	def __init__(self):
		self.minx = 0
		self.miny = 0
		self.maxx = 0
		self.maxy = 0
	def origAndDims(self, pt, width, height):
		self.minx = pt.x
		self.miny = pt.y
		self.maxx = pt.x + width
		self.maxy = pt.y + height
	def getWidth(self):
		return self.maxx - self.minx
	def getHeight(self):
		return self.maxy - self.miny
	def getRectParams(self, outlist):
		del outlist[:]
		outlist.append(self.minx)
		outlist.append(self.miny)
		outlist.append(self.getWidth())
		outlist.append(self.getHeight())
	def getMidPt(self, outpt):
		outpt.x = self.minx + (self.getWidth() / 2.0)
		outpt.y = self.miny + (self.getHeight() / 2.0)
	def cloneFromOther(self, other):
		self.minx = other.minx
		self.miny = other.miny
		self.maxx = other.maxx
		self.maxy = other.maxy
	def expandFromOther(self, other):
		if other.minx < self.minx:
			self.minx = other.minx
		if other.miny < self.miny:
			self.miny = other.miny
		if other.maxx > self.maxx:
			self.maxx = other.maxx
		if other.maxy > self.maxy:
			self.maxy = other.maxy
	def expandFromPoint(self, pt):
		if pt.x < self.minx:
			self.minx = pt.x
		if pt.y < self.miny:
			self.miny = pt.y
		if pt.x > self.maxx:
			self.maxx = pt.x
		if pt.y > self.maxy:
			self.maxy = pt.y
	def expand(self, ratio):
		pt = Pt()
		self.getMidPt(pt)
		newhwidth = self.getWidth() * ratio * 0.5
		newhheight = self.getHeight() * ratio * 0.5
		self.minx = pt.x - newhwidth 
		self.miny = pt.y - newhheight 
		self.maxx = pt.x + newhwidth 
		self.maxy = pt.y + newhheight 	
	def extractFromPointlist(self, inlist, mirrory=False):
		for pt in inlist:
			if mirrory:
				pt.y = -pt.y
			if pt.x < self.minx:
				self.minx = pt.x
			if pt.y < self.miny:
				self.miny = pt.y
			if pt.x > self.maxx:
				self.maxx = pt.x
			if pt.y > self.maxy:
				self.maxy = pt.y

def list2AbsPolylinePath(p_ptlist, mirrory=False, close=False):
	strcomps = []
	for pi, pt in enumerate(p_ptlist):
		if mirrory:
			pt.y = -pt.y
		if pi == 0:
			strcomps.append("M{0:.4f} {1:.4f}".format(*pt))
		elif pi == 1:
			strcomps.append("L{0:.4f} {1:.4f}".format(*pt))
		else:
			strcomps.append(" {0:.4f} {1:.4f}".format(*pt))
	if close:
		strcomps.append(" z")
	return "".join(strcomps)	
	
if __name__ == "__main__":
	l = [Pt(0,0), Pt(10,0), Pt(20,12), Pt(6,8)]	
	print(list2AbsPolylinePath(l))

	
