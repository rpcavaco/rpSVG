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

from rpcbSVG.SVGstyle import CSSSty, Sty
from rpcbSVG.Basics import Pt, Env, _withunits_struct, pH, pV, transform_def, path_command, rel_path_command

XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

DOCTYPE_STR = """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""


MAXCOORD = 99999999999.9
MINCOORD = -MAXCOORD

SVG_ROOT = """<svg 
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
		# l =  len(args)
		# if l <= 4:


		# else:
		# 	argslist = args
		super().__init__(*args, defaults=None)


class Ci(_withunits_struct):
	_fields = ("cx",  "cy", "r") 
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
		self.setStruct(struct)

	def _getTransform(self) -> str:
		return " ".join([t.get() for t in self._transforms])

	def hasEl(self):
		return  not self.el is None

	def getEl(self):
		assert not self.el is None, self.NO_XML_EL
		return self.el

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

	def updateStructAttrs(self):
		if not self._struct is None and not self.el is None:
			self._struct.setXmlAttrs(self.el)
		return self

	def setStruct(self, struct: _withunits_struct):
		self._struct = struct
		return self.updateStructAttrs()

	def getStruct(self) -> _withunits_struct:
		assert not self._struct is None
		if not self.el is None:
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

	def updateStyleAttrs(self):
		if not self._style is None and self.hasEl():
			self._style.setXmlAttrs(self.el)
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

	def updateTransformAttr(self):
		if len(self._transforms) > 0 and self.hasEl():
			self.getEl().set('transform', self._getTransform()) 

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

	def setEl(self, xmlel) -> None:
		assert self.el is None
		self.el = xmlel
		strct = self._struct
		if not strct is None:
			strct.setXmlAttrs(self.el)
		return self

	def removeEl(self):
		assert not self.el is None, self.NO_XML_EL
		par = self.el.getparent()
		par.remove(self.el)
		return par

	def readdElToParent(self, p_parent):
		assert not self.el is None, self.NO_XML_EL
		p_parent.append(self.el)

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
		style = self.getStyle()
		if not style is None:
			style.setXmlAttrs(xmlel)
		trtxt = self._getTransform() 
		if len(trtxt) > 0:
			xmlel.set('transform', trtxt)

	def clearTransforms(self):
		del self._transforms[:]

	def addTransform(self, tr: transform_def):
		self._transforms.append(tr)
		trtxt = self._getTransform() 
		if len(trtxt) > 0:
			self.getEl().set('transform', trtxt)
		return tr


class SVGContainer(BaseSVGElem):

	def __init__(self, tag: str, struct: Optional[_withunits_struct] = None) -> None:
		super().__init__(tag, struct=struct)
		self.content = []

	def addChild(self, p_child: BaseSVGElem):
		assert self.hasEl()
		newel = etree.SubElement(self.getEl(), p_child.tag)
		p_child.setEl(newel)
		self.content.append(p_child)
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

class Rect(BaseSVGElem):
	"Plain rectangle, no round corners"
	def __init__(self, *args) -> None:
		super().__init__("rect", struct=Re(*args))

class RectRC(BaseSVGElem):
	"Round cornered rectangle"
	def __init__(self, *args) -> None:
		super().__init__("rect", struct=ReRC(*args))

class Circle(BaseSVGElem):
	def __init__(self, *args) -> None:
		super().__init__("circle", struct=Ci(*args))

class Path(BaseSVGElem):
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
					if prevlett.lower() in ('m', 'l') and prevcmd.isRelative() == prevcmd.isRelative():
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
		# prev_pt = None
		# for pt in p_list:
		# 	self.addCmd(pM())



		# 	prev_pt = pt
		pass

	# def _refresh(self):
	# 	prevcmd = None
	# 	buf = []
	# 	for cmd in self.cmds:
	# 		newcmd = None
	# 		if prevcmd is None:
	# 			if isinstance(cmd, rel_path_command):
	# 				cmd.setRelative(False)
	# 			do_omit = False
	# 		else:
	# 			if isinstance(prevcmd, point_path_command) and isinstance(cmd, point_path_command):
	# 				if cmd.getLetter() == 'L':
	# 					diffX = prevcmd.getXDiff(cmd)
	# 					diffY = prevcmd.getYDiff(cmd)
	# 					if diffX == 0 and diffY == 0:
	# 						# skip this command
	# 						continue
	# 					if diffX == 0:
	# 						if abs(diffY) < abs(cmd.getNumeric('y')):
	# 							newcmd = pV(diffY)
	# 							newcmd.setRelative(True)
	# 						else:
	# 							newcmd = pV(cmd.getNumeric('y'))
	# 					elif diffY == 0:
	# 						if abs(diffX) < abs(cmd.getNumeric('x')):
	# 							newcmd = pH(diffX)
	# 							newcmd.setRelative(True)
	# 						else:
	# 							newcmd = pH(cmd.getNumeric('x'))
	# 					else:
	# 						if abs(diffX) < abs(cmd.getNumeric('x')) and \
	# 								abs(diffY) < abs(cmd.getNumeric('y')):
	# 							cmd.set('x', diffX)
	# 							cmd.set('y', diffY)
	# 							cmd.setRelative(True)
	# 			do_omit = prevcmd.eqLetter(cmd)
	# 		if newcmd is None:
	# 			newcmd = cmd
	# 		buf.append(newcmd.get(omitletter=do_omit))			
	# 		prevcmd = newcmd
	# 	self.getStruct().setall("".join(buf))
	# 	self.updateStructAttrs()

class SVGContent(SVGRoot):

	forbidden_user_tags = ["defs", "style"]
	def __init__(self, rect: Re, tree=None, viewbox: Optional[VBox] = None) -> None:
		super().__init__(rect, tree=tree, viewbox=viewbox)
		self._id_serial = 0
		self._defs = super().addChild(Defs())
		self._styleel = self._defs.addChild(Style())

	def _nextIDSerial(self):
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
			ret.setId(p_child.idprefix + str(self._nextIDSerial()))
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

	

