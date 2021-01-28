'''
Construção de um documento SVG
'''

#import cairo
#import rsvg

from io import StringIO
from math import pi, sin, cos, sqrt, pow
from typing import Optional, List, Union
from collections import namedtuple

from lxml import etree

from rpcbSVG.SVGstyle import Sty
from rpcbSVG.Basics import Pt, Env, _withunits_struct, _attrs_struct

XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

DOCTYPE_STR = """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""


MAXCOORD = 99999999999.9
MINCOORD = -MAXCOORD

SVG_ROOT = """<svg version="1.1"
	 xmlns="{0}" 
	 xmlns:xlink="{1}" />
	 """.format(SVG_NAMESPACE, XLINK_NAMESPACE)

DECLARATION_ROOT = """<?xml version="1.0" standalone="no"?>
{0}""".format(SVG_ROOT)
	 
POINTS_FORMAT = "{0:.2f},{1:.2f}"

SPECIAL_ATTRS = ('x','y','width','height','id','class')

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
						
class Re(_withunits_struct):
	_fields = ("x",  "y", "width", "height") 
	def __init__(self, *args) -> None:
		if len(args) == 1 and isinstance(args[0], list):
			super().__init__(*args[0], defaults=["0"])
		else:
			super().__init__(*args, defaults=["0"])
	def fromEnv(self, p_env: Env) -> None:
		super().set(p_env.getRectParams()) 
		return self
	def full(self):
		self.y = self.x = "0"
		self.width = self.height = "100"
		self.setUnits('%')
		return self

class VBox(_withunits_struct):
	_fields = ("viewBox",)
	def __init__(self, *args) -> None:
		if len(args) == 1 and isinstance(args[0], list):
			super().__init__(*args[0], defaults=["0"])
		else:
			super().__init__(*args, defaults=["0"])
		rect = Re(*args)
		cont = " ".join(list(rect.iterUnitsRemoved()))
		super().__init__(cont)
	def cloneFromRect(self, p_rect: Re, scale: Optional[float] = None):
		if not scale is None:
			cont = " ".join([str(round(float(at) * scale)) for at in p_rect.iterUnitsRemoved()])
		else:
			cont = " ".join(list(p_rect.iterUnitsRemoved()))
		self.viewBox = cont

# clone from Envelope: vb_instance.cloneFromRect(Re().fromEnvelope())

class VBox600x800(VBox):
	def __init__(self) -> None:
		super().__init__(0, 0, 600, 800)

class VBox1280x1024(VBox):
	def __init__(self) -> None:
		super().__init__(0, 0, 1280, 1024)


class Ci(_withunits_struct):
	_fields = ("cx",  "cy", "rad") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])


class BaseSVGElem(object):

	NO_XML_EL = "XML Element not created yet"

	def __init__(self, tag: str, 
			struct: Optional[_withunits_struct] = None) -> None:
		self.tag = tag
		self._struct = None
		self.idprefix = tag[:3].title()
		self.el = None
		self.setStruct(struct)

	def __repr__(self):
		out = [
			f"tag={str(self.tag)}"
		]
		if not self.el is None:
			for x in self.el.keys():
				out.append(f"{x}={self.el.get(x)}")
		return ' '.join(out)

	def setStruct(self, struct: _withunits_struct):
		self._struct = struct
		if not self.el is None:
			self._struct.setXmlAttrs(self.el)
		return self

	def getStruct(self) -> _withunits_struct:
		assert not self._struct is None
		if not self.el is None:
			self._struct.getFromXmlAttrs(self.el)
		return self._struct

	def setStyle(self, style: Sty):
		if not self.el is None:
			style.setXmlAttrs(self.el)
		return self

	def getStyleSelector(self, select='id'):
		assert select in ("id", "class", "tag")
		sel = None
		if select == 'id':
			if self.hasId():
				sel = '#' + self.getId()
		elif select == 'class':
			if self.hasClass():
				sel = '.' + self.getClass()
		elif select == 'tag':
			sel = self.tag
		return sel

	def getSS(self, select='id'):
		return self.getStyleSelector(select=select)

	def getStyle(self, select='id'):
		ret = None
		if not self.el is None:
			sel = self.getStyleSelector(select=select)
			ret = Sty(selector=sel)
			ret.fromXmlAttrs(self.el)
		return ret

	def hasEl(self):
		return  not self.el is None

	def getEl(self):
		assert not self.el is None, self.NO_XML_EL
		return self.el

	def setEl(self, xmlel) -> None:
		assert self.el is None
		self.el = xmlel
		strct = self._struct
		if not strct is None:
			strct.setXmlAttrs(self.el)
		return self

	def delEl(self):
		self.el.getparent().remove(self.el)
		self.el = None

	def setId(self, idval):
		assert isinstance(idval, str)
		assert not self.el is None, self.NO_XML_EL
		self.el.set('id', idval)
		return self

	def getId(self):
		assert not self.el is None, self.NO_XML_EL
		assert "id" in self.el.keys()
		return self.el.get('id')

	def hasId(self) -> bool:
		assert not self.el is None, self.NO_XML_EL
		return "id" in self.el.keys()

	def setClass(self, clsval):
		assert isinstance(clsval, str)
		assert not self.el is None, self.NO_XML_EL
		self.el.set('class', clsval)
		return self

	def getClass(self):
		assert not self.el is None, self.NO_XML_EL
		assert "class" in self.el.keys()
		return self.el.get('class')

	def hasClass(self) -> bool:
		assert not self.el is None, self.NO_XML_EL
		return "class" in self.el.keys()

	def getTag(self):
		return self.tag

	def setXmlAttrs(self, xmlel) -> None:  
		strct = self.getStruct()
		assert not strct is None
		strct.setXmlAttrs(xmlel)

class SVGContainer(BaseSVGElem):

	def addChild(self, p_child: BaseSVGElem):
		assert self.hasEl()
		newel = etree.SubElement(self.getEl(), p_child.tag)
		p_child.setEl(newel)
		return p_child

	def addChildTag(self, p_tag: str):
		assert self.hasEl()
		newel = etree.SubElement(self.getEl(), p_tag)
		return newel

	def clear(self):
		assert self.hasEl()
		del self.getEl()[:]

class SVGRoot(SVGContainer):

	def __init__(self, rect: Re, tree = None, viewbox: Optional[VBox] = None) -> None:
		super().__init__("svg", struct=rect)
		if tree is None:
			self.tree = etree.parse(StringIO(SVG_ROOT))
		elif hasattr(tree, 'getroot'):
			self.tree = tree
		else:
			raise RuntimeError("object supplied is not ElementTree")
		assert not self.tree is None
		self.el = self.tree.getroot()
		self.setRect(rect)
		if not viewbox is None:
			self.setViewbox(viewbox)

	def setRect(self, p_rect: Re):
		assert isinstance(p_rect, Re)
		self.setStruct(p_rect)
		p_rect.setXmlAttrs(self.el)
		return self

	def setViewbox(self, p_viewbox: VBox):
		assert isinstance(p_viewbox, VBox)
		p_viewbox.setXmlAttrs(self.el)
		return self

	def setIdentityViewbox(self, scale: Optional[float] = None):
		strct = self.getStruct()
		assert not strct is None
		vb = VBox()
		vb.cloneFromRect(self.getStruct(), scale=scale)
		return self.setViewbox(vb)

class Group(SVGContainer):
	def __init__(self) -> None:
		super().__init__('g')

class Defs(SVGContainer):
	def __init__(self) -> None:
		super().__init__('defs')

class Style(BaseSVGElem):

	def __init__(self) -> None:
		super().__init__('style')
		self.stylerules = {}

	def addRule(self, p_child: Sty, selector: Optional[str] = None) -> str:
		if not selector is None:
			p_child.setSelector(selector)
		assert p_child.hasSelector()
		ret = p_child.getSelector()
		self.stylerules[ret] =p_child
		return ret

	def delRule(self, selector: str) -> bool:
		ret = False
		if selector in self.stylerules.keys():
			del self.stylerules[selector]
			ret = True
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


class Rect(BaseSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("rect", struct=Re(*args))

class Circle(BaseSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("circle", struct=Ci(*args))


class SVGContent(SVGRoot):

	forbidden_user_tags = ["defs", "style"]
	def __init__(self, rect: Re, tree=None, viewbox: Optional[VBox] = None) -> None:
		super().__init__(rect, tree=tree, viewbox=viewbox)
		self._id_serial = 0
		self._defs = super().addChild(Defs())
		self._style = self._defs.addChild(Style())

	def _nextIDSerial(self):
		ret = self._id_serial
		self._id_serial = self._id_serial + 1
		return ret

	def addChild(self, p_child: BaseSVGElem):
		if p_child.tag in self.forbidden_user_tags:
			raise TagOutOfDirectUserManipulation(p_child.tag)
		ret = super().addChild(p_child)
		if not ret.hasId():
			ret.setId(p_child.idprefix + str(self._nextIDSerial()))
		return ret

	def addStyleRule(self, p_child: Sty, selector: Optional[str] = None) -> str:
		return self._style.addRule(p_child, selector = selector)

	def delStyleRule(self, selector: str) -> bool:
		return self._style.delRule(selector)

	def render(self):
		return self._style.render(depth=-1)

	def toBytes(self, inc_declaration=False, inc_doctype=False, pretty_print=True):
		nostyles = False
		if not self.render():
			nostyles = True
			self._style.delEl()

		if inc_doctype:
			ret = etree.tostring(self.getEl(), doctype=DOCTYPE_STR, xml_declaration=inc_declaration, pretty_print=pretty_print, encoding='utf-8')
		else:
			ret = etree.tostring(self.getEl(), xml_declaration=inc_declaration, pretty_print=pretty_print, encoding='utf-8')	

		if nostyles:
			self._style.setEl(Style())

		return ret

	def toString(self, inc_declaration=False, inc_doctype=False, pretty_print=True):
		return self.toBytes(inc_declaration=inc_declaration, inc_doctype=inc_doctype, pretty_print=pretty_print).decode('utf-8')

	

