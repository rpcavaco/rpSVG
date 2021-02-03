
#import cairo
#import rsvg

from io import StringIO
from math import pi, sin, cos, sqrt, pow
from typing import Optional, List, Union
from collections import namedtuple

from lxml import etree

from rpcbSVG.SVGstyle import CSSSty, Sty
from rpcbSVG.Basics import MINDELTA, Pt, Env, _withunits_struct, pClose, pH, pL, pM, pV, transform_def, path_command, rel_path_command, ptCoincidence, removeDecsep, ptEnsureStrings

XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
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
						
class Re(_withunits_struct):
	_fields = ("x",  "y", "width", "height") 
	def __init__(self, *args, defaults=["0"]) -> None:
		if len(args) == 1 and isinstance(args[0], list):
			super().__init__(*args[0], defaults=defaults)
		else:
			super().__init__(*args, defaults=defaults)
	def fromEnv(self, p_env: Env) -> None:
		super().setall(p_env.getRectParams()) 
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

class VBox600x800(VBox):
	def __init__(self) -> None:
		super().__init__(0, 0, 600, 800)

class VBox1280x1024(VBox):
	def __init__(self) -> None:
		super().__init__(0, 0, 1280, 1024)

class ReRC(Re):
	_fields = ("x",  "y", "width", "height", "rx", "ry") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)

class Ci(_withunits_struct):
	_fields = ("cx",  "cy", "r") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])

class Elli(_withunits_struct):
	_fields = ("cx",  "cy", "rx", "ry") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])

class Li(_withunits_struct):
	_fields = ("x1",  "y1", "x2", "y2") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])

class Us(_withunits_struct):
	_fields = ("x",  "y", "width", "height", f"{{{XLINK_NAMESPACE}}}href") 
	def __init__(self, *args) -> None:
		l =  len(args)
		if l != 5:
			if l == 2:
				if isinstance(args[0], Pt) and isinstance(args[1], str):
					argslist = (args[0].x, args[0].y, None, None, args[1])
				elif isinstance(args[0], Re) and isinstance(args[1], str):
					argslist = (args[0].x, args[0].y, args[0].width, args[0].height, args[1])
				else:
					raise TypeError(f"'Us' element requires exactly 5 argumens, {l} given")
			else:
				raise TypeError(f"'Us' element requires exactly 5 argumens, {l} given")
		else:
			argslist = args
		super().__init__(*argslist, defaults=None)

class Pth(_withunits_struct):
	_fields = ("d") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)

class Pl(_withunits_struct):
	_fields = ("points",) 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)

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
		self.setStruct(struct)

	def _getTransform(self) -> str:
		return " ".join([t.get() for t in self._transforms])

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
		assert not self.el is None, self.NO_XML_EL
		par = self.el.getparent()
		par.remove(self.el)
		return par

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
				out.append(f"{x}={self.el.get(x)}")
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
		if not self._struct is None:
			self._struct.setXmlAttrs(self.el)
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
			self._struct.getFromXmlAttrs(self.el)
		return self._struct

	def getSelector(self, select='id'):
		assert select in (None, "id", "class", "tag")
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

	def _updateStyleAttrs(self):
		if not self._style is None and self.hasEl():
			self._style.setXmlAttrs(self.el)
		return self

	def updateStyleAttrs(self):
		if not self._struct is None:
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
		if not self._style is None and not self.el is None:
			self._style.fromXmlAttrs(self.el)
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
		assert not self.el is None, self.NO_XML_EL
		return self.el.getparent()

	def readdElToParent(self, p_parent):
		assert not self.el is None, self.NO_XML_EL
		p_parent.append(self.el)

	def delEl(self):
		self.el.getparent().remove(self.el)
		self.el = None

	def _setId(self, idval):
		assert isinstance(idval, str)
		assert not self.el is None, self.NO_XML_EL
		self.el.set('id', idval)
		return self

	def setId(self, idval):
		self.dispatchXMLDependentOp(self._setId, args=(idval,))
		return self

	def getId(self):
		assert not self.el is None, self.NO_XML_EL
		assert "id" in self.el.keys()
		return self.el.get('id')

	def hasId(self) -> bool:
		assert not self.el is None, self.NO_XML_EL
		return "id" in self.el.keys()

	def _setClass(self, clsval):
		assert isinstance(clsval, str)
		assert not self.el is None, self.NO_XML_EL
		self.el.set('class', clsval)
		return self

	def setClass(self, clsval):
		self.dispatchXMLDependentOp(self._setClass, args=(clsval,))
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

	def clearTransforms(self):
		del self._transforms[:]

	def addTransform(self, tr: transform_def):
		self._transforms.append(tr)
		trtxt = self._getTransform() 
		if len(trtxt) > 0:
			self.getEl().set('transform', trtxt)
		return tr

class GenericSVGElem(BaseSVGElem):

	def __init__(self, tag: str, struct: Optional[_withunits_struct] = None) -> None:
		self.content = []
		super().__init__(tag, struct=struct)

	def addChild(self, p_child: BaseSVGElem):
		assert self.hasEl()
		newel = etree.SubElement(self.getEl(), p_child.tag)
		p_child.setEl(newel)
		self.content.append(p_child)
		
		if not p_child.hasId():
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

class SVGContainer(GenericSVGElem):

	def __init__(self, tag: str, struct: Optional[_withunits_struct] = None, viewbox: Optional[VBox] = None) -> None:
		super().__init__(tag, struct=struct)
		# self.content = []
		self.genIDMethod = None
		if not viewbox is None:
			self.setViewbox(viewbox)

	def setGenIdMethod(self, p_method):
		self.genIDMethod = p_method

	def genNextId(self):
		ret = None
		if not self.genIDMethod is None:
			ret = self.genIDMethod()
		return ret

	def _setViewbox(self, p_viewbox: VBox):
		assert isinstance(p_viewbox, VBox)
		p_viewbox.setXmlAttrs(self.el)
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
		self.el = self.tree.getroot()
		self.setRect(rect)
		# Viewbox must be (re)inited here: in SVGContainer __init__ , 
		# 	setViewbox finds no XML Element, is not yet created)
		if not viewbox is None:
			self.setViewbox(viewbox)

	def setRect(self, p_rect: Re):
		assert isinstance(p_rect, Re)
		self.setStruct(p_rect)
		p_rect.setXmlAttrs(self.el)
		return self

class Group(SVGContainer):
	def __init__(self) -> None:
		super().__init__('g')

class Defs(SVGContainer):
	def __init__(self) -> None:
		super().__init__('defs')

class Use(BaseSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("use", struct=Us(*args))

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
		super().__init__("rect", struct=Re(*args))

class RectRC(GenericSVGElem):
	"Round cornered rectangle"
	def __init__(self, *args) -> None:
		super().__init__("rect", struct=ReRC(*args))

class Circle(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("circle", struct=Ci(*args))

class Ellipse(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("ellipse", struct=Elli(*args))

class Line(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("line", struct=Li(*args))

class Path(GenericSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("path", struct=Pth(*args))

class AnalyticalPath(Path):
	def __init__(self) -> None:
		super().__init__("")
		self.cmds = []
	def _refresh(self):
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
	def addCmd(self, p_cmd: path_command):
		self.cmds.append(p_cmd)
		self._refresh()
	def delCmd(self, p_idx: int):
		del self.cmds[p_idx]
		self._refresh()
	def insCmd(self, p_idx: int, p_cmd: path_command):
		self.cmds.insert(p_idx, p_cmd)
		self._refresh()
	def addPolylinePList(self, p_list: List[Pt]):
		l = len(p_list)
		for pi, pt in enumerate(p_list):
			cmd_added = False
			if pi == 0: # first point
				self.cmds.append(pM(*pt))
				cmd_added = True
			elif pi == l-1: # last point
				frstpt = p_list[0]
				diffX = float(frstpt.x) - float(pt.x)
				diffY = float(frstpt.y) - float(pt.y)
				if diffX == 0 and diffY == 0:
					self.cmds.append(pClose())
					cmd_added = True
			if not cmd_added:
				prevpt = p_list[pi -1]
				diffX = float(pt.x) - float(prevpt.x)
				diffY = float(pt.y) - float(prevpt.y)
				if diffX == 0 and diffY == 0:
					# skip this point
					continue
				if diffX == 0:
					self.cmds.append(pV(removeDecsep(diffY), relative=True))
				elif diffY == 0:
					self.cmds.append(pH(removeDecsep(diffX), relative=True))
				else:
					if abs(diffX) < abs(float(pt.x)) and abs(diffY) < abs(float(pt.y)):
						self.cmds.append(pL(removeDecsep(diffX), removeDecsep(diffY), relative=True))
					else:
						self.cmds.append(pL(*pt))
		self._refresh()

class _pointsElement(GenericSVGElem):
	def __init__(self, tag, *args) -> None:
		super().__init__(tag, struct=Pl(*args))
		self.initialpoint = None
		self.omitclosingpoint = False
	def addPList(self, p_list: List[Pt], mindelta=MINDELTA):
		l = len(p_list)
		buf = []
		for pi, pt in enumerate(p_list):
			if pi == 0 and self.initialpoint is None: # first point
				self.initialpoint = pt
			elif pi == l-1 and not self.initialpoint is None: 
				if ptCoincidence(pt, self.initialpoint, mindelta=mindelta) and self.omitclosingpoint:
					continue
			buf.append("{0},{1}".format(*ptEnsureStrings(pt)))
		self.getStruct().setall(" ".join(buf))
		self.updateStructAttrs()

class Polyline(_pointsElement):
	def __init__(self, *args) -> None:
		super().__init__("polyline", *args)

class Polygon(_pointsElement):
	def __init__(self, *args) -> None:
		super().__init__("polygon", *args)
		self.omitclosingpoint = True


class SVGContent(SVGRoot):

	forbidden_user_tags = ["defs", "style"]
	def __init__(self, rect: Re, viewbox: Optional[VBox] = None) -> None:
		super().__init__(rect, viewbox=viewbox)
		self._id_serial = 0
		self._defs = super().addChild(Defs())
		self._styleel = self._defs.addChild(Style())

	def nextIDSerial(self):
		ret = self._id_serial
		self._id_serial = self._id_serial + 1
		return ret

	def addChild(self, p_child: BaseSVGElem, todefs: Optional[bool] = False) -> BaseSVGElem:
		if p_child.tag in self.forbidden_user_tags:
			raise TagOutOfDirectUserManipulation(p_child.tag)
		if todefs:
			assert not self._defs is None
			ret = self._defs.addChild(p_child)
		else:
			ret = super().addChild(p_child)
		if not ret.hasId():
			ret.setId(p_child.idprefix + str(self.nextIDSerial()))
		if isinstance(ret, SVGContainer):
			ret.setGenIdMethod(self.nextIDSerial)
		return ret

	def addStyleRule(self, p_child: CSSSty) -> str:
		return self._styleel.addRule(p_child)

	def delStyleRule(self, selector: str) -> bool:
		return self._styleel.delRule(selector)

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

	

