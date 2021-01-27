
from collections import namedtuple

Pt = namedtuple("Pt", "x y")

MAXCOORD = 99999999999.9
MINCOORD = -MAXCOORD


#def polar2rect(ang, rad):
#	return POINTS_FORMAT.format(cos(ang) * rad, sin(ang) * rad )

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

class _attrs_struct(object):
	_fields = None # Required -- list to be extended in subclasses
	_subfields = [] # Optional -- list to be extended in subclasses
	def __init__(self, *args, defaults=None) -> None:
		self.set(*args, defaults=defaults) 
	def set(self, *args, defaults=None) -> None:
		for i, fld in enumerate(self._fields):
			if i < len(args):
				setattr(self, fld, str(args[i]))
			else:
				revi = len(self._fields) - i - 1
				if not defaults is None:
					if len(defaults) > revi:
						val = str(defaults[revi])
					else:
						val = str(defaults[-1])
				else:
					val = None
				setattr(self, fld, val)
		if len(self._subfields) > 0:
			if len(self._subfields) == len(args) - len(self._fields):
				for j, sfld in enumerate(self._subfields):
					idx = j + len(self._fields)
					setattr(self, sfld, str(args[idx]))
		return self
	def __repr__(self):
		out = []
		for x in self.__dict__.keys():
			if not x.startswith('_'):
				out.append(f"{x}={getattr(self, x)}")
		return ' '.join(out)
	def setXmlAttrs(self, xmlel) -> None:  
		for f in self._fields:
			xmlel.set(f, str(getattr(self, f)))
		return self
	def getFromXmlAttrs(self, xmlel) -> None:  
		for f in self._fields:
			setattr(self, f, xmlel.get(f))
		return self
	def cloneFrom(self, p_other):
		for l in [self._fields, self._subfields]:
			for fld in l:
				if hasattr(p_other, fld):
					setattr(self, fld, getattr(p_other, fld))
		return self

class _withunits_struct(_attrs_struct):
	def __init__(self, *args, defaults=None) -> None:
		self._units = None
		if not "_units" in self._subfields:
			self._subfields.append("_units")
		super().__init__(*args, defaults=defaults)
		if not self._units is None:
			self._apply_units()
	def _apply_units(self) -> None:
		assert not self._units is None
		assert self._units in ('px', 'pt', 'em', 'rem', '%'), f"invalid units: '{self._units}' not in 'px', 'pt', 'em', 'rem' or '%'"
		for f in self._fields:
			val = getattr(self, f)
			numval = None
			try:
				numval = int(val)
			except ValueError:
				try:
					numval = float(val)
				except ValueError:
					pass
			if not numval is None and numval > 0:
				setattr(self, f, f"{numval}{self._units}")
	def setUnits(self, un: str) -> None:
		self._units = un
		self._apply_units()
	def iterUnitsRemoved(self):
		for f in self._fields:
			val = getattr(self, f)
			if not self._units is None:
				val = val.replace(self._units, '')
			yield val
	def iterUnitsRemoved(self):
		for f in self._fields:
			val = getattr(self, f)
			if not self._units is None:
				val = val.replace(self._units, '')
			yield val

class Env(_attrs_struct):
	_fields = ("minx",  "miny", "maxx", "maxy") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])
	def defFromPointList(self, p_ptlist):
		minx = MAXCOORD
		miny = MAXCOORD
		maxx = MINCOORD
		maxy = MINCOORD
		changed = False
		for pt in p_ptlist:
			changed = True
			if pt.x < minx:
				minx = pt.x
			if pt.y < miny:
				miny = pt.y
			if pt.x > maxx:
				maxx = pt.x
			if pt.y > maxy:
				maxy = pt.y
		if changed:
			self.minx = minx
			self.miny = miny
			self.maxx = maxx
			self.maxy = maxy
	def getWidth(self):
		return float(self.maxx) - float(self.minx)
	def getHeight(self):
		return float(self.maxy) - float(self.miny)
	def getMidPt(self) -> Pt:
		return Pt(self.minx + (self.getWidth() / 2.0),
					self.miny + (self.getHeight() / 2.0))
	def getRectParams(self):
		outlist = []
		outlist.append(self.minx)
		outlist.append(self.miny)
		outlist.append(self.getWidth())
		outlist.append(self.getHeight())
		return outlist
	def cloneFromOther(self, other):
		self.minx = other.minx
		self.miny = other.miny
		self.maxx = other.maxx
		self.maxy = other.maxy
		return self
	def centerAndDims(self, cntPt, dimx, dimy):
		self.minx = cntPt.x - dimx/2.0
		self.miny = cntPt.y - dimy/2.0
		self.maxx = cntPt.x + dimx/2.0
		self.maxy = cntPt.y + dimy/2.0
		return self
	def expandFromOther(self, other):
		if other.minx < self.minx:
			self.minx = other.minx
		if other.miny < self.miny:
			self.miny = other.miny
		if other.maxx > self.maxx:
			self.maxx = other.maxx
		if other.maxy > self.maxy:
			self.maxy = other.maxy
		return self
	def expandFromPoint(self, pt):
		if pt.x < self.minx:
			self.minx = pt.x
		if pt.y < self.miny:
			self.miny = pt.y
		if pt.x > self.maxx:
			self.maxx = pt.x
		if pt.y > self.maxy:
			self.maxy = pt.y
		return self
	def expand(self, ratio):
		pt = self.getMidPt()
		newhwidth = self.getWidth() * ratio * 0.5
		newhheight = self.getHeight() * ratio * 0.5
		self.minx = pt.x - newhwidth 
		self.miny = pt.y - newhheight 
		self.maxx = pt.x + newhwidth 
		self.maxy = pt.y + newhheight 	
		return self


if __name__ == "__main__":
	l = [Pt(0,0), Pt(10,0), Pt(20,12), Pt(6,8)]	
	print(ptList2AbsPolylinePath(l))

	
