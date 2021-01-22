
from collections import namedtuple

Pt = namedtuple("Pt", "x y")


class EnvGeom(object):
	def __init__(self, p_env):
		self.minx = p_env.minx
		self.miny = p_env.miny
		self.maxx = p_env.maxx
		self.maxy = p_env.maxy
	def getMidPt(self, outpt):
		outpt.x = self.minx + (self.getWidth() / 2.0)
		outpt.y = self.miny + (self.getHeight() / 2.0)
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


def ptList2AbsPolylinePath(p_ptlist, mirrory=False, close=False):
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
	print(ptList2AbsPolylinePath(l))

	
