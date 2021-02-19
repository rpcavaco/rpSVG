

from rpcbSVG.Basics import Pt, Trans, fontSizeToVPUnits, glRd, strictToNumber, toNumberAndUnit
from rpcbSVG.Structs import Ci, Re
from rpcbSVG.SVGLib import BaseSVGElem, Circle, Group, Rect, RectRC, TextParagraph, Use
from rpcbSVG.Symbols import Cylinder, Diamond, Server

from typing import Optional, Union

VERTICAL_ADJUST = 0.3

class TextBox(Group):

	def __init__(self, *args, text: Optional[str] = None, paddingh=10, paddingv=10, vsep="1.2em", anchor="lt", hjustify="left", vcenter_fontszpx=None) -> None:
		"consumes rect args"
		super().__init__()
		self._FATTR_forceNonYInvertChildren = True
		self._re = Re(*args)
		self.text = text
		self._padding = (paddingh, paddingv)
		self._vsep = vsep
		self._anchor = anchor.lower()
		self._hjustify = hjustify.lower()
		self._txpara = None
		self._shape = None
		self._vcenter_fontszpx = vcenter_fontszpx
		self._defselement = None

	def setBaseShape(self, p_shp: BaseSVGElem):
		"""Setting a template shape which is goint to be adjusted 'onAfterParentAdding'.
			Must precede onAfterParentAdding, the 'addChild' method execution to bind this to parent XML SVG element.
			If this method is not called, self._shape defaults to a Rect
		"""
		assert not self._parentadded, "setBaseShape can't be used after onAfterParentAdding"
		self._shape = p_shp
		return self._shape

	def getShape(self):
		return self._shape

	def getComment(self):	
		if self._re is None:	
			return "TextBox"
		else:	
			return f"TextBox {self._re}"

	def _getTextLines(self):
		if not self.text is None and len(self.text) > 0:
			textrows = self.text.split('\n')
		else:
			textrows = []
		return textrows

	def getParagraph(self):
		return self._txpara

	def getAnchor(self) -> Union[None, Pt]:
		x, _u = toNumberAndUnit(self._re.get("x"))
		y, _u = toNumberAndUnit(self._re.get("y"))
		return Pt(x, y)

	def getCorners(self, forceanchor=None):
		"ccw from lower right"
		x, _u = toNumberAndUnit(self._re.get("x"))
		y, _u = toNumberAndUnit(self._re.get("y"))
		w, _u = toNumberAndUnit(self._re.get("width"))
		h, _u = toNumberAndUnit(self._re.get("height"))
		hw = w/2
		hh = h/2

		if not forceanchor is None:
			anch = forceanchor
		else:
			anch = self._anchor

		if anch.startswith('l'):
			if anch.endswith('c'):
				ret = [
					Pt(x+w, y+hh), Pt(x+w, y-hh), Pt(x, y-hh), Pt(x, y+hh)
				]
			elif anch.endswith('b'):
				ret = [
					Pt(x+w, y), Pt(x+w, y-h), Pt(x, y-h), Pt(x, y)
				]
			elif anch.endswith('t'):
				ret = [
					Pt(x+w, y+h), Pt(x+w, y), Pt(x, y), Pt(x, y+h)
				]
		elif anch.startswith('c'):
			if anch.endswith('t'):
				ret = [
					Pt(x+hw, y+h), Pt(x+hw, y), Pt(x-hw, y), Pt(x-hw, y+h)
				]
			elif anch.endswith('c'):
				ret = [
					Pt(x+hw, y+hh), Pt(x+hw, y-hh), Pt(x-hw, y-hh), Pt(x-hw, y+hh)
				]
			elif anch.endswith('b'):
				ret = [
					Pt(x+hw, y), Pt(x+hw, y-h), Pt(x-hw, y-h), Pt(x-hw, y)
				]
		elif anch.startswith('r'):
			if anch.endswith('t'):
				ret = [
					Pt(x, y+h), Pt(x, y), Pt(x-w, y), Pt(x-w, y+h)
				]
			elif anch.endswith('c'):
				ret = [
					Pt(x, y+hw), Pt(x, y-hw), Pt(x-w, y-hw), Pt(x-w, y+hw)
				]
			elif anch.endswith('b'):
				ret = [
					Pt(x, y), Pt(x, y-h), Pt(x-w, y-h), Pt(x-w, y)
				]

		return ret


	def _adjustTextVertical(self, l=None):
		if not l is None:
			_l = l
		else:
			_l = len(self._getTextLines())

		if _l > 0 and not self._vcenter_fontszpx is None and not self._txpara is None:			
			boxheight = self._re.getNumeric("height")
			hbh = boxheight / 2
			lineheight = fontSizeToVPUnits(fontsize=self._vcenter_fontszpx, possibleEmModifier=self._vsep)
			fontheight = fontSizeToVPUnits(fontsize=self._vcenter_fontszpx)
			head = lineheight - fontheight
			hfh = fontheight / 2
			offsetodd = hfh + head

			if _l % 2 == 1:
				vshift = offsetodd + (_l-1) * 0.5  * lineheight
			else:
				vshift = (_l * 0.5 * lineheight) + (head / 2)
			ty = glRd(hbh - vshift - (VERTICAL_ADJUST * fontheight))
			transf = self._txpara.getTransformN(0)
			transf.set("ty", ty)
			self._txpara.updateTransformAttr()

			# print("Param V", ty, _l , lineheight * 0.5 , height/2, self._shape)

	def setText(self, p_text: str):
		self.text = p_text
		if not self._txpara is None:
			self._txpara.setText(self._getTextLines())
			self._adjustTextVertical()
		return self

	def refresh(self):

		assert not self._defselement is None

		textrows = self._getTextLines()

		mwdelta = lambda z,w: z - w / 2 
		mwdelta_plus = lambda z,w: z + w / 2 

		yinverting = not self._yinvertdelta is None

		x, y, width, height = list(self._re.iterUnitsRemovedNum())
		ax = glRd(x)
		ay = glRd(y)
		diamond_pt = (glRd(width/2), glRd(height/2))

		tx = glRd(self._padding[0])
		ty = glRd(self._padding[1])

		if self._hjustify == "center":
			tx = glRd(width / 2)
		elif self._hjustify == "right":
			tx = glRd(width - self._padding[0])

		if self._anchor.startswith('l'):
			if self._anchor.endswith('c'):
				ax = x
				if yinverting:
					ay = mwdelta_plus(y, height)
				else:
					ay = mwdelta(y, height)
			elif self._anchor.endswith('b'):
				ax = x
				if yinverting:
					ay = y + height
				else:
					ay = y - height
		elif self._anchor.startswith('c'):
			if self._anchor.endswith('t'):
				ax = mwdelta(x, width)
				ay = y
			elif self._anchor.endswith('c'):
				ax = mwdelta(x, width)
				if yinverting:
					ay = mwdelta_plus(y, height)
				else:
					ay = mwdelta(y, height)
			elif self._anchor.endswith('b'):
				ax = mwdelta(x, width)
				if yinverting:
					ay = y + height
				else:
					ay = y - height
		elif self._anchor.startswith('r'):
			if self._anchor.endswith('t'):
				ax = x - width
				ay = y
			elif self._anchor.endswith('c'):
				ax = x - width
				if yinverting:
					ay = mwdelta_plus(y, height)
				else:
					ay = mwdelta(y, height)
			elif self._anchor.endswith('b'):
				ax = x - width
				if yinverting:
					ay = y + height
				else:
					ay = y - height

		ax = glRd(ax)
		ay = glRd(ay)

		self.clearTransforms()
		self.addTransform(Trans(ax, ay))

		if self._shape is None:
			self._shape = Rect(0,0, width, height)
		elif isinstance(self._shape, Rect) or isinstance(self._shape, RectRC):
			self._shape.setStructAttr("width", width)
			self._shape.setStructAttr("height", height)
		elif isinstance(self._shape, Diamond):
			self._shape.setDims(Re(width, height, *diamond_pt))
		elif isinstance(self._shape, Circle):
			radius = max(width, height) / 2.0
			self._shape.setStruct(Ci(*diamond_pt, radius))
		elif isinstance(self._shape, Cylinder):
			self._shape.setDims(width, height)
		elif isinstance(self._shape, Server):
			w0 = strictToNumber(width)
			w = 0.3 * w0
			d = 0.6 * w0
			h = 1.0 * strictToNumber(height)
			self._shape.setDims(w, h, depth=d)

		# Symbols (added to DESC)
		if isinstance(self._shape, Cylinder):
			if not self._shape.hasEl():
				assert not self._defselement is None
				self._defselement.addChild(self._shape)
			utup = self._shape.getUseTuple(*diamond_pt)
			self.addChild(Use(*utup, self._shape.getSel()))
		elif isinstance(self._shape, Server):
			if not self._shape.hasEl():
				assert not self._defselement is None
				self._defselement.addChild(self._shape)
			utup = self._shape.getUseTuple(*diamond_pt)
			self.addChild(Use(*utup, self._shape.getSel()))
		else:
			if not self._shape.hasEl():
				self.addChild(self._shape)

		self._adjustTextVertical(l=len(textrows))

		if self._txpara is None:
			self._txpara = self.addChild(TextParagraph(tx, ty, textrows, vsep=self._vsep, justify=self._hjustify), noyinvert=True)

	def onAfterParentAdding(self, defselement=None):	
		self._defselement = defselement
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		self.refresh()

	def yinvert(self, p_height: Union[float, int]):
		if not self._noyinvert: 
			self._yinvertdelta = p_height
			self.refresh()

