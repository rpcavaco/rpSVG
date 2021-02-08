
from typing import Optional, Union
from rpcbSVG.Basics import Pt, calc3rdPointInSegment, pA, pClose, pL, pM, polar2rectDegs, ptRemoveDecsep, removeDecsep, toNumberAndUnit
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
		self.addCmd(pA())

