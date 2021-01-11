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

from rpcbSVG.SVGstyle import toCSS, Fill, Stroke, TextAttribs
from rpcbSVG.BasicGeom import Envelope, Pt

XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

DOCTYPE_STR = """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""

SVG_ROOT = """<svg version="1.1"
	 xmlns="{0}" 
	 xmlns:xlink="{1}" />
	 """.format(SVG_NAMESPACE, XLINK_NAMESPACE)

DECLARATION_ROOT = """<?xml version="1.0" standalone="no"?>
{0}""".format(SVG_ROOT)
	 
POINTS_FORMAT = "{0:.2f},{1:.2f}"

SPECIAL_ATTRS = ('x','y','width','height','id','class')

def polar2rect(ang, rad):
	return POINTS_FORMAT.format(cos(ang) * rad, sin(ang) * rad )

# def renderToFile(svgstr, w, h, filename):
# 	img = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
# 	ctx = cairo.Context(img)
# 	svg = rsvg.Handle(data=svgstr)
# 	svg.render_cairo(ctx)
# 	img.write_to_png(filename)

def getCSSId(domelem):	
	return '#' + domelem.get('id')	
			

def addFeOffset(filterroot, dx, dy, instr="SourceGraphic", result="offOut"):
	fe = etree.SubElement(filterroot, 'feOffset')
	fe.set('dx', str(dx))
	fe.set('dy', str(dy))
	fe.set('in', instr)
	fe.set('result', result)

def addFeBlend(filterroot, instr2, instr="SourceGraphic", mode="normal"):
	fe = etree.SubElement(filterroot, 'feBlend')
	fe.set('in', instr)
	fe.set('in2', instr2)
	fe.set('mode', mode)

def addFeGaussianBlur(filterroot, instr, result, stdDeviation):
	fe = etree.SubElement(filterroot, 'feGaussianBlur')
	fe.set('in', instr)
	fe.set('result', result)
	fe.set('stdDeviation', str(stdDeviation))
							
class BasicDims(object):
	def __init__(self, width, height, x=0, y=0):
		self.x = int(x)
		self.y = int(y)
		self.width = int(width)
		self.height = int(height)
	def cloneFrom(self, other, scale=1.0):
		self.x = other.x * scale
		self.y = other.y * scale
		self.width = other.width * scale
		self.height = other.height * scale
	def cloneFromZeroOrigin(self, other):
		self.x = 0
		self.y = 0
		self.width = other.width
		self.height = other.height
		
class Dims(BasicDims):
	def __init__(self, width, height, x=0, y=0, unit='px'):
		super().__init__(width, height, x=x, y=y)
		self.unit = unit
	def getWidthStr(self, scale=1.0):
		return "{0}{1}".format(round(self.width * scale), self.unit)
	def getHeightStr(self, scale=1.0):
		return "{0}{1}".format(round(self.height * scale), self.unit)

class Viewport(Dims):
	def __init__(self, width, height, x=0, y=0):
		super().__init__(width, height, x=x, y=y)
	def toString(self):
		return "{0} {1} {2} {3}".format(round(self.x), round(self.y), round(self.width), round(self.height))

class WorldViewport(Viewport):
	def __init__(self, extlist):
		minx, miny, maxx, maxy = extlist
		height = abs(maxy - miny)
		super().__init__(abs(maxx-minx), height, x=minx, y=-miny-height)
	
class DimsFull(Dims):
	def __init__(self):
		super().__init__(100, 100, unit='%')

# class attrIface(object):
# 	def transf(self, svgelem):
# 		for a in dir(self):
# 			if not a.startswith("__"):
# 				if not callable(getattr(self, a)):
# 					svgelem.set(getattr(self, a))

class Rect(namedtuple('Rect', ("x", "y", "width", "height"))):
    
	def fromEnvelope(self, env: Envelope) -> None:
		self.x = env.minx
		self.y = env.miny
		self.width = env.getWidth()
		self.height = env.getHeight()

class BaseSVGElem(object):

	def __init__(self, attr_interfaces: List[namedtuple]) -> None:
		self.el = None
		self.attr_interfaces = attr_interfaces # Namedtuple classes

	def getEl(self):
		assert not self.el is None
		return self.el

	def setId(self, idval):
		assert isinstance(idval, str)
		assert not self.el is None
		self.el.set('id', idval)

	def getId(self):
		assert not self.el is None
		assert "id" in self.el.keys()
		return self.el.get('id')

	def setAttrs(self, inobj: namedtuple) -> None:
		assert not self.el is None
		for c in self.attr_interfaces:
			if isinstance(inobj, c):
				for fld in inobj._fields:
					self.el.set(fld, str(getattr(inobj, fld)))
				break



class SVGRoot(BaseSVGElem):
	def __init__(self, tree = None, rect: Optional[Rect] = None) -> None:
		super().__init__([Rect])
		if tree is None:
			self.tree = etree.parse(StringIO(SVG_ROOT))
		elif hasattr(tree, 'getroot'):
			self.tree = tree
		else:
			raise RuntimeError("object supplied is not ElementTree")
		assert not self.tree is None
		self.el = self.tree.getroot()
		if not rect is None:
			self.setAttrs(rect)

class GenericElem(BaseSVGElem):
	def __init__(self, tag: str, parent, idval: Optional[str] = None) -> None:
		assert not parent is None
		if hasattr(parent, 'getroot'):
			rootel = parent.getroot()
		elif isinstance(parent, BaseSVGElem):
			rootel = parent.getRoot()
		else:
			rootel = None
			raise RuntimeError(f"Wrong parent type: {type(parent)}")
		self.el = etree.SubElement(rootel, tag)
		if not idval is None:
			self.el.set('id', idval)


class SVGGroup(BaseSVGElem):
	def __init__(self, parent, idval: Optional[str]) -> None:
		super().__init__('g', parent=parent, idval=idval)


class SVGContent(SVGGroup):
	def __init__(self, thisroot_or_parent, creationtag=None, defscontent=None, attribs=None):
		if hasattr(thisroot_or_parent, 'getRoot'):
			rootel = thisroot_or_parent.getRoot()
		else:
			rootel = thisroot_or_parent
		if not creationtag is None:
			self.root = etree.SubElement(rootel, creationtag)
		else:
			self.root = rootel
		if not attribs is None:
			for k in list(attribs.keys()):
				self.root.set(k, str(attribs[k]))
		self.defscontent = defscontent
		self.dims = None
		self.envelope = Envelope()
		self.groups = {}
	def addGroup(self, idval=None, cls=None, attribs=None, todefs=False):
		if idval is None:
			idval = 'G{0}'.format(self._nextIDSerial())
		if todefs:
			assert not self.getDefs() is None, "addGroup to defs: no DEFS defined on this SVGContent"
			self.groups[idval] = GROUPContent(self.getDefs(), idval=idval, attribs=attribs)
		else:
			self.groups[idval] = GROUPContent(self, idval=idval, attribs=attribs)
		return self.groups[idval]
	def getGroup(self, idval, cls=None):
		if not idval in list(self.groups.keys()):
			raise MissingGroup(idval, list(self.groups.keys()))
		else:
			return self.groups[idval]
	def getRoot(self):
		return self.root
	def getDefs(self):
		return self.defscontent
	def getDims(self):
		return self.dims
	def setViewbox(self, viewport):		
		if self.root.tag in [
				'{' + SVG_NAMESPACE + '}svg', '{' + SVG_NAMESPACE + '}symbol',
				'{' + SVG_NAMESPACE + '}image', '{' + SVG_NAMESPACE + '}marker',
				'{' + SVG_NAMESPACE + '}pattern', '{' + SVG_NAMESPACE + '}view']:
			self.root.set("viewBox",viewport.toString())		
		elif self.root.tag in ['svg','symbol','image','marker','pattern','view']:
			self.root.set("viewBox",viewport.toString())
		else:
			raise RuntimeError("'{0}': not a viewBox element".format(self.root.tag))
	def setIdentityViewbox(self, scale=1.0):
		vb = Viewport(0,0)
		vb.cloneFrom(self.dims, scale=scale)
		self.setViewbox(vb)
		return vb
	def setDims(self, dimsObject, scale=1.0):
		if self.root.tag.endswith('svg'):
			self.dims = dimsObject
			self.root.set("x",str(dimsObject.x))
			self.root.set("y",str(dimsObject.x))
			self.root.set("width",dimsObject.getWidthStr())
			self.root.set("height",dimsObject.getHeightStr())
		else:
			raise RuntimeError("<{0}>.setDims: not a dims element".format(self.root.tag))
		self.setIdentityViewbox(scale=scale)
	def addFilter(self, idval=None, todefs=True):
		if idval is None:
			idval = 'FLT{0}'.format(self._nextIDSerial())
		if todefs:
			assert not self.getDefs() is None, "addFilter to defs: no DEFS defined on this SVGContent"
			flt = etree.SubElement(self.defscontent.getRoot(), 'filter')
		else:
			flt = etree.SubElement(self.root, 'filter')
		flt.set('id', idval)
		flt.set('width', '150%')
		flt.set('height', '150%')
		return flt
	def addUse(self, x, y, refid, idval=None, cls=None, attribs=None):
		if idval is None:
			trueid = 'U{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		u = etree.SubElement(self.root, 'use')
		u.set('{' + XLINK_NAMESPACE + '}href', '#{0}'.format(refid))
		u.set('id',trueid)
		if not cls is None:
			u.set('class')
		u.set('x', str(x))
		u.set('y', str(y))
		if not attribs is None:
			for k in list(attribs.keys()):
				if not k in SPECIAL_ATTRS:
					u.set(k, str(attribs[k]))
		return u	
	def addRect(self, x, y, width, height, attribs=None, idval=None, cls=None, todefs=False, ns_stroke=None):
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			r = etree.SubElement(self.defscontent.getRoot(), 'rect')
		else:
			r = etree.SubElement(self.root, 'rect')
		if idval is None:
			trueid = 'R{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		r.set('id',trueid)
		r.set('x', str(x))
		r.set('y', str(y))
		r.set('width', str(width))
		r.set('height', str(height))
		if not attribs is None:
			for k in list(attribs.keys()):
				if not k in SPECIAL_ATTRS:
					r.set(k, str(attribs[k]))
		return r
	def addRectFromEnvelope(self, env, attribs=None, idval=None, cls=None, todefs=False):
		rect_params = []
		env.getRectParams(rect_params)
		return self.addRect(*rect_params, attribs=attribs, idval=idval, todefs=todefs)
	def addPath(self, pathdatastring, attribs=None, idval=None, cls=None, todefs=False, ns_stroke=None):
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			p = etree.SubElement(self.defscontent.getRoot(), 'path')
		else:
			p = etree.SubElement(self.root, 'path')
		if idval is None:
			trueid = 'P{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		p.set('id',trueid)
		p.set('d', pathdatastring)
		if not attribs is None:
			for k in list(attribs.keys()):
				if not k in ['id','d']:
					p.set(k, str(attribs[k]))
		return p
	def addPolygon(self, pointsdatastring, attribs=None, idval=None, cls=None, todefs=False):
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			p = etree.SubElement(self.defscontent.getRoot(), 'polygon')
		else:
			p = etree.SubElement(self.root, 'polygon')
		if idval is None:
			trueid = 'PO{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		p.set('id',trueid)
		p.set('points', pointsdatastring)
		if not attribs is None:
			for k in list(attribs.keys()):
				if not k in ['id','points']:
					p.set(k, str(attribs[k]))
		return p
	def addCircle(self, cx, cy, rad, attribs=None, idval=None, cls=None, todefs=False, ns_stroke=False):
		if idval is None:
			trueid = 'C{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			c = etree.SubElement(self.defscontent.getRoot(), 'circle')
		else:
			c = etree.SubElement(self.root, 'circle')
		c.set('id',trueid)
		if todefs:
			c.set('cx', '0')
			c.set('cy', '0')
		else:
			c.set('cx', str(cx))
			c.set('cy', str(cy))
		c.set('r', str(rad))
		if ns_stroke: # nao usar, apenas SVG 2
			c.set('vector-effect', 'non-scaling-stroke')
		if not attribs is None:
			for k in list(attribs.keys()):
				if not k in ['id','cx','cy','r']:
					c.set(k, str(attribs[k]))
		return c
	def addImage(self, x, y, width, height, image_iri, attribs=None, idval=None, cls=None, todefs=False):
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			img = etree.SubElement(self.defscontent.getRoot(), 'image')
		else:
			img = etree.SubElement(self.root, 'image')
		if idval is None:
			trueid = 'I{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		img.set('id',trueid)
		img.set('{' + XLINK_NAMESPACE + '}href', '{0}'.format(image_iri))
		img.set('x',str(x))
		img.set('y',str(y))
		img.set('width',str(width))
		img.set('height',str(height))
		if not attribs is None:
			for k, val in attribs.items():
				if k not in SPECIAL_ATTRS:
					img.set(k, val)
		return img	
	def addText(self, x, y, content, attribs=None, idval=None, cls=None, deltay=None, todefs=False):
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			txt = etree.SubElement(self.defscontent.getRoot(), 'text')
		else:
			txt = etree.SubElement(self.root, 'text')
		if idval is None:
			trueid = 'T{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		txt.set('id',trueid)
		txt.set('x',str(x))
		txt.set('y',str(y))
		if not deltay is None:
			txt.set('dy', str(deltay))
		if not attribs is None:
			for k, val in attribs.items():
				if k not in SPECIAL_ATTRS:
					txt.set(k, val)
		txt.text = content
		return txt
	def addTextAlongPath(self, content, alongpathid, attribs=None, idval=None, cls=None, deltay=None, startoffset=40):
		txt = etree.SubElement(self.root, 'text')
		if idval is None:
			trueid = 'T{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		txt.set('id',trueid)

		txtpath = etree.SubElement(txt, 'textPath')
		txtpath.set('{' + XLINK_NAMESPACE + '}href', '#{0}'.format(alongpathid))
		txtpath.set('startOffset', '{0}%'.format(startoffset))
		
		if not deltay is None:
			txtspan = etree.SubElement(txtpath, 'tspan')
			txtspan.set('dy', str(deltay))
			txtspan.text = content
		else:
			txtpath.text = content

		if not attribs is None:
			for k, val in attribs.items():
				if k not in SPECIAL_ATTRS:
					txt.set(k, val)

		return txt
	def addLinearGradient(self, orig: Optional[Pt]=None, dest: Optional[Pt]=None, idval=None, cls=None, todefs=False):
		if todefs:
			assert not self.getDefs() is None, "add... element to defs: no DEFS defined on this SVGContent"
			lg = etree.SubElement(self.defscontent.getRoot(), 'linearGradient')
		else:
			lg = etree.SubElement(self.root, 'linearGradient')
		if idval is None:
			trueid = 'T{0}'.format(self._nextIDSerial())
		else:
			trueid = idval
		lg.set('id',trueid)
		if not orig is None and not dest is None:
			lg.set('x1', orig.x)
			lg.set('x2', dest.x)
			lg.set('y1', orig.y)
			lg.set('y2', dest.y)
		return lg
	# addGradStop/self, idval=x


class DEFSContent(SVGContent):
	def __init__(self, parent):
		super().__init__(parent, creationtag='defs')

class GROUPContent(SVGContent):
	def __init__(self, parent, idval=None, attribs=None):
		super().__init__(parent, creationtag='g', attribs=attribs)
		self.setId(idval)
	def set(self, attr, val):
		self.root.set(attr, val)

class MissingGroup(Exception):
	def __init__(self, idval, existing_list):
		self.idval = idval
		self.existing_list = existing_list
	def __str__(self):
		return "missing group: '{0}'; existing groups: {1}".format(self.idval, ','.join(self.existing_list))
	
class MainContent(SVGContent):
	def __init__(self, docroot):
		super().__init__(docroot, defscontent=DEFSContent(docroot))

class InnerContent(SVGContent):
	def __init__(self, mainContent):
		super().__init__(mainContent.root, creationtag='svg', defscontent=None)

class SVGDocOld(object):
	
	SVG_DYN_METHOD_NAMES = [
		"addFilter",
		"addRect",
		"addCircle",
		"addPolygon",
		"addPath",
		"addText",
		"addTextAlongPath",
		"addGroup",
		"addUse",
		"setDims"
	]

	def __init__(self, rootTemplate):

		def make_dyn_method(p_cls, p_meth_name):
			def fn(self, *args, **kwargs):
				inner_fn = getattr(self.content, p_meth_name)	
				return inner_fn(*args, **kwargs)
			setattr(p_cls, p_meth_name, fn)
		self.id_serial = 0
		
		self.tree = etree.parse(StringIO(rootTemplate))
		self.content = MainContent(self.tree.getroot())
		self.styles = {}
		
		for mname in self.SVG_DYN_METHOD_NAMES:
			make_dyn_method(self.__class__, mname)
		
	def _nextIDSerial(self):
		ret = self.id_serial
		self.id_serial = self.id_serial + 1
		return ret
		
	def getRoot(self):
		return self.tree.getroot()
	def addStyle(self, key, newstyleobj):
		if key not in list(self.styles.keys()):
			self.styles[key] = []
		self.styles[key].append(newstyleobj)
	def addStyleFromDict(self, style_key, the_dict, symbscale=1.0, labsymbscale=None):
		styles = {}
		sw = None
		if labsymbscale is None:
			lsscale = symbscale
		else:
			lsscale = labsymbscale
# TODO: Verificar a passagem de todos os atributos necessários
		for key in list(the_dict.keys()):
			if key.lower().strip() == 'fill':
				if not 'fill' in list(styles.keys()):
					styles['fill'] = Fill(the_dict[key])
			elif key.lower().strip() == 'fill-opacity':
				if not 'fill' in list(styles.keys()):
					styles['fill'] = Fill(the_dict['fill'])
				styles['fill'].setOpacity(the_dict[key])
			elif key.lower().strip() == 'stroke':
				styles['stroke'] = Stroke(the_dict[key], symbscale=symbscale)
			elif key.lower().strip() == 'stroke-opacity':
				if not 'stroke' in list(styles.keys()):
					styles['stroke'] = Stroke(the_dict['stroke'], symbscale=symbscale)
				styles['stroke'].setOpacity(the_dict[key])
			elif key.lower().strip() == 'stroke-dasharray':
				if not 'stroke' in list(styles.keys()):
					styles['stroke'] = Stroke(the_dict['stroke'], symbscale=symbscale)
				styles['stroke'].setDasharray(the_dict[key])
			elif key.lower().strip() == 'stroke-linejoin':
				if not 'stroke' in list(styles.keys()):
					styles['stroke'] = Stroke(the_dict['stroke'], symbscale=symbscale)
				styles['stroke'].setLinejoin(the_dict[key])
			elif key.lower().strip() == 'stroke-linecap':
				if not 'stroke' in list(styles.keys()):
					styles['stroke'] = Stroke(the_dict['stroke'], symbscale=symbscale)
				styles['stroke'].setLinecap(the_dict[key])
			elif key.lower().strip() == 'stroke-width':
				sw = the_dict[key]
			elif key.lower().strip() == 'font-family':
				if not 'tattribs' in list(styles.keys()):
					styles['tattribs'] = TextAttribs(symbscale=symbscale)
				styles['tattribs'].setFFamily(the_dict['font-family'])
			elif key.lower().strip() == 'font-size':
				if not 'tattribs' in list(styles.keys()):
					styles['tattribs'] = TextAttribs(symbscale=lsscale)
				styles['tattribs'].setFSize(the_dict['font-size'])
			elif key.lower().strip() == 'font-weight':
				if not 'tattribs' in list(styles.keys()):
					styles['tattribs'] = TextAttribs(symbscale=lsscale)
				styles['tattribs'].setFWeight(the_dict['font-weight'])
			elif key.lower().strip() == 'text-anchor':
				if not 'tattribs' in list(styles.keys()):
					styles['tattribs'] = TextAttribs(symbscale=lsscale)
				styles['tattribs'].setTAnchor(the_dict['text-anchor'])							
			elif key.lower().strip() == 'pointer-events':
				styles['pointer-events'] = the_dict
				
		if not sw is None and 'stroke' in list(styles.keys()):
			styles['stroke'].setWidth(sw)

		for a_style in list(styles.values()):
			self.addStyle(style_key, a_style)
			
	def prepareRendering(self):
		defs = self.content.getDefs()
		droot = defs.getRoot()

		#print 'style keys :: ',  self.styles.keys()

		if len(list(self.styles.keys())) > 0:
			s = None
			for element in droot.iter("style"):
				s = element
				break
			if s is None:
				s = etree.SubElement(droot, 'style')
			s.set("type", "text/css")
			od = {}
			for key in list(self.styles.keys()):
				od[key] = {}
				for st in self.styles[key]:
					if isinstance(st, dict):
						od[key].update(st)
					else:
						st.toCSSDict(od[key])
			s.text = etree.CDATA(toCSS(od))
	
	def toBytes(self, inc_declaration=True, inc_doctype=False, pretty_print=True):
		self.prepareRendering()
		if inc_doctype:
			ret = etree.tostring(self.getRoot(), doctype=DOCTYPE_STR, xml_declaration=inc_declaration, pretty_print=pretty_print, encoding='utf-8')
		else:
			ret = etree.tostring(self.getRoot(), xml_declaration=inc_declaration, pretty_print=pretty_print, encoding='utf-8')			
		return ret

	def toString(self, inc_declaration=True, inc_doctype=False, pretty_print=True):
		return self.toBytes(inc_declaration=inc_declaration, inc_doctype=inc_doctype, pretty_print=pretty_print).decode('utf-8')
		
class WorldSVGDoc(SVGDoc):

	SVG_DYN_METHOD_NAMES = [
		"addFilter",
		"addRect",
		"addCircle",
		"addPolygon",
		"addPath",
		"addText",
		"addTextAlongPath",
		"addGroup",
		"addUse",
		"setDims"
	]

	def __init__(self, rootTemplate):
		super().__init__(rootTemplate)		
		self.world = InnerContent(self.content)
		self.world.getRoot().set('class', 'world')
		self.primitive_symbol_names = []
	def setDims(self, dimsObject, scale=1.0):
		self.content.setDims(dimsObject)
		vb = self.content.setIdentityViewbox(scale=scale)
		self.world.setDims(vb)
	def setWorldViewbox(self, viewport):
		self.world.setViewbox(viewport)
	def setExtent(self, extent):
		self.setWorldViewbox(WorldViewport(extent))
	def getPage(self):
		return self.content
	def getWorld(self):
		return self.world	
	def addWorldRect(self, x, y, width, height, attribs=None, idval=None, group=None, ns_stroke=False):
		if not group is None:
			c = self.world.getGroup(group)
		else:
			c = self.world
		return c.addRect(x, y, width, height, attribs=attribs, idval=idval, ns_stroke=ns_stroke)
	def addWorldPath(self, d, attribs=None, idval=None, group=None, ns_stroke=False):
		if not group is None:
			c = self.world.getGroup(group)
		else:
			c = self.world
		return c.addPath(d, attribs=attribs, idval=idval, ns_stroke=ns_stroke)
	def addWorldCircle(self, cx, cy, rad, attribs=None, idval=None, group=None, ns_stroke=False):
		if not group is None:
			c = self.world.getGroup(group)
		else:
			c = self.world
		return c.addCircle(cx, cy, rad, attribs=attribs, idval=idval, ns_stroke=ns_stroke)
	def addWorldUse(self, x, y, refid, attribs=None, idval=None, group=None):
		if not group is None:
			c = self.world.getGroup(group)
		else:
			c = self.world
		return c.addUse(x, y, refid, attribs=attribs, idval=idval)
	def addPrimitiveSymbol(self, name, typestr, params_dict, symbscale=1.0):
		if typestr == "plain_asterisk" and name not in self.primitive_symbol_names:
			rad = float(params_dict['radius']) * symbscale
			wid = float(params_dict['width']) * symbscale
			if rad < 0.1:
				rad = 0.1
			if wid < 0.1:
				wid = 0.1
			rads = '{0:.1f}'.format(rad)
			wids = '{0:.1f}'.format(wid)
			grp = self.addGroup(todefs=True, idval=name, attribs={'fill': 'none', 'stroke-width': wids})
			grp.addPath("M -{0} 0.0 L {0} 0 M 0.0 -{0} L 0.0 {0}".format(rads))
			prjrad = sqrt(rad / 2.0)
			grp.addPath("M -{0} -{0} L {0} {0} M -{0} {0} L {0} -{0}".format(prjrad))
			self.primitive_symbol_names.append(name)
		elif typestr == "plain_square" and name not in self.primitive_symbol_names:
			rad = float(params_dict['radius']) * symbscale
			if rad < 0.1:
				rad = 0.1
			#rads = '{0:.1f}'.format(rad)
			self.addRect(-rad, -rad,2*rad,2*rad, 
					idval=name,
					todefs=True)
			self.primitive_symbol_names.append(name)
		elif typestr == "plain_cross" and name not in self.primitive_symbol_names:
			rad = float(params_dict['radius']) * symbscale
			wid = float(params_dict['width']) * symbscale
			if rad < 0.1:
				rad = 0.1
			if wid < 0.1:
				wid = 0.1
			rads = '{0:.1f}'.format(rad)
			wids = '{0:.1f}'.format(wid)
			self.addPath("M -{0} 0.0 L {0} 0.0 M 0.0 -{0} L 0.0 {0}".format(rads), 
					idval=name, 
					attribs={'fill': 'none', 'stroke-width': wids}, 
					todefs=True)
			self.primitive_symbol_names.append(name)
		elif typestr == "plain_circle" and name not in self.primitive_symbol_names:
			rad = float(params_dict['radius']) * symbscale
			if rad < 0.1:
				rad = 0.1
			rads = '{0:.1f}'.format(rad)
			self.addCircle(0,0, rads, idval=name, todefs=True)
			self.primitive_symbol_names.append(name)
		elif typestr == "inscribed_triangle" and name not in self.primitive_symbol_names:
			rad = float(params_dict['radius']) * symbscale
			if rad < 0.1:
				rad = 0.1
			orient = params_dict['orientation']
			if orient.lower().strip() == 'down':
				ang = 7.0*pi/6.0
				coords = [polar2rect(ang, rad)]
				ang = 11.0*pi/6.0
				coords.append(polar2rect(ang, rad))
				ang = pi/2.0
				coords.append(polar2rect(ang, rad))
			else:
				ang = 1.0*pi/6.0
				coords = [polar2rect(ang, rad)]
				ang = 5.0*pi/6.0
				coords.append(polar2rect(ang, rad))
				ang = 3.0*pi/2.0
				coords.append(polar2rect(ang, rad))
			self.addPolygon(' '.join(coords) , idval=name, todefs=True)
			self.primitive_symbol_names.append(name)
		elif typestr == "location_marker_A" and name not in self.primitive_symbol_names:
			rad = float(params_dict['radius']) * symbscale
			if rad < 0.1:
				rad = 0.1
			dim = 2.0 * rad
			rads = '{0:.1f}'.format(rad)
			#dims = '{0:.1f}'.format(dim)
			grp = self.addGroup(todefs=True, idval=name)
			grp.addCircle(0,-dim, rads)
			grp.addPath("M -{0} -{0} L 0 0 {0} -{0}".format(rads), attribs={'fill': 'none'})
			self.primitive_symbol_names.append(name)
	def addWorldImage(self, x, y, width, height, image_iri, attribs=None, idval=None, group=None, ns_stroke=False):
		if not group is None:
			c = self.world.getGroup(group)
		else:
			c = self.world
		return c.addImage(x, y, width, height, image_iri, attribs=attribs, idval=idval)

class FullDocSVG(SVGDoc):
	def __init__(self, scale=1.0):
		super().__init__(DECLARATION_ROOT)
		self.setDims(DimsFull(), scale=scale)

class BasicDocSVG(SVGDoc):
	def __init__(self, width, height):
		super().__init__(DECLARATION_ROOT)
		self.setDims(Dims(width, height))

class HTMLInsertSVG(SVGDoc):
	def __init__(self, width, height):
		super().__init__(SVG_ROOT)
		self.setDims(Dims(width, height))

class FullDocWorldSVG(WorldSVGDoc):
	def __init__(self, scale=1.0):
		super().__init__(DECLARATION_ROOT)
		self.setDims(DimsFull(), scale=scale)
		
class HTMLInsertWorldSVG(WorldSVGDoc):
	def __init__(self, width, height, x=0, y=0, scale=1.0):
		super().__init__(SVG_ROOT)
		self.setDims(Dims(width, height, x=x, y=y), scale=scale)		
		
# class HTMLInsertMapSVG(HTMLInsertWorldSVG):
# 	def __init__(self, width, height, x=0, y=0):
# 		super(HTMLInsertMapSVG, self).__init__(width, height, x=x, y=y)
		
# 	def finalStr(self):
# 		# Elementos transientes: rectangulo zoom, sketches para efectuar medições, etc.
# 		self.addWorldGroup(idval='worldtransients')
# 		#wtr.addRect(0, 0, 1, 1, idval='zoomrect') 
# 		#wtr.addPath("M 0,0 L 1,1", idval='lengthtoolpath') 
# 		self.addWorldGroup(idval='worldtemporaries')
# 		
# 		return self.toString()
	

if __name__ == "__main__":

	s = SVGRoot(rect=Rect(2,3,100,200))
	#r.transf(s)
	print(etree.tostring(s.tree.getroot()))

