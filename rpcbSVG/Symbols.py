
from typing import Optional, Union
from math import sqrt, pow

from rpcbSVG.Basics import Pt, calc3rdPointInSegment, circleDividers, pA, pClose, pL, pM, polar2rectDegs, ptRemoveDecsep, removeDecsep, strictToNumber, toNumberAndUnit
from rpcbSVG.SVGLib import AnalyticalPath, Group, Rect

class Diamond(AnalyticalPath):

	def __init__(self, width, height, handle='cc') -> None:
		super().__init__()
		assert handle in ('cc', 'lc', 'rc', 'cb', 'ct')
		self.dims = (width, height)
		self.handle = handle

	def getComment(self):
		return f"Diamond symbol, dims:{self.dims} handle:{self.handle}"

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

	def getComment(self):
		return f"Cross symbol, dims:{self.dims}"

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

	def getComment(self):
		return f"XSymb symbol, dims:{self.dims}"

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

	def getComment(self):
		return f"XSight symbol, dims:{self.dims}"

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

	def getComment(self):
		return f"CrossSight symbol, dims:{self.dims}"

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

	def getComment(self):
		return f"Square symbol, width:{self.width}"

class Asterisk(AnalyticalPath):
	
	def __init__(self, width, separation: Optional[Union[float, int]] = None) -> None:
		super().__init__()
		self.width = width
		self.separation = separation

	def getComment(self):
		return f"Asterisk symbol, width:{self.width} separation:{self.separation}"

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

	def getComment(self):		
		return f"{super().getComment()}, CircAsterisk, circrad:{self.circrad}"

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

	def getComment(self):		
		return f"Arrow, dims:{self.dims}"

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

	def getComment(self):		
		return f"{super().getComment()}, CircArrow, coffset:{self.coffset}"

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

class Wedge(AnalyticalPath):
	
	def __init__(self, width, height, indent: Optional[Union[float, int]] = 0) -> None:
		super().__init__()
		self.dims = (width, height, indent)

	def getComment(self):		
		return f"Wedge, dims:{self.dims}"

	def onAfterParentAdding(self):	
		w = strictToNumber(self.dims[0])
		h = strictToNumber(self.dims[1])
		i = strictToNumber(self.dims[2])
		mw = removeDecsep(w / 2)

		a = sqrt(pow(h,2) + pow(mw,2))
		s = 0.5 * ((2 * a) + w)

		# r = sqrt(((s-a) * (s-a) * (s - w)) / s) -- inscribed
		R = (a * a * w) / (4 * sqrt(s * (s-a) * (s-a) * (s-w))) # Circunscribed

		self.addCmd(pM(0,-R))
		self.addCmd(pL(-mw,h, relative=True))
		if i != 0:
			self.addCmd(pL(mw,-i, relative=True))
			self.addCmd(pL(mw,i, relative=True))
		else:
			self.addCmd(pL(w,0, relative=True))
		self.addCmd(pClose())

		return R

class CircWedge(Wedge):

	def __init__(self, width, height, indent: Optional[Union[float, int]] = 0, coffset: Optional[Union[float, int]] = None) -> None:
		super().__init__(width, height, indent=indent)
		self.coffset = coffset

	def getComment(self):		
		return f"{super().getComment()}, CircWedge, coffset:{self.coffset}"

	def onAfterParentAdding(self):	
		R = super().onAfterParentAdding()
		rad = self.coffset + R
		self.addCmd(pM(-rad,0))
		self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
		self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))

class Crescent(AnalyticalPath):

	def __init__(self, p_radius) -> None:

		super().__init__()
		self.radius = strictToNumber(p_radius)

	def getComment(self):		
		return f"Crescent, radius:{self.radius}"

	def onAfterParentAdding(self):	
		
		ang = 95
		rad2 = self.radius+4
		p1 = polar2rectDegs(ang, self.radius)
		p2 = polar2rectDegs(-ang, self.radius)

		self.addCmd(pM(*p1))
		self.addCmd(pA(self.radius, self.radius, 0, 1, 0, *p2))
		self.addCmd(pM(*p1))
		self.addCmd(pA(rad2, rad2, 0, 0, 0, *p2))

		ang2 = 100
		p3 = polar2rectDegs(ang2, self.radius)
		p4 = polar2rectDegs(-ang2, self.radius)

		self.addCmd(pM(*p3))
		self.addCmd(pA(self.radius, self.radius, 0, 0, 1, *p4))

class SuspPointCirc(AnalyticalPath):

	def __init__(self, p_radius) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)

	def getComment(self):		
		return f"SuspPointCirc, radius:{self.radius}"

	def onAfterParentAdding(self):	
		
		p1 = polar2rectDegs(0, self.radius)
		p2 = polar2rectDegs(270, self.radius)
		self.addCmd(pM(*p1))
		self.addCmd(pA(self.radius, self.radius, 0, 0, 0, *p2))
		self.addCmd(pL(0,0))
		self.addCmd(pClose())
		
		p3 = polar2rectDegs(180, self.radius)
		p4 = polar2rectDegs(90, self.radius)
		self.addCmd(pM(*p3))
		self.addCmd(pA(self.radius, self.radius, 0, 0, 0, *p4))
		self.addCmd(pL(0,0))
		self.addCmd(pClose())
		
		p5 = polar2rectDegs(190, self.radius)
		p6 = polar2rectDegs(260, self.radius)
		self.addCmd(pM(*p5))
		self.addCmd(pA(self.radius, self.radius, 0, 0, 1, *p6))
		
		p7 = polar2rectDegs(10, self.radius)
		p8 = polar2rectDegs(80, self.radius)
		self.addCmd(pM(*p7))
		self.addCmd(pA(self.radius, self.radius, 0, 0, 1, *p8))

class SuspPointSquare(AnalyticalPath):

	def __init__(self, p_radius) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)

	def getComment(self):		
		return f"SuspPointSquare, radius:{self.radius}"

	def onAfterParentAdding(self):	
		
		p1 = polar2rectDegs(-45, self.radius)
		self.addCmd(pM(*p1))
		self.addCmd(pL(-p1.x, 0, relative=True))
		self.addCmd(pL(0, 0))
		self.addCmd(pL(p1.x, 0))
		self.addCmd(pClose())
		
		p2 = polar2rectDegs(135, self.radius)
		self.addCmd(pM(*p2))
		self.addCmd(pL(-p2.x, 0, relative=True))
		self.addCmd(pL(0, 0))
		self.addCmd(pL(p2.x, 0))
		self.addCmd(pClose())

		self.addCmd(pM(p2.x, -3))
		self.addCmd(pL(p2.x, p1.y))
		self.addCmd(pL(-3, p1.y))

		self.addCmd(pM(3, p2.y))
		self.addCmd(pL(p1.x, p2.y))
		self.addCmd(pL(p1.x, 3))

class SuspPointTriang(AnalyticalPath):

	def __init__(self, p_radius) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)
		self.interval = 3

	def getComment(self):		
		return f"SuspPointTriang, radius:{self.radius}"

	def onAfterParentAdding(self):	
		
		pt = polar2rectDegs(270, self.radius)
		pl = polar2rectDegs(150, self.radius)
		pr = polar2rectDegs(30, self.radius)

		h = pl.y - pt.y
		b = pr.x - pl.x
		mb = b / 2
		rat = mb / h 
		l0 = pt.y * rat 
		l0t = (-self.interval + pt.y) * rat 
		l0b = (self.interval + pt.y) * rat
		tb = self.interval * rat

		self.addCmd(pM(*pl))
		self.addCmd(pL(-pl.x, 0, relative=True))
		self.addCmd(pL(0, 0))
		self.addCmd(pL(l0, 0))
		self.addCmd(pClose())

		self.addCmd(pM(0,0))
		self.addCmd(pL(-l0,0))
		self.addCmd(pL(*pt))
		self.addCmd(pClose())

		self.addCmd(pM(3,pl.y))
		self.addCmd(pL(*pr))
		self.addCmd(pL(-l0t,self.interval)) 

		self.addCmd(pM(-tb,pt.y+self.interval)) # --> replace
		self.addCmd(pL(l0b,-self.interval)) 

class Star(AnalyticalPath):

	def __init__(self, p_outradius, p_inoffset, p_nspikes, rot: Optional[Union[float, int]] = 0) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_outradius)
		self.offset = strictToNumber(p_inoffset)
		self.nspikes = strictToNumber(p_nspikes)
		self.rot = strictToNumber(rot)

	def getComment(self):		
		return f"Star, radius:{self.radius}, nspikes:{self.nspikes}, rot:{self.rot}"

	def onAfterParentAdding(self):	

		step = 360 / self.nspikes
		rot = self.rot - 90 # 0 is vertical
		hstep = step / 2
		first = True
		ct = Pt(0,0)

		opts = list(circleDividers(ct, self.radius, self.nspikes, rot))
		ipts = list(circleDividers(ct, self.radius-self.offset, self.nspikes, rot+hstep))

		for i, opt in enumerate(opts):
			ipt = ipts[i]
			if first:
				self.addCmd(pM(*opt))
			else:
				self.addCmd(pL(*opt))

			self.addCmd(pL(*ipt))

			first = False

		if not first:
			self.addCmd(pClose())

class RegPoly(AnalyticalPath):

	def __init__(self, p_radius, p_n, rot: Optional[Union[float, int]] = 0) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)
		self.n = strictToNumber(p_n)
		self.rot = strictToNumber(rot)

	def getComment(self):		
		return f"RegPoly, radius:{self.radius}, n:{self.n}, rot:{self.rot}"

	def onAfterParentAdding(self):	

		step = 360 / self.n
		rot = self.rot - 90 # 0 is vertical
		hstep = step / 2
		first = True
		ct = Pt(0,0)

		opts = list(circleDividers(ct, self.radius, self.n, rot))

		for i, opt in enumerate(opts):
			if first:
				self.addCmd(pM(*opt))
			else:
				self.addCmd(pL(*opt))
			first = False

		if not first:
			self.addCmd(pClose())

			
