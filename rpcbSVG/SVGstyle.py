#import json

from typing import Optional, Union

STYLE_ATTRIBS = set([ 
	'font', 
	'font-family',
	'font-size',
	'font-size-adjust',
	'font-stretch',
	'font-style',
	'font-variant',
	'font-weight',
	'direction',
	'letter-spacing',
	'text-decoration',
	'unicode-bidi',
	'word-spacing',
	'clip', 
	'color',
	'cursor',
	'display',
	'overflow', 
	'visibility',
	'clip-path',
	'clip-rule',
	'mask',
	'opacity',
	'enable-background',
	'filter',
	'flood-color',
	'flood-opacity',
	'lighting-color',
	'stop-color',
	'stop-opacity',
	'pointer-events',
	'color-interpolation',
	'color-interpolation-filters',
	'color-profile',
	'color-rendering',
	'fill',
	'fill-opacity',
	'fill-rule',
	'image-rendering',
	'marker',
	'marker-end',
	'marker-mid',
	'marker-start',
	'shape-rendering',
	'stroke',
	'stroke-dasharray',
	'stroke-dashoffset',
	'stroke-linecap',
	'stroke-linejoin',
	'stroke-miterlimit',
	'stroke-opacity',
	'stroke-width',
	'text-rendering',
	'alignment-baseline',
	'baseline-shift',
	'dominant-baseline',
	'glyph-orientation-horizontal',
	'glyph-orientation-vertical',
	'kerning',
	'text-anchor',
	'writing-mode'
])

class NestedDictError(RuntimeError):
	def __str__(self):
		return "no nested dicts allowed in addFromDict method in this class"


def toCSSRule(indict, outbuf, depth=-1):
	dp = depth + 1
	indent = '\t' * dp
	for k in list(indict.keys()):
		if isinstance(indict[k], dict):
			outbuf.append('{0}{1} {{'.format(indent, k))
			toCSSRule(indict[k], outbuf, depth=dp)
			outbuf.append('{0}}}'.format(indent))
		else:
			outbuf.append('{0}{1}: {2};'.format(indent, k, indict[k]))

class Sty(object):

	def __init__(self, *args) -> None:
		self.add(args)

	def getStyleAttrs(self):
		return [attr for attr in dir(self) if not attr.startswith('__') and attr in STYLE_ATTRIBS]

	def diffDict(self, o: object) -> dict:
		ret = {}
		if not hasattr(o, 'selector'):
			attrs = self.getStyleAttrs()
			oattrs = o.getStyleAttrs()
			if set(attrs) == set(oattrs):
				for attr in attrs:
					a = getattr(self, attr)
					b = getattr(o, attr)
					if a != b:
						ret[attr] = (a, b)
			else:
				ret = { "attrs": (attrs, oattrs)  }
		else:
			ret = { "selector": (None, o.selector)  }
		return ret

	def __eq__(self, o: object) -> bool:
		dd = self.diffDict(o)
		return len(dd) == 0

	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)

	def toString(self, prefix=None):
		if not prefix is None:
			out = [prefix]
		else:
			out = []
		for x in self.getStyleAttrs():
			out.append(f"{x}={getattr(self, x)}")
		return ' '.join(out)

	def __repr__(self):
		return self.toString()

	def add(self, *args):
		alist = tuple(*args)
		for ix, val in enumerate(zip(alist, alist[1:])):
			if ix % 2 == 1:
				continue
			attrib, value = val
			if attrib in STYLE_ATTRIBS:
				setattr(self, attrib, str(value))
		if not hasattr(self, 'fill'):
			setattr(self, 'fill', 'none')
		return self

	def set(self, attrib: str, value):
		if attrib in STYLE_ATTRIBS:
			setattr(self, attrib, str(value))

	def addFromDict(self, in_dict):
		ld = len(in_dict)
		usable_dict = None
		if ld == 1:
			tentative_selector = list(in_dict.keys())[0]
			if not tentative_selector in STYLE_ATTRIBS and isinstance(in_dict[tentative_selector], dict):
				raise NestedDictError()
			else:
				usable_dict = in_dict
		elif ld > 0:
			if isinstance(in_dict, dict):
				usable_dict = in_dict

		assert usable_dict is not None, f"no usable dict from {in_dict}"
				
		if ld > 0:
			if isinstance(usable_dict, dict):
				isec = set(usable_dict.keys()).intersection(STYLE_ATTRIBS)
				if len (isec) > 0:
					for sa in isec:
						setattr(self, sa, usable_dict[sa])

		return self

	def toDict(self) -> dict:
		ret = {}
		for f in self.getStyleAttrs():
			ret[f] = str(getattr(self, f))
		return ret

	def setXmlAttrs(self, xmlel) -> None:  
		for f in self.getStyleAttrs():
			if hasattr(self, f):
				xmlel.set(f, str(getattr(self, f)))
		return self

	def fromXmlAttrs(self, xmlel):
		for attr in xmlel.keys():
			if attr in STYLE_ATTRIBS:
				setattr(self, attr, xmlel.get(attr))
		return self


class CSSSty(Sty):

	def __init__(self, *args, selector) -> None:
		if selector is None:
			raise TypeError("CSSSty() needs keyword-only argument 'selector'")
		self.selector = selector
		super().__init__(*args)

	def setSelector(self, p_selector):
		self.selector = p_selector
		return self

	def getSelector(self):
		return self.selector

	def diffDict(self, o: object, exclude_selector: Optional[bool] = False) -> dict:
		ret = {}
		if exclude_selector or self.selector == o.selector:
			attrs = self.getStyleAttrs()
			oattrs = o.getStyleAttrs()
			if set(attrs) == set(oattrs):
				for attr in attrs:
					a = getattr(self, attr)
					b = getattr(o, attr)
					if a != b:
						ret[attr] = (a, b)
			else:
				ret = { "attrs": (attrs, oattrs)  }
		else:
			ret = { "selector": (self.selector, o.selector)  }
		return ret

	def isSimilarTo(self, o: object) -> bool:
		dd = self.diffDict(o, exclude_selector=True)
		return len(dd) == 0

	def __repr__(self):
		return self.toString(prefix=f"sel={str(self.selector)}")

	def addFromDict(self, in_dict):
		ld = len(in_dict)
		usable_dict = None
		if ld == 1:
			tentative_selector = list(in_dict.keys())[0]
			if not tentative_selector in STYLE_ATTRIBS and isinstance(in_dict[tentative_selector], dict):
				self.selector = tentative_selector
				usable_dict = in_dict[tentative_selector]
			else:
				usable_dict = in_dict
		elif ld > 0:
			if isinstance(in_dict, dict):
				usable_dict = in_dict

		assert usable_dict is not None, f"no usable dict from {in_dict}"
				
		if ld > 0:
			if isinstance(usable_dict, dict):
				isec = set(usable_dict.keys()).intersection(STYLE_ATTRIBS)
				if len (isec) > 0:
					for sa in isec:
						setattr(self, sa, usable_dict[sa])

		return self

	def copyFromSty(self, sty: Sty, selector: Optional[str] = None):
		if not selector is None:
			self.setSelector(selector)
		self.addFromDict(sty.toDict())
		return self

	def toCSSRule(self, outbuf, depth=-1):
		attrs = self.getStyleAttrs()
		if self.selector is None:
			the_dict = {attr: getattr(self, attr) for attr in attrs}
		else:
			the_dict = {self.selector: {attr: getattr(self, attr) for attr in attrs}}
		toCSSRule(the_dict, outbuf,  depth=-1)
		return self

	def toCSSString(self, depth=-1):
		outbuf = []		
		self.toCSSRule(outbuf, depth=depth)
		return '\n'.join(outbuf)


