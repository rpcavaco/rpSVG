
from rpSVG.Structs import Re, VBox
from rpSVG.SVGStyleText import Sty
from typing import Optional, Union
from math import cos, radians, sin, sqrt, pow

from rpSVG.Basics import Pt, Trans, calc3rdPointInLine, circleDividers, glRd, pA, pClose, pL, pM, polar2rectDegs, ptAdd, ptRemoveDecsep, removeDecsep, strictToNumber, toNumberAndUnit
from rpSVG.SVGLib import AnalyticalPath, Desc, Rect, Symbol

class Diamond(AnalyticalPath):

	def __init__(self, width=0, height=0, x=0, y=0, handle='cc') -> None:			
		assert handle in ('cc', 'lc', 'rc', 'cb', 'ct')
		super().__init__()
		self.dims = (width, height)
		self.handle = handle
		self.xv, _u = toNumberAndUnit(x)
		self.yv, _u = toNumberAndUnit(y)
	
	def getComment(self):
		return f"Diamond symbol, dims:{self.dims} x:{self.xv} y:{self.yv} handle:{self.handle}"

	def setDims(self, p_re: Re):
		vals = p_re.getValues()
		self.dims = (vals[0], vals[1])
		self.xv = vals[2]
		self.yv = vals[3]

	def build(self):
		self.clearTransforms()
		self.clear()
		if self.xv != 0 or self.yv != 0:
			self.addTransform(Trans(self.xv,self.yv))
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

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		self.build()

class Cross(AnalyticalPath):

	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def getComment(self):
		return f"Cross symbol, dims:{self.dims}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		self.addCmd(pM(0,mh))
		self.addCmd(pL(0,-mh))
		self.addCmd(pM(-mw,0))
		self.addCmd(pL(mw,0))
		self.refresh()

class XSymb(AnalyticalPath):
	
	def __init__(self, width, height) -> None:
		super().__init__()
		self.dims = (width, height)

	def getComment(self):
		return f"XSymb symbol, dims:{self.dims}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		w, _u = toNumberAndUnit(self.dims[0])
		h, _u = toNumberAndUnit(self.dims[1])
		mw = removeDecsep(w / 2)
		mh = removeDecsep(h / 2)

		self.addCmd(pM(-mw,-mh))
		self.addCmd(pL(mw,mh))
		self.addCmd(pM(-mw,mh))
		self.addCmd(pL(mw,-mh))
		self.refresh()

class XSight(AnalyticalPath):
	
	def __init__(self, width, height, separation) -> None:
		super().__init__()
		self.dims = (width, height, separation)

	def getComment(self):
		return f"XSight symbol, dims:{self.dims}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
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
		
		uls = calc3rdPointInLine(orig, ul, sep)
		lls = calc3rdPointInLine(orig, ll, sep)
		urs = calc3rdPointInLine(orig, ur, sep)
		lrs = calc3rdPointInLine(orig, lr, sep)

		self.addCmd(pM(*ul)).addCmd(pL(*uls))
		self.addCmd(pM(*ll)).addCmd(pL(*lls))
		self.addCmd(pM(*ur)).addCmd(pL(*urs))
		self.addCmd(pM(*lr)).addCmd(pL(*lrs))
		self.refresh()

class CrossSight(AnalyticalPath):
	
	def __init__(self, width, height, separation: Union[float, int]) -> None:
		super().__init__()
		self.dims = (width, height, separation)

	def getComment(self):
		return f"CrossSight symbol, dims:{self.dims}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
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
		
		ts = calc3rdPointInLine(orig, t, sep)
		ls = calc3rdPointInLine(orig, l, sep)
		bs = calc3rdPointInLine(orig, b, sep)
		rs = calc3rdPointInLine(orig, r, sep)

		self.addCmd(pM(*t)).addCmd(pL(*ts))
		self.addCmd(pM(*l)).addCmd(pL(*ls))
		self.addCmd(pM(*b)).addCmd(pL(*bs))
		self.addCmd(pM(*r)).addCmd(pL(*rs))
		self.refresh()

class Square(Rect):
	
	def __init__(self, width) -> None:
		self.width = width
		w, _u = toNumberAndUnit(self.width)
		mw = removeDecsep(w / 2)
		super().__init__(-mw,-mw,w,w)

	def getComment(self):
		return f"Square symbol, width:{self.width}"

class Asterisk(AnalyticalPath):
	
	def __init__(self, p_radius, separation: Optional[Union[float, int]] = None) -> None:
		super().__init__()
		self.radius = p_radius
		self.separation = separation

	def getComment(self):
		return f"Asterisk symbol, width:{self.radius} separation:{self.separation}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return False

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
				p1 = ptRemoveDecsep(*polar2rectDegs(ang, self.radius))
				p2 = Pt(-p1.x, -p1.y)
				self.addCmd(pM(*p1)).addCmd(pL(*p2))
		else:
			for ang in nextangle(step):
				p1 = ptRemoveDecsep(*polar2rectDegs(ang, self.radius))
				p2 = ptRemoveDecsep(*polar2rectDegs(ang, self.separation))
				self.addCmd(pM(*p1)).addCmd(pL(*p2))
		self.refresh()

		return True

class CircAsterisk(Asterisk):
	
	def __init__(self, p_radius, circrad, separation: Optional[Union[float, int]] = None) -> None:
		super().__init__(p_radius, separation=separation)
		self.circrad = circrad

	def getComment(self):		
		return f"{super().getComment()}, CircAsterisk, circrad:{self.circrad}"

	def onAfterParentAdding(self, defselement=None):	
		if super().onAfterParentAdding():
			self.addCmd(pM(-self.circrad,0))
			self.addCmd(pA(self.circrad, self.circrad, 0, 1, 0, self.circrad, 0))
			self.addCmd(pA(self.circrad, self.circrad, 0, 1, 0, -self.circrad, 0))
			self.refresh()

class Arrow(AnalyticalPath):
	
	def __init__(self, length, basewidth, headwidth, headlength, handle='cc') -> None:
		assert headwidth > basewidth
		assert length > headlength
		assert handle in ('cb', 'cc')
		super().__init__()
		self._rhr = True
		self.dims = (length, basewidth, headwidth, headlength, handle)

	def getComment(self):		
		return f"Arrow, dims:{self.dims}"

	def changeFillRule(self, filled=True):
		self._rhr = filled

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return False
		length, basewidth, headwidth, headlength, handle = self.dims
		baselength = length - headlength
		mw = basewidth / 2
		ml = length / 2
		hmw = headwidth / 2
		hhmw = (headwidth-basewidth) / 2
		if handle == 'cb':
			if self._rhr:
				self.addCmd(pM(0,-length))
				self.addCmd(pL(-hmw,headlength, relative=True))
				self.addCmd(pL(hhmw,0, relative=True))
				self.addCmd(pL(0,baselength, relative=True))
				self.addCmd(pL(basewidth,0, relative=True))
				self.addCmd(pL(0,-baselength, relative=True))
				self.addCmd(pL(hhmw,0, relative=True))
				self.addCmd(pClose())
			else: # Filled = False	
				self.addCmd(pM(0,-length))
				self.addCmd(pL(hmw,headlength, relative=True))
				self.addCmd(pL(-hhmw,0, relative=True))
				self.addCmd(pL(0,baselength, relative=True))
				self.addCmd(pL(-basewidth,0, relative=True))
				self.addCmd(pL(0,-baselength, relative=True))
				self.addCmd(pL(-hhmw,0, relative=True))
				self.addCmd(pClose())
		elif handle == 'cc':
			if self._rhr:
				self.addCmd(pM(0,-ml))
				self.addCmd(pL(-hmw,headlength, relative=True))
				self.addCmd(pL(hhmw,0, relative=True))
				self.addCmd(pL(0,baselength, relative=True))
				self.addCmd(pL(basewidth,0, relative=True))
				self.addCmd(pL(0, -baselength, relative=True))
				self.addCmd(pL(hhmw,0, relative=True))
				self.addCmd(pClose())
			else: # Filled = False				
				self.addCmd(pM(0,-ml))
				self.addCmd(pL(hmw,headlength, relative=True))
				self.addCmd(pL(-hhmw,0, relative=True))
				self.addCmd(pL(mw,ml))
				self.addCmd(pL(-basewidth,0, relative=True))
				self.addCmd(pL(0,-baselength, relative=True))
				self.addCmd(pL(-hhmw,0, relative=True))
				self.addCmd(pClose())

		return True

class CircArrow(Arrow):
	"Only on arrow handle = 'cc'"
	def __init__(self, length, basewidth, headwidth, headlength, coffset: Optional[Union[float, int]] = None) -> None:
		super().__init__(length, basewidth, headwidth, headlength, handle='cc')
		self.coffset = coffset

	def getComment(self):		
		return f"{super().getComment()}, CircArrow, coffset:{self.coffset}"

	def onAfterParentAdding(self, defselement=None):	
		self.changeFillRule(filled=False)
		if super().onAfterParentAdding():

			length = self.dims[0]
			rad = self.coffset + (length / 2)

			self.addCmd(pM(-rad,0))
			self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
			self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))
			self.refresh()

class SquaredArrow(Arrow):
	"Only on arrow handle = 'cc'"
	def __init__(self, length, basewidth, headwidth, headlength, coffset: Optional[Union[float, int]] = None) -> None:
		super().__init__(length, basewidth, headwidth, headlength, handle='cc')
		self.coffset = coffset

	def getComment(self):		
		return f"{super().getComment()}, CircArrow, coffset:{self.coffset}"

	def onAfterParentAdding(self, defselement=None):	
		self.changeFillRule(filled=False)
		if super().onAfterParentAdding():

			length = self.dims[0]
			rad = self.coffset + (length / 2)

			self.addCmd(pM(rad,rad))
			self.addCmd(pL(rad,-rad))
			self.addCmd(pL(-rad,-rad))
			self.addCmd(pL(-rad,rad))
			self.addCmd(pClose())

class Wedge(AnalyticalPath):
	
	def __init__(self, width, height, indent: Optional[Union[float, int]] = 0) -> None:
		super().__init__()
		self.dims = (width, height, indent)
		self._rhr = True

	def getComment(self):		
		return f"Wedge, dims:{self.dims}"

	def changeFillRule(self, filled=True):
		self._rhr = filled

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return -1
		w = strictToNumber(self.dims[0])
		h = strictToNumber(self.dims[1])
		i = strictToNumber(self.dims[2])
		mw = removeDecsep(w / 2)

		a = sqrt(pow(h,2) + pow(mw,2))
		s = 0.5 * ((2 * a) + w)

		# r = sqrt(((s-a) * (s-a) * (s - w)) / s) -- inscribed
		R = (a * a * w) / (4 * sqrt(s * (s-a) * (s-a) * (s-w))) # Circunscribed

		pt = Pt(0,-R)

		self.addCmd(pM(*pt))
		if self._rhr:
			self.addCmd(pL(-mw,h, relative=True))
			if i != 0:
				self.addCmd(pL(mw,-i, relative=True))
				self.addCmd(pL(mw,i, relative=True))
			else:
				self.addCmd(pL(w,0, relative=True))
		else:
			self.addCmd(pL(mw,h, relative=True))
			if i != 0:
				self.addCmd(pL(-mw,-i, relative=True))
				self.addCmd(pL(-mw,i, relative=True))
			else:
				self.addCmd(pL(-w,0, relative=True))
		self.addCmd(pClose())

		return R

class CircWedge(Wedge):

	def __init__(self, width, height, indent: Optional[Union[float, int]] = 0, coffset: Optional[Union[float, int]] = None) -> None:
		super().__init__(width, height, indent=indent)
		self.coffset = coffset

	def getComment(self):		
		return f"{super().getComment()}, CircWedge, coffset:{self.coffset}"

	def onAfterParentAdding(self, defselement=None):	
		self.changeFillRule(filled=False)
		R = super().onAfterParentAdding()
		if R < 0:
			return
		rad = self.coffset + R
		self.addCmd(pM(-rad,0))
		self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
		self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))
		self.refresh()

class Crescent(Symbol):

	def __init__(self, p_radius) -> None:

		super().__init__()
		self.radius = strictToNumber(p_radius)

	def getComment(self):		
		return f"Crescent, radius:{self.radius}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return

		self.addChild(Desc().setText(self.getComment()))
		ap = self.addChild(AnalyticalPath())
		
		ang = 92
		rad2 = self.radius+4
		p1 = polar2rectDegs(ang, self.radius)
		p2 = polar2rectDegs(-ang, self.radius)

		ap.addCmd(pM(*p1))
		ap.addCmd(pA(self.radius, self.radius, 0, 1, 0, *p2))
		ap.addCmd(pM(*p2))
		ap.addCmd(pA(rad2, rad2, 0, 0, 1, *p1))
		ap.refresh()

		ap2 = self.addChild(AnalyticalPath().setStyle(Sty('fill', 'none')))

		ap2.addCmd(pM(*p1))
		ap2.addCmd(pA(self.radius, self.radius, 0, 0, 1, *p2))
		ap2.refresh()

		offset = 2
		minx = -self.radius-offset
		maxx = self.radius+offset
		wid = maxx - minx
		miny = minx
		hei = wid

		self.setViewbox(VBox(minx, miny, wid, hei))
		self.use_dims = (minx, miny, wid, hei)

	def yinvert(self, p_height: Union[float, int]):
		self._yinverting = True

class SuspPointCirc(Symbol):

	def __init__(self, p_radius) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)
		self.use_dims = (0,0,0,0)

	def getUseDims(self):
		return self.use_dims

	def getComment(self):		
		return f"SuspPointCirc, radius:{self.radius}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return

		self.addChild(Desc().setText(self.getComment()))
		ap = self.addChild(AnalyticalPath())
		
		p1 = polar2rectDegs(0, self.radius)
		p2 = polar2rectDegs(270, self.radius)
		ap.addCmd(pM(*p1))
		ap.addCmd(pA(self.radius, self.radius, 0, 0, 0, *p2))
		ap.addCmd(pL(0,0))
		ap.addCmd(pClose())
		
		p3 = polar2rectDegs(180, self.radius)
		p4 = polar2rectDegs(90, self.radius)
		ap.addCmd(pM(*p3))
		ap.addCmd(pA(self.radius, self.radius, 0, 0, 0, *p4))
		ap.addCmd(pL(0,0))
		ap.addCmd(pClose())
		
		ap2 = self.addChild(AnalyticalPath().setStyle(Sty('fill', 'none')))		
		ap2.addCmd(pM(*p3))
		ap2.addCmd(pA(self.radius, self.radius, 0, 0, 1, *p2))

		ap2.addCmd(pM(*p1))
		ap2.addCmd(pA(self.radius, self.radius, 0, 0, 1, *p4))
		ap2.refresh()

		offset = 2
		minx = p3.x-offset
		maxx = p1.x+offset
		wid = maxx - minx
		miny = p2.y-offset
		maxy = p4.y+offset
		hei = maxy-miny

		self.setViewbox(VBox(minx, miny, wid, hei))
		self.use_dims = (minx, miny, wid, hei)

	def yinvert(self, p_height: Union[float, int]):
		self._yinverting = True

class SuspPointSquare(Symbol):

	def __init__(self, p_radius) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)
		self.use_dims = (0,0,0,0)

	def getUseDims(self):
		return self.use_dims

	def getComment(self):		
		return f"SuspPointSquare, radius:{self.radius}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return

		self.addChild(Desc().setText(self.getComment()))
		ap = self.addChild(AnalyticalPath())
		
		p1 = polar2rectDegs(-45, self.radius)
		ap.addCmd(pM(*p1))
		ap.addCmd(pL(-p1.x, 0, relative=True))
		ap.addCmd(pL(0, 0))
		ap.addCmd(pL(p1.x, 0))
		ap.addCmd(pClose())
		
		p2 = polar2rectDegs(135, self.radius)
		ap.addCmd(pM(*p2))
		ap.addCmd(pL(-p2.x, 0, relative=True))
		ap.addCmd(pL(0, 0))
		ap.addCmd(pL(p2.x, 0))
		ap.addCmd(pClose())

		ap2 = self.addChild(AnalyticalPath().setStyle(Sty('fill', 'none')))
		
		ap2.addCmd(pM(*p2))
		ap2.addCmd(pL(p2.x, p1.y))
		ap2.addCmd(pL(0, p1.y))

		ap2.addCmd(pM(0, p2.y))
		ap2.addCmd(pL(p1.x, p2.y))
		ap2.addCmd(pL(p1.x, 0))
		ap2.refresh()

		offset = 2
		minx = p2.x-offset
		maxx = p1.x+offset
		wid = maxx - minx
		miny = p1.y-offset
		maxy = p2.y+offset
		hei = maxy-miny

		self.setViewbox(VBox(minx, miny, wid, hei))
		self.use_dims = (minx, miny, wid, hei)

	def yinvert(self, p_height: Union[float, int]):
		self._yinverting = True

class SuspPointTriang(Symbol):

	def __init__(self, p_radius) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)
		self.interval = 3
		self.use_dims = (0,0,0,0)

	def getUseDims(self):
		return self.use_dims

	def getComment(self):		
		return f"SuspPointTriang, radius:{self.radius}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return

		self.addChild(Desc().setText(self.getComment()))

		pt = polar2rectDegs(270, self.radius)
		pl = polar2rectDegs(150, self.radius)
		pr = polar2rectDegs(30, self.radius)

		h = pl.y - pt.y
		b = pr.x - pl.x
		mb = b / 2
		rat = mb / h 
		l0 = pt.y * rat 

		ap = self.addChild(AnalyticalPath())
		
		ap.addCmd(pM(*pl))
		ap.addCmd(pL(-pl.x, 0, relative=True))
		ap.addCmd(pL(0, 0))
		ap.addCmd(pL(l0, 0))
		ap.addCmd(pClose())

		ap.addCmd(pM(0,0))
		ap.addCmd(pL(-l0,0))
		ap.addCmd(pL(*pt))
		ap.addCmd(pClose())

		ap2 = self.addChild(AnalyticalPath().setStyle(Sty('fill', 'none')))
		
		ap2.addCmd(pM(0,pl.y))
		ap2.addCmd(pL(*pr))
		ap2.addCmd(pL(-l0,0)) 

		ap2.addCmd(pM(*pt))
		ap2.addCmd(pL(l0,0)) 
		ap2.refresh()

		offset = 1
		minx = pl.x-offset
		maxx = pr.x+offset
		wid = maxx - minx 
		miny = pt.y - offset
		maxy = pl.y + offset
		hei = maxy-miny

		self.setViewbox(VBox(minx, miny, wid, hei))
		self.use_dims = (minx, miny, wid, hei)

	def yinvert(self, p_height: Union[float, int]):
		self._yinverting = True

class Star(AnalyticalPath):

	def __init__(self, p_outradius, p_inoffset, p_nspikes, rot: Optional[Union[float, int]] = 0) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_outradius)
		self.offset = strictToNumber(p_inoffset)
		self.nspikes = strictToNumber(p_nspikes)
		self.rot = strictToNumber(rot)

	def getComment(self):		
		return f"Star, radius:{self.radius}, nspikes:{self.nspikes}, rot:{self.rot}"

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return False

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

		return True

class CircStar(Star):

	def __init__(self, p_outradius, p_inoffset, p_nspikes, rot: Optional[Union[float, int]] = 0, coffset: Optional[Union[float, int]] = None) -> None:
		
		super().__init__(p_outradius, p_inoffset, p_nspikes, rot=rot)
		self.coffset = coffset

	def getComment(self):		
		return f"{super().getComment()}, CircStar, coffset:{self.coffset}"

	def onAfterParentAdding(self, defselement=None):	
		if super().onAfterParentAdding():
			rad = self.coffset + self.radius
			self.addCmd(pM(-rad,0))
			self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
			self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))
			self.refresh()

def addRegPolyToPath(p_analytic_path, p_rot, p_radius, p_n, p_rhr):
	rot = p_rot - 90 # 0 is vertical
	ct = Pt(0,0)
	opts = list(circleDividers(ct, p_radius, p_n, rot))
	
	first = True

	if p_rhr:
		opts.reverse()

	for opt in opts:
		if first:
			p_analytic_path.addCmd(pM(*opt))
		else:
			p_analytic_path.addCmd(pL(*opt))
		first = False

	if not first:
		p_analytic_path.addCmd(pClose())

class RegPoly(AnalyticalPath):

	def __init__(self, p_radius, p_n, rot: Optional[Union[float, int]] = 0) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_radius)
		self.n = strictToNumber(p_n)
		self.rot = strictToNumber(rot)
		self._rhr = True
		assert self.n > 2

	def getComment(self):		
		return f"RegPoly, radius:{self.radius}, n:{self.n}, rot:{self.rot}"

	def changeFillRule(self, filled=True):
		self._rhr = filled

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return False

		addRegPolyToPath(self, self.rot, self.radius, self.n, self._rhr)

		return True

class CircRegPoly(RegPoly):

	def __init__(self, p_radius, p_n, rot: Optional[Union[float, int]] = 0, coffset: Optional[Union[float, int]] = None) -> None:
		
		super().__init__(p_radius, p_n, rot=rot)
		self.coffset = coffset

	def getComment(self):		
		return f"{super().getComment()}, CircPoly, coffset:{self.coffset}"

	def onAfterParentAdding(self, defselement=None):	
		self.changeFillRule(filled=False)
		if super().onAfterParentAdding():
			rad = self.coffset + self.radius
			self.addCmd(pM(-rad,0))
			self.addCmd(pA(rad, rad, 0, 1, 0, rad, 0))
			self.addCmd(pA(rad, rad, 0, 1, 0, -rad, 0))
			self.refresh()

class DonutPoly(RegPoly):

	def __init__(self, p_radius, p_n, out_n: Optional[int] = 0, rot: Optional[Union[float, int]] = 0, inrot: Optional[Union[float, int]] = 0, coffset: Optional[Union[float, int]] = None) -> None:
		
		super().__init__(p_radius, p_n, rot=inrot)
		self._outrot = rot
		self._coffset = coffset
		self._out_n = out_n

	def getComment(self):		
		return f"{super().getComment()}, DonutPoly, out-n:{self._out_n}, outrot:{self._outrot}, coffset:{self._coffset}"

	def onAfterParentAdding(self, defselement=None):	
		if super().onAfterParentAdding():
			rad = self._coffset + self.radius
			if self._out_n < 3:
				n = self.n
			else:
				n = self._out_n
			addRegPolyToPath(self, self._outrot, rad, n, False)

class Donut(AnalyticalPath):

	def __init__(self, p_outradius, p_inoffset) -> None:
		
		super().__init__()
		self.radius = strictToNumber(p_outradius)
		self.offset = strictToNumber(p_inoffset)

	def getComment(self):		
		return f"Donut, radius:{self.radius}, offset:{self.offset}"

	def onAfterParentAdding(self, defselement=None):	

		if not self._parentadded:
			self._parentadded = True
		else:
		 	return

		r2 = self.radius - self.offset

		self.addCmd(pM(self.radius,0))
		self.addCmd(pA(self.radius, self.radius, 0, 1, 1, -self.radius, 0))
		self.addCmd(pA(self.radius, self.radius, 0, 1, 1, self.radius, 0))
		self.addCmd(pM(r2,0))
		self.addCmd(pA(r2, r2, 0, 1, 0, -r2, 0))
		self.addCmd(pA(r2, r2, 0, 1, 0, r2, 0))
		self.refresh()

class Cylinder(Symbol):

	def __init__(self, p_width, p_height, pitch_ratio=0.5) -> None:

		super().__init__()
		self.height = strictToNumber(p_height)
		self.width = strictToNumber(p_width)
		self.pitch_ratio = strictToNumber(pitch_ratio)
		self.use_dims = (0,0,0,0)

	def setDims(self, p_width, p_height):
		self.height = strictToNumber(p_height)
		self.width = strictToNumber(p_width)

	def getUseDims(self):
		return self.use_dims

	def getComment(self):		
		return f"Cylinder, height:{self.height}, width:{self.width}, pitch_ratio:{self.pitch_ratio}"

	def refresh(self):

		if self.hasEl():
			self.clear()

		self.addChild(Desc().setText(self.getComment()))

		rad = self.width / 2.0
		hh = self.height / 2.0
		vrad = rad * self.pitch_ratio

		with self.addChild(AnalyticalPath()).setClass("symbfilllight") as pth:
			pth.addCmd(pM(-rad,-hh))
			pth.addCmd(pA(rad, vrad, 0, 1, 0, rad, -hh))
			pth.addCmd(pA(rad, vrad, 0, 1, 0, -rad, -hh))

		with self.addChild(AnalyticalPath()).setClass("symbfillmed") as ap2:
			ap2.addCmd(pM(-rad,-hh))
			ap2.addCmd(pL(-rad,hh))
			ap2.addCmd(pA(rad, vrad, 0, 1, 0, rad, hh))
			ap2.addCmd(pL(rad,-hh))
			ap2.addCmd(pA(rad, vrad, 0, 1, 1, -rad, -hh))

		minx = -rad-1
		wid = 2 * (rad+1)
		miny = -rad - vrad -1
		maxy = -miny
		hei = maxy-miny

		self.setViewbox(VBox(minx, miny, wid, hei))
		self.use_dims = (minx, miny, wid, hei)

	def onAfterParentAdding(self, defselement=None):	
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		self.refresh()

	def yinvert(self, p_height: Union[float, int]):
		self._yinverting = True

class Server(Symbol):

	def __init__(self, p_width, p_height, p_depth, rotation=30, projangle=120) -> None:

		super().__init__()
		self.height = strictToNumber(p_height)
		self.width = strictToNumber(p_width)
		self.depth = strictToNumber(p_depth)
		self.rotation = strictToNumber(rotation)
		self.projangle = strictToNumber(projangle)
		self.use_dims = (0,0,0,0)

	def setDims(self, p_width, p_height, depth=None):
		self.height = strictToNumber(p_height)
		self.width = strictToNumber(p_width)
		if not depth is None:
			self.depth = strictToNumber(depth)

	def getUseDims(self):
		return self.use_dims

	def getComment(self):		
		return f"Server, height:{self.height}, width:{self.width}, depth:{self.depth}, rotation:{self.rotation}"

	def refresh(self):	

		self.addChild(Desc().setText(self.getComment()))

		beta = self.rotation + self.projangle
		lright = glRd(cos(radians(self.rotation)) * self.depth)
		lleft = abs(glRd(cos(radians(beta)) * self.width))
		planar_width = lright + lleft
		hw = planar_width / 2

		low_hh = self.height / 3

		pzero_x = hw - lright
		right_deltay = glRd(sin(radians(self.rotation)) * self.depth)
		left_deltay = glRd(sin(radians(beta)) * self.width)
		pzero_y = low_hh + right_deltay

		pth = self.addChild(AnalyticalPath()).setClass("symbfillmed")
		pth.addCmd(pM(pzero_x, pzero_y))
		pth.addCmd(pL(lright, -right_deltay, relative=True))
		pth.addCmd(pL(0, -self.height, relative=True))
		pth.addCmd(pL(-lright, right_deltay, relative=True))
		pth.addCmd(pClose())

		ap2 = self.addChild(AnalyticalPath()).setClass("symbfilldark")
		ap2.addCmd(pM(pzero_x, pzero_y))
		ap2.addCmd(pL(0,-self.height, relative=True))
		ap2.addCmd(pL(-lleft, -left_deltay, relative=True))
		ap2.addCmd(pL(0, self.height, relative=True))
		ap2.addCmd(pClose())

		ap3 = self.addChild(AnalyticalPath()).setClass("symbfilllight")
		ap3.addCmd(pM(pzero_x, pzero_y))
		ap3.addCmd(pM(0, -self.height, relative=True))
		ap3.addCmd(pL(lright, -right_deltay, relative=True))
		ap3.addCmd(pL(-lleft, -left_deltay, relative=True))
		ap3.addCmd(pL(-lright, right_deltay, relative=True))
		ap3.addCmd(pClose())

		left_diagonal = sqrt(pow(lleft,2) + pow(left_deltay,2))

		with self.addChild(AnalyticalPath()).setClass("symbinnerstroke") as ap4:

			for i in range(4):
				pt1 = Pt(pzero_x, pzero_y-(right_deltay/2)-(i*8))
				ap4.addCmd(pM(*pt1))
				ptx = polar2rectDegs(-beta, 0.7 * left_diagonal)
				pt2 = ptAdd(pt1, ptx)
				ap4.addCmd(pL(*pt2))

	
		offset = 2
		minx = pzero_x-lleft-offset
		maxx = pzero_x+lright+offset
		wid = maxx - minx
		maxy = pzero_y + offset
		miny = pzero_y - self.height - right_deltay - left_deltay - offset

		hei = maxy-miny

		self.setViewbox(VBox(minx, miny, wid, hei))
		self.use_dims = (minx, miny, wid, hei)

	def onAfterParentAdding(self, defselement=None):	

		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		self.refresh()

	def yinvert(self, p_height: Union[float, int]):
		self._yinverting = True
