

from rpcbSVG.Basics import Trans, fontSizeToVPUnits, toNumberAndUnit
from rpcbSVG.Structs import Ci, Re
from rpcbSVG.SVGLib import BaseSVGElem, Circle, Group, Rect, RectRC, TextParagraph
from rpcbSVG.Symbols import Diamond

from typing import Optional

VERTICAL_ADJUST = 0.2

class TextBox(Group):

	def __init__(self, *args, text: Optional[str] = None, paddingh=10, paddingv=10, vsep="1.2em", anchor="lt", hjustify="left", vcenter_fontszpx=None) -> None:
		"consumes rect args"
		super().__init__()
		self._forceNonYInvertChildren = True
		self._re = Re(*args)
		self.text = text
		self._padding = (paddingh, paddingv)
		self._vsep = vsep
		self._anchor = anchor.lower()
		self._hjustify = hjustify.lower()
		self._txpara = None
		self._shape = None
		self._vcenter_fontszpx = vcenter_fontszpx

	def setBaseShape(self, p_shp: BaseSVGElem):
		"""Setting a template shape which is goint to be adjusted 'onAfterParentAdding'.
			Must precede onAfterParentAdding, the 'addChild' method execution to bind this to parent XML SVG element.
			If this method is not called, self._shape defaults to a Rect
		"""
		assert not self._parentadded, "setBaseShape can't be used after onAfterParentAdding"
		self._shape = p_shp

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

	def _adjustTextVertical(self, l=None):
		if not l is None:
			_l = l
		else:
			_l = len(self._getTextLines())

		if _l > 0 and not self._vcenter_fontszpx is None and not self._txpara is None:			
			yinverting = not self._yinvertdelta is None
			boxheight = self._re.getNumeric("height")
			hbh = boxheight / 2
			lineheight = fontSizeToVPUnits(fontsize=self._vcenter_fontszpx, possibleEmModifier=self._vsep)
			fontheight = fontSizeToVPUnits(fontsize=self._vcenter_fontszpx)
			head = lineheight - fontheight
			hfh = fontheight / 2
			offsetodd = hfh + head

			# print("lineheight, fontheight, boxheight:", lineheight, fontheight, boxheight)
			# print("offsetodd, _l:", offsetodd, _l)

			if _l % 2 == 1:
				vshift = offsetodd + (_l-1) * 0.5  * lineheight
			else:
				vshift = (_l * 0.5) + (head / 2)

			# print("vshift:", vshift, "hbh:", hbh)

			ty = hbh - vshift - (VERTICAL_ADJUST * fontheight)
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

	def onAfterParentAdding(self):	

		if not self._parentadded:
			self._parentadded = True
		else:
		 	return

		textrows = self._getTextLines()

		mwdelta = lambda z,w: z - w / 2 
		mwdelta_plus = lambda z,w: z + w / 2 

		yinverting = not self._yinvertdelta is None
			
		x, y, width, height = list(self._re.iterUnitsRemovedNum())
		ax = x
		ay = y
		diamond_pt = (width/2, height/2)

		tx, ty = self._padding

		if self._hjustify == "center":
			tx = width / 2
		elif self._hjustify == "right":
			tx = width - self._padding[0]

		self._adjustTextVertical(l=len(textrows))

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

		self.addChild(self._shape)

		self._txpara = self.addChild(TextParagraph(tx, ty, textrows, vsep=self._vsep, justify=self._hjustify))


