
from typing import Optional, Union
from math import sqrt, pow

from rpcbSVG.Basics import Pt, calc3rdPointInSegment, pA, pClose, pL, pM, polar2rectDegs, ptRemoveDecsep, removeDecsep, strictToNumber, toNumberAndUnit
from rpcbSVG.SVGLib import AnalyticalPath, Rect

class Diamond(AnalyticalPath):

	def __init__(self, width, height, handle='cc') -> None:
		super().__init__()
		assert handle in ('cc', 'lc', 'rc', 'cb', 'ct')
		self.dims = (width, height)
		self.handle = handle

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		if self.handle == 'cc':
			self.addCmd(pM(-mw,0))
			self.addCmd(pL(0,-mh))
			self.addCmd(pL(mw,0))
			self.addCmd(pL(0,mh))
			self.addCmd(pClose())
		elif self.handle == 'lc':
			self.addCmd(pM(0,0))
			self.addCmd(pL(mw,-mh))
			self.addCmd(pL(w,0))
			self.addCmd(pL(mw,mh))
			self.addCmd(pClose())
		elif self.handle == 'rc':
			self.addCmd(pM(-w,0))
			self.addCmd(pL(-mw,-mh))
			self.addCmd(pL(0,0))
			self.addCmd(pL(-mw,mh))
			self.addCmd(pClose())
		elif self.handle == 'ct':
			self.addCmd(pM(-mw,mh))
			self.addCmd(pL(0,0))
			self.addCmd(pL(mw,mh))
			self.addCmd(pL(0,h))
			self.addCmd(pClose())
		elif self.handle == 'cb':
			self.addCmd(pM(-mw,-mh))
			self.addCmd(pL(0,-h))
			self.addCmd(pL(mw,-mh))
			self.addCmd(pL(0,0))
			self.addCmd(pClose())

class Cross(AnalyticalPath):

	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		self.addCmd(pM(0,mh))
		self.addCmd(pL(0,-mh))
		self.addCmd(pM(-mw,0))
		self.addCmd(pL(mw,0))

class XSymb(AnalyticalPath):
	
	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		self.addCmd(pM(-mw,-mh))
		self.addCmd(pL(mw,mh))
		self.addCmd(pM(-mw,mh))
		self.addCmd(pL(mw,-mh))

class XSight(AnalyticalPath):
	
	def __init__(self, width, height, separation) -> None:
		super().__init__()
		self.dims = (width, height, separation)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		sep, _u = toNumberAndUnit(self.dims[2])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		ul = Pt(-mw,-mh)
		ll = Pt(-mw,mh)
		ur = Pt(mw,-mh)
		lr = Pt(mw,mh)

		orig = Pt(0,0)
		
		uls = calc3rdPointInSegment(orig, ul, sep)
		lls = calc3rdPointInSegment(orig, ll, sep)
		urs = calc3rdPointInSegment(orig, ur, sep)
		lrs = calc3rdPointInSegment(orig, lr, sep)

		self.addCmd(pM(*ul)).addCmd(pL(*uls))
		self.addCmd(pM(*ll)).addCmd(pL(*lls))
		self.addCmd(pM(*ur)).addCmd(pL(*urs))
		self.addCmd(pM(*lr)).addCmd(pL(*lrs))

class CrossSight(AnalyticalPath):
	
	def __init__(self, width, height, separation: Union[float, int]) -> None:
		super().__init__()
		self.dims = (width, height, separation)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		sep, _u = toNumberAndUnit(self.dims[2])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		t = Pt(0,-mh)
		l = Pt(-mw,0)
		b = Pt(0,mh)
		r = Pt(mw,0)

		orig = Pt(0,0)
		
		ts = calc3rdPointInSegment(orig, t, sep)
		ls = calc3rdPointInSegment(orig, l, sep)
		bs = calc3rdPointInSegment(orig, b, sep)
		rs = calc3rdPointInSegment(orig, r, sep)

		self.addCmd(pM(*t)).addCmd(pL(*ts))
		self.addCmd(pM(*l)).addCmd(pL(*ls))
		self.addCmd(pM(*b)).addCmd(pL(*bs))
		self.addCmd(pM(*r)).addCmd(pL(*rs))

class Square(Rect):
	
	def __init__(self, width) -> None:
		self.width = width
		w, _u = toNumberAndUnit(self.width)
		mw = removeDecsep(w / 2)
		super().__init__(-mw,-mw,w,w)

class Asterisk(AnalyticalPath):
	
	def __init__(self, width, separation: Optional[Union[float, int]] = None) -> None:
		super().__init__()
		self.width = width
		self.separation = separation

	def onAfterParentAdding(self):	

		mw = self.width / 2

		step = 30

		def nextangle(p_ang, halve=False):
			seed = 0
			if halve:
				steps = 360 / p_ang / 2.0
			else:
				steps = 360 / p_ang
			for i in range(round(steps)):
				yield seed + i * p_ang

		if self.separation is None:
			for ang in nextangle(step, halve=True):
				p1 = ptRemoveDecsep(*polar2rectDegs(ang, mw))
				p2 = Pt(-p1.x, -p1.y)
				self.addCmd(pM(*p1)).addCmd(pL(*p2))
		else:
			for ang in nextangle(step):
				p1 = ptRemoveDecsep(*polar2rectDegs(ang, mw))
				p2 = ptRemoveDecsep(*polar2rectDegs(ang, self.separation))
				self.addCmd(pM(*p1)).addCmd(pL(*p2))

class CircAsterisk(Asterisk):
	
	def __init__(self, width, circrad, separation: Optional[Union[float, int]] = None) -> None:
		super().__init__(width, separation=separation)
		self.circrad = circrad

	def onAfterParentAdding(self):	
		super().onAfterParentAdding()
		self.addCmd(pM(-self.circrad,0))
		self.addCmd(pA(self.circrad, self.circrad, 0, 1, 0, self.circrad, 0))
		self.addCmd(pA(self.circrad, self.circrad, 0, 1, 0, -self.circrad, 0))

class Arrow(AnalyticalPath):
	
	def __init__(self, length, basewidth, headwidth, headlength, handle='cc') -> None:
		assert headwidth > basewidth
		assert length > headlength
		assert handle in ('cb', 'cc')
		super().__init__()
		self.dims = (length, basewidth, headwidth, headlength, handle)

	def onAfterParentAdding(self):	
		length, basewidth, headwidth, headlength, handle = self.dims
		baselength = length - headlength
		mw = basewidth / 2
		ml = length / 2
		hmw = headwidth / 2
		hhmw = (headwidth-basewidth) / 2
		if handle == 'cb':
			self.addCmd(pM(mw,0))
			self.addCmd(pL(-mw,0))
			self.addCmd(pL(-mw,-baselength))
			self.addCmd(pL(-hmw,-baselength))
			self.addCmd(pL(0,-length))
			self.addCmd(pL(hmw,headlength, relative=True))
			self.addCmd(pL(-hhmw,0, relative=True))
			self.addCmd(pClose())
		elif handle == 'cc':
			self.addCmd(pM(mw,ml))
			self.addCmd(pL(-mw,ml))
			self.addCmd(pL(0,-baselength, relative=True))
			self.addCmd(pL(-hhmw,0, relative=True))
			self.addCmd(pL(0,-ml))
			self.addCmd(pL(hmw,headlength, relative=True))
			self.addCmd(pL(-hhmw,0, relative=True))
			self.addCmd(pClose())

class CircArrow(Arrow):
	"Only on handle = 'cc'"
	def __init__(self, length, basewidth, headwidth, headlength, coffset: Optional[Union[float, int]] = None) -> None:
		super().__init__(length, basewidth, headwidth, headlength, handle='cc')
		self.coffset = coffset

	def onAfterParentAdding(self):	
		super().onAfterParentAdding()
		length, _basewidth, _headwidth, _headlength, handle = self.dims
		# if handle == 'cb':
		# 	rad = self.coffset + length
		# elif handle == 'cc':
		rad = self.coffset + (length / 2)
		self.addCmd(pM(-rad,0))
		self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
		self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))

class Triangle(AnalyticalPath):
	
	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def onAfterParentAdding(self):	
		w = strictToNumber(self.dims[0])
		h = strictToNumber(self.dims[1])
		mw = removeDecsep(w / 2)

		a = sqrt(pow(h,2) + pow(mw,2))
		s = 0.5 * ((2 * a) + w)

		# r = sqrt(((s-a) * (s-a) * (s - w)) / s) -- inscribed
		R = (a * a * w) / (4 * sqrt(s * (s-a) * (s-a) * (s-w))) # Circunscribed

		self.addCmd(pM(0,-R))
		self.addCmd(pL(-mw,h, relative=True))
		self.addCmd(pL(w,0, relative=True))
		self.addCmd(pClose())

		return R

class CircTriangle(Triangle):

	def __init__(self, width, height, coffset: Optional[Union[float, int]] = None) -> None:
		super().__init__(width, height)
		self.coffset = coffset

	def onAfterParentAdding(self):	
		R = super().onAfterParentAdding()
		rad = self.coffset + R
		self.addCmd(pM(-rad,0))
		self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
		self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))
