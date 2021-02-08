
from rpcbSVG.Basics import pClose, pL, pM, toNumberAndUnit
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
