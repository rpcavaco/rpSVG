
from typing import Optional
from rpcbSVG.Basics import Pt, calc3rdPointInSegment, pClose, pL, pM, polar2rectDegs, toNumberAndUnit
from rpcbSVG.SVGLib import AnalyticalPath, Group, Rect

class Diamond(Group):

	def __init__(self, width, height, handle='cc') -> None:
		super().__init__()
		assert handle in ('cc', 'lc', 'rc', 'cb', 'ct')
		self.dims = (width, height)
		self.handle = handle

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = w / 2
		mh = h / 2

		ap = self.addChild(AnalyticalPath())
		if self.handle == 'cc':
			ap.addCmd(pM(-mw,0))
			ap.addCmd(pL(0,-mh))
			ap.addCmd(pL(mw,0))
			ap.addCmd(pL(0,mh))
			ap.addCmd(pClose())
		elif self.handle == 'lc':
			ap.addCmd(pM(0,0))
			ap.addCmd(pL(mw,-mh))
			ap.addCmd(pL(w,0))
			ap.addCmd(pL(mw,mh))
			ap.addCmd(pClose())
		elif self.handle == 'rc':
			ap.addCmd(pM(-w,0))
			ap.addCmd(pL(-mw,-mh))
			ap.addCmd(pL(0,0))
			ap.addCmd(pL(-mw,mh))
			ap.addCmd(pClose())
		elif self.handle == 'ct':
			ap.addCmd(pM(-mw,mh))
			ap.addCmd(pL(0,0))
			ap.addCmd(pL(mw,mh))
			ap.addCmd(pL(0,h))
			ap.addCmd(pClose())
		elif self.handle == 'cb':
			ap.addCmd(pM(-mw,-mh))
			ap.addCmd(pL(0,-h))
			ap.addCmd(pL(mw,-mh))
			ap.addCmd(pL(0,0))
			ap.addCmd(pClose())

class Cross(Group):

	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = w / 2
		mh = h / 2

		ap = self.addChild(AnalyticalPath())
		ap.addCmd(pM(0,mh))
		ap.addCmd(pL(0,-mh))
		ap.addCmd(pM(-mw,0))
		ap.addCmd(pL(mw,0))

class XSymb(Group):
	
	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = w / 2
		mh = h / 2

		ap = self.addChild(AnalyticalPath())
		ap.addCmd(pM(-mw,-mh))
		ap.addCmd(pL(mw,mh))
		ap.addCmd(pM(-mw,mh))
		ap.addCmd(pL(mw,-mh))

class XSight(Group):
	
	def __init__(self, width, height, separation) -> None:
		super().__init__()
		self.dims = (width, height, separation)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		sep, _u = toNumberAndUnit(self.dims[2])
		mw = w / 2
		mh = h / 2

		ul = Pt(-mw,-mh)
		ll = Pt(-mw,mh)
		ur = Pt(mw,-mh)
		lr = Pt(mw,mh)

		orig = Pt(0,0)
		
		uls = calc3rdPointInSegment(orig, ul, sep)
		lls = calc3rdPointInSegment(orig, ll, sep)
		urs = calc3rdPointInSegment(orig, ur, sep)
		lrs = calc3rdPointInSegment(orig, lr, sep)

		ap = self.addChild(AnalyticalPath())
		ap.addCmd(pM(*ul)).addCmd(pL(*uls))
		ap.addCmd(pM(*ll)).addCmd(pL(*lls))
		ap.addCmd(pM(*ur)).addCmd(pL(*urs))
		ap.addCmd(pM(*lr)).addCmd(pL(*lrs))

class CrossSight(Group):
	
	def __init__(self, width, height, separation) -> None:
		super().__init__()
		self.dims = (width, height, separation)

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		sep, _u = toNumberAndUnit(self.dims[2])
		mw = w / 2
		mh = h / 2

		t = Pt(0,-mh)
		l = Pt(-mw,0)
		b = Pt(0,mh)
		r = Pt(mw,0)

		orig = Pt(0,0)
		
		ts = calc3rdPointInSegment(orig, t, sep)
		ls = calc3rdPointInSegment(orig, l, sep)
		bs = calc3rdPointInSegment(orig, b, sep)
		rs = calc3rdPointInSegment(orig, r, sep)

		ap = self.addChild(AnalyticalPath())
		ap.addCmd(pM(*t)).addCmd(pL(*ts))
		ap.addCmd(pM(*l)).addCmd(pL(*ls))
		ap.addCmd(pM(*b)).addCmd(pL(*bs))
		ap.addCmd(pM(*r)).addCmd(pL(*rs))

class Square(Group):
	
	def __init__(self, width) -> None:
		super().__init__()
		self.width = width

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.width)
		mw = w / 2

		self.addChild(Rect(-mw,-mw,w,w))

class Asterisk(Group):
	
	def __init__(self, width, separation=Optional[] = None) -> None:
		super().__init__()
		self.width = width

	def onAfterParentAdding(self):	
		w, _u = toNumberAndUnit(self.width)
		mw = w / 2

		step = 30

		def nextangle(p_ang):
			seed = 0
			steps = 360 / p_ang / 2.0
			for i in range(round(steps)):
				yield seed + i * p_ang

		ap = self.addChild(AnalyticalPath())
		for ang in nextangle(step):
			p1 = polar2rectDegs(ang, mw)
			p2 = Pt(-p1.x, -p1.y)
			ap.addCmd(pM(*p1)).addCmd(pL(*p2))



