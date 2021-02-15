
#import cairo
#import rsvg


from io import StringIO
from typing import Optional, List, Union
from warnings import warn

from lxml import etree

from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.Basics import MINDELTA, Pt, Trans, XLINK_NAMESPACE, _withunits_struct, \
	pClose, pH, pL, pM, pV, strictToNumber, transform_def, path_command, \
	ptCoincidence, removeDecsep, ptEnsureStrings
from rpcbSVG.Structs import Ci, Elli, GraSt, Img, Li, LiGra, Mrk, MrkProps, Patt, Pl, Pth, RaGra, Re, ReRC, Symb, Tx, TxPth, TxRf, Us, VBox

SVG_NAMESPACE = "http://www.w3.org/2000/svg"

DOCTYPE_STR = """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""


SVG_ROOT = """<svg 
	 xmlns="{0}" 
	 xmlns:xlink="{1}" />
	 """.format(SVG_NAMESPACE, XLINK_NAMESPACE)

DECLARATION_ROOT = """<?xml version="1.0" standalone="no"?>
{0}""".format(SVG_ROOT)

class TagOutOfDirectUserManipulation(RuntimeError):
	def __init__(self, p_tag):
		self.tag = p_tag
	def __str__(self):
		return f"Tag '{self.tag}' not to be manipulated by user."

# def renderToFile(svgstr, w, h, filename):
# 	img = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
# 	ctx = cairo.Context(img)
# 	svg = rsvg.Handle(data=svgstr)
# 	svg.render_cairo(ctx)
# 	img.write_to_png(filename)
						
class BaseSVGElem(object):

	NO_XML_EL = "XML Element not created yet. Must add this to SVGContainer to auto create it."

	def __init__(self, tag: str, 
			struct: Optional[_withunits_struct] = None):
		self.tag = tag
		self._struct = None
		self._style = None
		self._transforms = []
		self.idprefix = tag[:3].title()
		self.el = None
		self._pendingXMLDependentOps = []
		self._yinvertdelta = None
		self._parentadded = False
		self.setStruct(struct)

	def clone(self):
		return BaseSVGElem(self.tag, struct=self.getStruct())

	def _getTransform(self) -> str:
		return " ".join([t.get() for t in self._transforms])

	def hasEl(self):
		return  not self.el is None

	def getEl(self):
		assert self.hasEl(), self.NO_XML_EL
		return self.el

	def setEl(self, xmlel) -> None:
		assert not self.hasEl()
		self.el = xmlel
		strct = self._struct
		if not strct is None:
			strct.setXmlAttrs(self.getEl())
		# Things waiting to XML el to be de
		if len(self._pendingXMLDependentOps) > 0:
			op = self._pendingXMLDependentOps.pop(0)
			while op:
				meth, args, kwargs = op
				if args is None:
					if kwargs is None:
						meth()
					else:
						meth(**kwargs)
				else:
					if kwargs is None:
						meth(*args)
					else:
						meth(*args, **kwargs)
				try:
					op = self._pendingXMLDependentOps.pop(0)
				except IndexError:
					op = None
		return self

	def removeEl(self):
		assert self.hasEl(), self.NO_XML_EL
		par = self.getEl().getparent()
		par.remove(self.getEl())
		return par

	def _setText(self, p_text: str) -> None:
		assert isinstance(p_text, str)
		assert self.hasEl(), self.NO_XML_EL
		self.getEl().text = p_text

	def setText(self, p_text: str):
		self.dispatchXMLDependentOp(self._setText, args=(p_text,))
		return self

	def getText(self):
		if self.hasEl():
			ret = self.getEl().text
		else:
			ret = ""
		return ret

	def clearText(self):
		if self.hasEl():
			self.getEl().text = ""

	def clearChildren(self):
		for child in list(self.getEl()):
			self.getEl().remove(child)		

	def _tailText(self, p_text: str) -> None:
		assert isinstance(p_text, str)
		assert self.hasEl(), self.NO_XML_EL
		self.getEl().tail = p_text

	def tailText(self, p_text: str):
		self.dispatchXMLDependentOp(self._tailText, args=(p_text,))
		return self

	def _setDirectAttr(self, p_attr: str, p_value):
		assert self.hasEl(), self.NO_XML_EL
		self.getEl().set(p_attr, p_value)
		return self

	def dispatchXMLDependentOp(self, method, args=None, kwargs=None):
		if self.hasEl():
			if args is None:
				if kwargs is None:
					method()
				else:
					method(**kwargs)
			else:
				if kwargs is None:
					method(*args)
				else:
					method(*args, **kwargs)
		else:
			self._pendingXMLDependentOps.append((method, args, kwargs))

	def __repr__(self):
		out = [
			f"tag={str(self.tag)}"
		]
		if self.hasEl():
			for x in self.getEl().keys():
				out.append(f"{x}={self.getEl().get(x)}")
		return ' '.join(out)

	def toJSON(self):
		out = {
			"tag": str(self.tag),
			"attribs": {}
		}
		if self.hasEl():
			for x in self.getEl().keys():
				out["attribs"][x] = self.getEl().get(x)
		return out

	def similitudeTo(self, o: object) -> str:
		ret = []
		if self.getTag() == o.getTag():
			ret.append('TAG')
			a = self.getStruct()
			b = o.getStruct()
			if self.getStruct() == o.getStruct():
				ret.append('STRUCT')
			sty = self.getStyle()
			if not sty is None:
				osty = o.getStyle()
				if not osty is None:
					if sty == osty:
						ret.append('STYLE')
			trtxt = self._getTransform() 
			if len(trtxt) > 0 and trtxt == o._getTransform():
				ret.append('TRANS')
		return ret

	def _updateStructAttrs(self):
		assert self.hasEl()
		if not self._struct is None:
			self._struct.setXmlAttrs(self.getEl())
		return self

	def updateStructAttrs(self):
		if not self._struct is None:
			self.dispatchXMLDependentOp(self._updateStructAttrs)
		return self

	def setStruct(self, struct: _withunits_struct):
		self._struct = struct
		return self.updateStructAttrs()

	def getStruct(self) -> _withunits_struct:
		assert not self._struct is None
		if self.hasEl():
			self._struct.getFromXmlAttrs(self.getEl())
		return self._struct

	def hasStruct(self) -> bool:
		return not self._struct is None

	def setStructAttr(self, p_attr: str, p_value):
		stru = self.getStruct()
		stru.set(p_attr, p_value)
		self.updateStructAttrs()
		return self

	def setHREFAttr(self, p_value):
		stru = self.getStruct()
		stru.setHREF(p_value)
		self.updateStructAttrs()
		return self

	def getSelector(self, select='id', funciri=False):
		assert select in (None, "id", "class", "tag")
		sel = None
		if select == 'id':
			assert self.hasId()
			sel = '#' + self.getId()
		elif select == 'class':
			assert self.hasClass()
			sel = '.' + self.getClass()
		elif select == 'tag':
			sel = self.tag
		if funciri:
			ret = f"url({sel})"
		else:
			ret = sel
		return ret

	def _updateStyleAttrs(self):
		if not self._style is None and self.hasEl():
			self._style.setXmlAttrs(self.getEl())
		return self

	def updateStyleAttrs(self):
		if not self._style is None:
			self.dispatchXMLDependentOp(self._updateStyleAttrs)
		return self

	def setStyle(self, style: Sty):
		assert isinstance(style, Sty)
		self._style = style
		return self.updateStyleAttrs()

	def hasStyle(self):
		return not self._style is None

	def getStyle(self, select=None) -> Union[Sty, CSSSty]:
		""" select: None, "id", "class", "tag" """
		ret = None
		if not self._style is None and self.hasEl():
			self._style.fromXmlAttrs(self.getEl())
			sel = self.getSelector(select=select)
			if not sel is None:
				ret = CSSSty(selector=sel)
				ret.copyFromSty(self._style)
			else:
				ret = self._style
		return ret

	def _updateTransformAttr(self):
		if len(self._transforms) > 0 and self.hasEl():
			self.getEl().set('transform', self._getTransform()) 
		return self

	def updateTransformAttr(self):
		if len(self._transforms) > 0:
			self.dispatchXMLDependentOp(self._updateTransformAttr)
		return self

	def getTransformN(self, p_n: int):
		assert p_n < len(self._transforms)
		return self._transforms[p_n]

	def getTransformsList(self):
		return self._transforms

	def __enter__(self):
	 	return (self.getStruct(), self.getStyle(), self.getTransformsList())

	def __exit__(self, exc_type, exc_value, traceback):
		self.updateStructAttrs()
		self.updateStyleAttrs()
		self.updateTransformAttr()

	def getSel(self, select='id'):
		return self.getSelector(select=select)

	def getParent(self):
		assert self.hasEl(), self.NO_XML_EL
		return self.getEl().getparent()

	def readdElToParent(self, p_parent):
		assert self.hasEl(), self.NO_XML_EL
		p_parent.append(self.getEl())

	def delEl(self):
		self.getEl().getparent().remove(self.getEl())
		self.el = None

	def _setId(self, idval):
		assert isinstance(idval, str)
		assert self.hasEl(), self.NO_XML_EL
		self.getEl().set('id', idval)

	def setId(self, idval):
		assert isinstance(idval, str)
		self.dispatchXMLDependentOp(self._setId, args=(idval,))
		return self

	def getId(self):
		assert self.hasEl(), self.NO_XML_EL
		assert "id" in self.getEl().keys()
		return self.getEl().get('id')

	def hasId(self) -> bool:
		assert self.hasEl(), self.NO_XML_EL
		return "id" in self.getEl().keys()

	def _setClass(self, clsval):
		assert isinstance(clsval, str)
		assert self.hasEl(), self.NO_XML_EL
		self.getEl().set('class', clsval)

	def setClass(self, clsval):
		self.dispatchXMLDependentOp(self._setClass, args=(clsval,))
		return self

	def getClass(self):
		assert self.hasEl(), self.NO_XML_EL
		assert "class" in self.getEl().keys()
		return self.getEl().get('class')

	def hasClass(self) -> bool:
		assert self.hasEl(), self.NO_XML_EL
		return "class" in self.getEl().keys()

	def getTag(self):
		return self.tag

	def clearTransforms(self):
		del self._transforms[:]

	def addTransform(self, tr: transform_def):
		if not self._yinvertdelta is None and hasattr(tr, "yinvert"):
			tr.yinvert(self._yinvertdelta)
		self._transforms.append(tr)
		trtxt = self._getTransform() 
		if len(trtxt) > 0:
			self.getEl().set('transform', trtxt)
		return tr

	def yinvert(self, p_height: Union[float, int]):
		self._yinvertdelta = p_height
		if self.hasStruct():
			strct = self.getStruct()
			if hasattr(strct, 'yinvert'):
				strct.yinvert(p_height)
				ret = self.updateStructAttrs()
			else:
				ret = self
		else:
			ret = self
		return ret

	def onAfterParentAdding(self):
		"""To be extended, actions to run after being added to parent. 
		   Extending classes must check self._parentadded state and return immediately if this is True"""
		# if not self._parentadded:
		# 	self._parentadded = True
		# else:
		# 	return


class GenericSVGElem(BaseSVGElem):

	def __init__(self, tag: str, struct: Optional[_withunits_struct] = None) -> None:
		self.content = []
		self._noyinvert = False
		super().__init__(tag, struct=struct)

	def addChild(self, p_child: BaseSVGElem, parent: Optional[Union[etree.Element, BaseSVGElem]]=None, nsmap=None, noyinvert=False):
		
		self._noyinvert = noyinvert

		# Comments
		if hasattr(p_child, 'getComment'):
			self.getEl().append(etree.Comment(p_child.getComment()))

		if parent is None:
			assert self.hasEl(), "XML parent not inited. If this is happening in a new object class init, maybe you should instead place this child adding in 'onAfterParentAdding' method"
			if nsmap is None:
				newel = etree.SubElement(self.getEl(), p_child.tag)
			else:
				newel = etree.SubElement(self.getEl(), p_child.tag, nsmap=nsmap)
		else:
			if isinstance(parent, type(etree.Element)):
				newel = etree.SubElement(parent, p_child.tag)
			else:
				assert isinstance(parent, BaseSVGElem), str(type(parent))
				assert self.hasEl()
				newel = etree.SubElement(parent.getEl(), p_child.tag)

		if not self._noyinvert:
			if not self._yinvertdelta is None and hasattr(p_child, 'yinvert'):
				p_child.yinvert(self._yinvertdelta)

		p_child.setEl(newel)
		self.content.append(p_child)

		if not hasattr(self, "_autoGenerateSubIds") or getattr(self, "_autoGenerateSubIds"):
			if not hasattr(p_child, '_autoGenerateId') or getattr(p_child, '_autoGenerateId'):		
				if not p_child.hasId() and hasattr(self, 'genNextId'):
					idval = self.genNextId()
					if not idval is None:
						p_child.setId(p_child.idprefix + str(idval))

		return p_child

	def addChildTag(self, p_tag: str):
		assert self.hasEl()
		newel = etree.SubElement(self.getEl(), p_tag)
		return newel

	def clear(self):
		assert self.hasEl()
		del self.getEl()[:]

	def toJSON(self):
		out = super().toJSON()
		if len(self.content) > 0:
			out["content"] = []
			for chld in self.content:
				out["content"].append(chld.toJSON())
		return out

	def yinvert(self, p_height: Union[float, int]):
		if not self._noyinvert:
			return super().yinvert(p_height)

class SVGContainer(GenericSVGElem):

	def __init__(self, tag: str, struct: Optional[_withunits_struct] = None, viewbox: Optional[VBox] = None) -> None:
		super().__init__(tag, struct=struct)
		self._defs = None
		self.genIDMethod = None
		if not viewbox is None:
			self.setViewbox(viewbox)

	def setGenIdMethod(self, p_method):
		self.genIDMethod = p_method

	def addChild(self, p_child: BaseSVGElem, todefs: Optional[bool] = False, nsmap=None, noyinvert=False) -> BaseSVGElem:
		if hasattr(self, '_forceNonYInvertChildren') and getattr(self, '_forceNonYInvertChildren'):
			_noyinvert = True
		else:
			_noyinvert = noyinvert
		if todefs:
			if self._defs is None:
				self._defs = super().addChild(Defs())
			ret = super().addChild(p_child, parent=self._defs, nsmap=nsmap, noyinvert=_noyinvert)
		else:
			ret = super().addChild(p_child, nsmap=nsmap, noyinvert=_noyinvert)
		if not self.genIDMethod is None and hasattr(ret, 'setGenIdMethod'):
			ret.setGenIdMethod(self.genIDMethod)

		ret.onAfterParentAdding()

		return ret

	def genNextId(self):
		ret = None
		if not self.genIDMethod is None:
			ret = self.genIDMethod()
		return ret

	def _setViewbox(self, p_viewbox: VBox):
		assert isinstance(p_viewbox, VBox)
		p_viewbox.setXmlAttrs(self.getEl())
		return self

	def setViewbox(self, p_viewbox: VBox):
		self.dispatchXMLDependentOp(self._setViewbox, args=(p_viewbox,))
		return self

	def setIdentityViewbox(self, scale: Optional[float] = None):
		strct = self.getStruct()
		assert not strct is None
		vb = VBox()
		vb.cloneFromRect(self.getStruct(), scale=scale)
		return self.setViewbox(vb)

	def getViewbox(self):
		vb = VBox()
		vb.getFromXmlAttrs(self.getEl())
		return vb

class SVGRoot(SVGContainer):

	def __init__(self, rect: Re, tree = None, viewbox: Optional[VBox] = None) -> None:
		super().__init__("svg", struct=rect, viewbox=viewbox)
		if tree is None:
			self.tree = etree.parse(StringIO(SVG_ROOT))
		elif hasattr(tree, 'getroot'):
			self.tree = tree
		else:
			raise RuntimeError("object supplied is not ElementTree")
		assert not self.tree is None
		self.setEl(self.tree.getroot())
		self.setRect(rect)
		# Viewbox must be (re)inited here: in SVGContainer __init__ , 
		# 	setViewbox finds no XML Element, is not yet created)
		if not viewbox is None:
			self.setViewbox(viewbox)

	def setRect(self, p_rect: Re):
		assert isinstance(p_rect, Re)
		self.setStruct(p_rect)
		p_rect.setXmlAttrs(self.getEl())
		return self

	def _addComment(self, p_text: str) -> None:
		assert isinstance(p_text, str)
		assert self.hasEl(), self.NO_XML_EL
		self.getEl().append(etree.Comment(p_text))

	def addComment(self, p_text: str):
		self.dispatchXMLDependentOp(self._addComment, args=(p_text,))
		return self

class SVGContent(SVGRoot):

	forbidden_user_tags = ["defs", "style"]
	def __init__(self, rect: Re, viewbox: Optional[VBox] = None, yinvert=False) -> None:
		super().__init__(rect, viewbox=viewbox)
		self._id_serial = 0
		self._defs = super().addChild(Defs())
		self._styleel = self._defs.addChild(Style())
		self._yinvert = yinvert

	def _calcYInvertDelta(self):
		vb = self.getViewbox()
		vbvals = vb.getValues()
		miny = None
		height = None
		if len(vbvals) > 2:
			miny = vbvals[1]
			height = vbvals[3]
		else:
			strct = self.getStruct()
			if hasattr(strct, 'height'):
				height = strictToNumber(getattr(strct, 'height'))
			if hasattr(strct, 'y'):
				miny = strictToNumber(getattr(strct, 'y'))
		assert not miny is None and not height is None
		return 2 * miny + height

	def getYInvertFlag(self):
		return self._yinvert

	def getYInvertDelta(self):
		return self._calcYInvertDelta()

	def nextIDSerial(self):
		ret = self._id_serial
		self._id_serial = self._id_serial + 1
		return ret

		# self._autoGenerateSubIds = False

	def addChild(self, p_child: BaseSVGElem, todefs: Optional[bool] = False, nsmap=None, noyinvert=False) -> BaseSVGElem:
		if p_child.tag in self.forbidden_user_tags:
			raise TagOutOfDirectUserManipulation(p_child.tag)
		if not noyinvert:
			if self._yinvert and hasattr(p_child, 'yinvert'):
				delta = self._calcYInvertDelta()
				p_child.yinvert(delta)
		if todefs or (hasattr(p_child, "_forceToDefs") and getattr(p_child, "_forceToDefs")):
			assert not self._defs is None
			ret = self._defs.addChild(p_child, nsmap=nsmap, noyinvert=noyinvert)
		else:
			ret = super().addChild(p_child, nsmap=nsmap, noyinvert=noyinvert)
		if not ret.hasId():
			ret.setId(p_child.idprefix + str(self.nextIDSerial()))
		if isinstance(ret, SVGContainer):
			ret.setGenIdMethod(self.nextIDSerial)

		ret.onAfterParentAdding()

		return ret

	def addStyleRule(self, p_child: CSSSty) -> str:
		return self._styleel.addRule(p_child)

	def delStyleRule(self, selector: str) -> bool:
		return self._styleel.delRule(selector)

	def setBackground(self, sty: Sty):
		vb = self.getViewbox()
		if vb.isEmpty():
			strct = self.getStruct()
			assert not strct.isEmpty()
			vals = strct.getValues()
		else:
			vals = vb.getValues()
		self.addChild(Rect(*vals)).setStyle(sty)

	def render(self):
		return self._styleel.render(depth=-1)

	def toBytes(self, inc_declaration=False, inc_doctype=False, pretty_print=True):
		parelem = None
		if not self.render():
			parelem = self._styleel.removeEl()

		if inc_doctype:
			ret = etree.tostring(self.getEl(), doctype=DOCTYPE_STR, xml_declaration=inc_declaration, pretty_print=pretty_print, encoding='utf-8')
		else:
			ret = etree.tostring(self.getEl(), xml_declaration=inc_declaration, pretty_print=pretty_print, encoding='utf-8')	

		if not parelem is None:
			self._styleel.readdElToParent(parelem)

		return ret

	def toString(self, inc_declaration=False, inc_doctype=False, pretty_print=True):
		return self.toBytes(inc_declaration=inc_declaration, inc_doctype=inc_doctype, pretty_print=pretty_print).decode('utf-8')

class Group(SVGContainer):
	def __init__(self) -> None:
		super().__init__('g')

class Defs(SVGContainer):
	def __init__(self) -> None:
		super().__init__('defs')

class Marker(SVGContainer):
	def __init__(self, *args) -> None:
		super().__init__("marker", struct=Mrk(*args))

class Symbol(SVGContainer):
	def __init__(self, *args) -> None:
		self._forceToDefs = True
		self._autoGenerateSubIds = False
		super().__init__("symbol", struct=Symb(*args))

class Use(BaseSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("use", struct=Us(*args))

class Desc(SVGContainer):
	def __init__(self) -> None:
		self._autoGenerateId = False
		super().__init__("desc")

class Title(BaseSVGElem):
	def __init__(self, p_titletext: str) -> None:
		self._autoGenerateId = False
		super().__init__("title")
		self.dispatchXMLDependentOp(self.setText, args=(p_titletext,))

class Style(BaseSVGElem):

	def __init__(self) -> None:
		super().__init__('style')
		self.stylerules = {}

	def addRule(self, p_child: CSSSty) -> str:
		assert isinstance(p_child, CSSSty)
		ret = p_child.getSelector()
		self.stylerules[ret] =p_child
		return ret

	def delRule(self, selector: str) -> bool:
		ret = False
		if selector in self.stylerules.keys():
			del self.stylerules[selector]
			ret = True
		return ret

	def getRule(self, selector: str) -> Union[None, CSSSty]:
		ret = None
		if selector in self.stylerules.keys():
			ret = self.stylerules[selector]
		return ret

	def render(self, depth=-1) -> bool:
		ret = False
		if len(self.stylerules) > 0:
			outbuf = []
			assert self.hasEl()
			self.getEl().set("type", "text/css")
			for _selector, sty in self.stylerules.items():
				sty.toCSSRule(outbuf, depth=depth)
			out = '\n'.join(outbuf)
			self.getEl().text = etree.CDATA(out)
			ret = True 
		return ret

class Rect(GenericSVGElem):
	"Plain rectangle, no round corners"
	def __init__(self, *args) -> None:
		if len(args) == 1 and isinstance(args[0], Re):
			super().__init__("rect", struct=args[0])
		else:
			super().__init__("rect", struct=Re(*args))

class RectRC(GenericSVGElem):
	"Round cornered rectangle"
	def __init__(self, *args) -> None:
		super().__init__("rect", struct=ReRC(*args))
	def setRCRadiuses(self, rx, ry=None):
		self.getStruct().setRCRadiuses(rx,ry=ry)
		return self

class Circle(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("circle", struct=Ci(*args))

class Ellipse(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("ellipse", struct=Elli(*args))

class MarkeableSVGElem(GenericSVGElem):
	def __init__(self, tag: str, struct: Optional[_withunits_struct] = None, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__(tag, struct=struct)
		if not marker_props is None:
			self.setMrkProps(marker_props)
		else:
			self._markerprops = None

	def _updateMarkerAttrs(self):
		if not self._markerprops is None and self.hasEl():
			self._markerprops.setXmlAttrs(self.getEl())
		return self

	def updateMarkerAttrs(self):
		if not self._markerprops is None:
			self.dispatchXMLDependentOp(self._updateMarkerAttrs)
		return self

	def setMrkProps(self, mrkprp: MrkProps):
		assert isinstance(mrkprp, MrkProps)
		self._markerprops = mrkprp
		return self.updateMarkerAttrs()

	def hasMarkerProps(self):
		return not self._markerprops is None

	def getMrkProps(self) -> Union[None, MrkProps]:
		return self._markerprops

class Line(MarkeableSVGElem):
	def __init__(self, *args, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__("line", struct=Li(*args), marker_props=marker_props)

class Path(MarkeableSVGElem):
	def __init__(self, *args, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__("path", struct=Pth(*args), marker_props=marker_props)

class AnalyticalPath(Path):

	def __init__(self, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__("", marker_props=marker_props)
		self.cmds = []

	def refresh(self):
		prevcmd = None
		buf = []
		for cmd in self.cmds:
			do_omit = False
			lett = cmd.getLetter()
			if prevcmd is None:
				assert lett.lower() == 'm', cmd.getLetter()	
				cmd.setRelative(False)			
			else:
				prevlett = prevcmd.getLetter()
				if lett.lower() == 'l':
					if prevlett.lower() in ('m', 'l') and prevcmd.isRelative() == cmd.isRelative():
						do_omit = True
				elif lett.lower() != 'm':
					if lett == prevlett:
						do_omit = True
			buf.append(cmd.get(omitletter=do_omit))
			prevcmd = cmd
		self.getStruct().setall("".join(buf))
		self.updateStructAttrs()

	def addCmd(self, p_cmd: path_command, tostart=False, refresh=False):
		if hasattr(p_cmd, 'yinvert'):
			if not self._noyinvert and not self._yinvertdelta is None:
				p_cmd.yinvert(self._yinvertdelta)
		if tostart:
			self.cmds.insert(0,p_cmd)
		else:
			self.cmds.append(p_cmd)
		if isinstance(p_cmd, pClose) or refresh:
			self.refresh()
		return self

	def delCmd(self, p_idx: int):
		del self.cmds[p_idx]
		self.refresh()

	def clear(self, refresh=True):
		del self.cmds[:]
		if refresh:
			self.refresh()

	def insCmd(self, p_idx: int, p_cmd: path_command):
		self.cmds.insert(p_idx, p_cmd)
		self.refresh()

	def addPolylinePList(self, p_list: List[Pt]):
		l = len(p_list)
		new_list = []
		for pi, pt in enumerate(p_list):
			wkpt = [strictToNumber(pt.x), strictToNumber(pt.y)]
			if not self._noyinvert and not self._yinvertdelta is None:
				wkpt[1] = self._yinvertdelta - wkpt[1]
			new_list.append(wkpt)
			cmd_added = False
			if pi == 0: # first point
				self.cmds.append(pM(*wkpt))
				cmd_added = True
			elif pi == l-1: # last point
				frstpt = new_list[0]
				diffX = frstpt[0] - wkpt[0]
				diffY = frstpt[1] - wkpt[1]
				if diffX == 0 and diffY == 0:
					self.cmds.append(pClose())
					cmd_added = True
			if not cmd_added:
				prevpt = new_list[pi -1]
				diffX = wkpt[0] - prevpt[0]
				diffY = wkpt[1] - prevpt[1]
				if diffX == 0 and diffY == 0:
					# skip this point
					continue
				if diffX == 0:
					self.cmds.append(pV(removeDecsep(diffY), relative=True))
				elif diffY == 0:
					self.cmds.append(pH(removeDecsep(diffX), relative=True))
				else:
					if abs(diffX) < abs(wkpt[0]) and abs(diffY) < abs(wkpt[1]):
						self.cmds.append(pL(removeDecsep(diffX), removeDecsep(diffY), relative=True))
					else:
						self.cmds.append(pL(*wkpt))
		self.refresh()

	def yinvert(self, p_height: Union[float, int]):
		if not self._noyinvert:
			self._yinvertdelta = p_height

class _pointsElement(MarkeableSVGElem):
	def __init__(self, tag, *args, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__(tag, struct=Pl(*args), marker_props=marker_props)
		self.initialpoint = None
		self.omitclosingpoint = False
	def hasPoints(self):
		return self.getStruct().hasPoints()
	def addPList(self, p_list: List[Pt], mindelta=MINDELTA):
		l = len(p_list)
		buf = []
		for pi, pt in enumerate(p_list):
			if pi == 0 and self.initialpoint is None: # first point
				self.initialpoint = pt
			elif pi == l-1 and not self.initialpoint is None: 
				if ptCoincidence(pt, self.initialpoint, mindelta=mindelta) and self.omitclosingpoint:
					continue
			wkpt = [strictToNumber(pt.x), strictToNumber(pt.y)]
			if not self._noyinvert and not self._yinvertdelta is None:
				wkpt[1] = self._yinvertdelta - wkpt[1]
			buf.append("{0},{1}".format(*ptEnsureStrings(wkpt)))
		self.getStruct().setall(" ".join(buf))
		self.updateStructAttrs()
		return self
	def yinvert(self, p_height: Union[float, int]):
		if not self._noyinvert:
			self._yinvertdelta = p_height
			if self.hasPoints():
				warn(UserWarning("points already defined prior to yinvert activation on this object, their y coord won't be changed."))

class Polyline(_pointsElement):
	def __init__(self, *args, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__("polyline", *args, marker_props=marker_props)

class Polygon(_pointsElement):
	def __init__(self, *args, marker_props: Optional[MrkProps] = None) -> None:
		super().__init__("polygon", *args, marker_props=marker_props)
		self.omitclosingpoint = True

class GradientStop(BaseSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("stop", struct=GraSt(*args))

class LinearGradient(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("linearGradient", struct=LiGra(*args))

class RadialGradient(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("radialGradient", struct=RaGra(*args))

class Text(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("text", struct=Tx(*args))

class TSpan(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("tspan", struct=Tx(*args))

class TRef(GenericSVGElem):
	def __init__(self, p_text: str) -> None:
		super().__init__("tref", struct=TxRf(p_text))

class TextPath(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("textPath", struct=TxPth(*args))

class Image(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("image", struct=Img(*args))

class Pattern(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("pattern", struct=Patt(*args))

class TextParagraph(Group):

	def __init__(self, x, y, textrows: Optional[Union[str, List[str]]] = None, vsep="1.2em", justify="left"):
		"""anchor - anchor point of box encolsing all text lines:
					 'lt' left-top - upper left corner"""
		super().__init__()
		if isinstance(textrows, List):
			self._textrows = textrows
		elif isinstance(textrows, str):
			self._textrows = textrows.split('\n')
		else:
			self._textrows = []
		self._vsep = vsep
		self._justify = justify
		self._txtanchorpt = (x, y)
		self.tx = None

	def setAnchoring(self, x=None, y=None):
		assert not x is None or not y is None
		if x is None:
			if not y is None:
				self._txtanchorpt[1] = y
		else:
			if y is None:
				self._txtanchorpt[0] = x
			else:
				self._txtanchorpt = (x, y)

	def getComment(self):	
		return f"TextParagraph justify:{self._justify} pt:{self._txtanchorpt}"

	def setText(self, textrows: Optional[Union[str, List[str]]]):
		assert isinstance(textrows, List) or isinstance(textrows, str)
		if isinstance(textrows, List):
			self._textrows = textrows
		elif isinstance(textrows, str):
			self._textrows = textrows.split('\n')
		self._build()

	def _build(self):
		assert not self.tx is None
		self.tx.clearChildren()
		#first = True
		for row in self._textrows:
			###########################################################################
			#  !! IMPORTANT NOTICE - Non Y-inversion is forced on TSpan element    !! #
			###########################################################################
			self.tx.addChild(TSpan(0,None,None,self._vsep).setText(row), noyinvert=True)

	def onAfterParentAdding(self):
		if not self._parentadded:
			self._parentadded = True
		else:
		 	return
		self.addTransform(Trans(*self._txtanchorpt))
		self.tx = self.addChild(Text())
		if self._justify == "left":
			self.tx.setStyle(Sty('fill', 'inherit', 'text-anchor', 'start'))
		elif self._justify == "center":
			self.tx.setStyle(Sty('fill', 'inherit', 'text-anchor', 'middle'))
		elif self._justify == "right":
			self.tx.setStyle(Sty('fill', 'inherit', 'text-anchor', 'end'))
		self._build()






