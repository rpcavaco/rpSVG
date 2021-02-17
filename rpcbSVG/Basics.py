
from collections import namedtuple

from typing import List, Optional, Union

from math import atan, cos, sin, radians, degrees

Pt = namedtuple("Pt", "x y")

XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"

MAXCOORD = 99999999999.9
MINCOORD = -MAXCOORD
MINDELTA = 0.001
NANODELTA = 0.000001

DONTYINVERT_CHILDREN = ["symbol"]

class ValueWithUnitsError(RuntimeError):
	def __init__(self, p_val) -> None:
		super().__init__()
		self.val = p_val
	def __str__(self):
		return f"no units allowed here, found: {self.val}"

class UnknownUnitsError(RuntimeError):
	def __init__(self, p_unitsstr) -> None:
		super().__init__()
		self.unitsstr = p_unitsstr
	def __str__(self):
		return f"unknown units: {self.unitsstr}"

GLOBAL_ENV = {
	"ROUND": {
		"flag": True,
		"places": 4
	}
}


def removeDecsep(p_val):
	r = int(p_val)
	if r == p_val:
		ret = r
	else:
		ret = p_val
	return ret

def glRd(p_val):
	if GLOBAL_ENV["ROUND"]["flag"]:
		return removeDecsep(round(p_val, GLOBAL_ENV["ROUND"]["places"]))
	else:
		return removeDecsep(p_val)
	 
def ptCoincidence(pa: Pt, pb: Pt, mindelta=MINDELTA):
	return abs(pa.x - pb.x) < mindelta and abs(pa.y - pb.y)  < mindelta

def ptAdd(pa: Pt, pb: Pt):
	return Pt(pa.x + pb.x, pa.y + pb.y)

def ptRemoveDecsep(p_x, p_y):
	return Pt(removeDecsep(p_x), removeDecsep(p_y))

def toNumberAndUnit(p_val):
	base = str(p_val)
	numchars = []
	unitchars = []
	for c in base:
		if str.isdigit(c) or c in ('.', ',', '-'):
			numchars.append(c)
		else:
			unitchars.append(c)
	if len(unitchars) > 0:
		un = ''.join(unitchars)
	else:
		un = None
	return removeDecsep(float(''.join(numchars))), un

def fromNumberAndUnit(p_val, p_unit):
	return f"{removeDecsep(p_val)}{p_unit}"

def strictToNumber(p_val):
	base = str(p_val)
	numchars = []
	for c in base:
		if str.isdigit(c) or c in ('.', ',', '-'):
			numchars.append(c)
		else:
			raise ValueWithUnitsError(p_val)
	return removeDecsep(float(''.join(numchars)))

def add(a, b):
	return strictToNumber(a) + strictToNumber(b)

def subtr(a, b):
	return strictToNumber(a) - strictToNumber(b)

def getUnit(p_val):
	base = str(p_val)
	unitchars = []
	for c in base:
		if not str.isdigit(c) and not c in ('.', ',', '-'):
			unitchars.append(c)
	if len(unitchars) > 0:
		un = ''.join(unitchars)
	else:
		un = None
	return un

# def fromNumberAndUnit(p_num, p_unit):
# 	if p_unit is None:
# 		ret = str(removeDecsep(p_num))
# 	else:
# 		ret = f"{p_num}{p_unit}"
# 	return ret

def ptEnsureStrings(p_pt: Pt):
	ret = Pt(None, None)
	if hasattr(p_pt, 'x'):
		v_x = p_pt.x
	else:
		v_x = p_pt[0]
	if hasattr(p_pt, 'y'):
		v_y = p_pt.y
	else:
		v_y = p_pt[1]
	if not isinstance(v_x, str):
		ret = ret._replace(x=str(removeDecsep(v_x)))
	else:
		ret = ret._replace(x=v_x)
	if not isinstance(v_y, str):
		ret = ret._replace(y=str(removeDecsep(v_y)))
	else:
		ret = ret._replace(y=v_y)
	return ret

def ptGetAngle(p_pt1: Pt, p_pt2: Pt):
	ret = None
	dx = float(p_pt2.x) - float(p_pt1.x)
	dy = float(p_pt2.y) - float(p_pt1.y)
	adx = abs(dx)
	ady = abs(dy)
	if adx < MINDELTA:
		if dy > MINDELTA:
			ret = 90
		if dy < MINDELTA:
			ret = 270
	elif ady < MINDELTA:
		if dx > MINDELTA:
			ret = 0
		if dx < MINDELTA:
			ret = 180
	else:
		ret = degrees(atan(ady/adx))
	if dx < 0:
		if dy > 0:
			ret = 180 - ret
		elif dy < 0:
			ret = 180 + ret
	elif dx > 0:
		if dy < 0:
			ret = - ret


	return ret

def polar2rectDegs(ang, rad):
	ret = Pt(glRd(cos(radians(ang)) * rad), glRd(sin(radians(ang)) * rad))
	return ret

def polar2rect(ang, rad):
	return Pt(cos(ang) * rad, sin(ang) * rad)

def calc3rdPointInSegment(p_pt1: Pt, p_pt2: Pt, radiusFromP1: Union[float, int]):
	ang = ptGetAngle(p_pt1, p_pt2)
	return polar2rectDegs(ang, radiusFromP1)

def isNumeric(p_val):
	try:
		float(p_val)
		ret = True
	except ValueError:
		ret = False
	return ret

def circleDividers(p_center: Pt, p_radius: Union[float, int], p_n: int, p_rot_left: Optional[Union[float, int]] = 0):
	"""Generate p_n points equally dividing a circle defined by:
		- p_center - a point
		- p_radius - radius from center
		- p_rot_left - (degrees) angle on trigonometric circle"""
	step = 360 / p_n
	for i in range(p_n):
		ang = i * step + p_rot_left
		yield ptRemoveDecsep(*ptAdd(p_center, polar2rectDegs(ang, p_radius)))

def url_href(p_text):
	if not p_text.startswith('url'):
		if not p_text.startswith('#'):
			v_text = f"url(#{p_text})"
		else:
			v_text = f"url({p_text})"
	else:
		v_text = p_text
	return v_text

def hashed_href(p_text):
	if not p_text.startswith('#'):
		v_text = f"#{p_text}"
	else:
		v_text = p_text
	return v_text

def unitValueToVPUnits(p_val, units=None, emModifier=1):
	ret = None
	val = emModifier * strictToNumber(p_val)
	if units is None or units == "px":
		ret = val
	elif units == 'pt':
		ret = val * 1.25
	elif units == 'pc':
		ret = val * 15
	elif units == 'mm':
		ret = val * 3.543307
	elif units == 'cm':
		ret = val * 35.43307
	elif units == 'in':
		ret = val * 90
	else:
		UnknownUnitsError(units)
	return ret

def fontSizeToVPUnits(fontsize=None, possibleEmModifier=None):
	assert not fontsize is None or not possibleEmModifier is None
	ret = None
	if not fontsize is None:
		fsz, ufsz = toNumberAndUnit(fontsize)
	else:
		ufsz = fsz = None
	emm = 1.0
	if not possibleEmModifier is None:
		_emm, uemm = toNumberAndUnit(possibleEmModifier)
		if uemm == "em":
			emm = _emm
		else:
			ret = unitValueToVPUnits(_emm, units=uemm)
	if ret is None:
		ret = unitValueToVPUnits(fsz, units=ufsz, emModifier=emm)
	return ret

class WrongValueTransformDef(RuntimeError):
	def __init__(self, p_class_instance, p_attr):
		self.classname = p_class_instance.__class__.__name__
		self.attr = p_attr
	def __str__(self):
		return f"Transform definition '{self.classname}' accepts no '{self.attr}' value"

class WrongValuePathCmd(RuntimeError):
	def __init__(self, p_class_instance, p_attr):
		self.classname = p_class_instance.__class__.__name__
		self.attr = p_attr
	def __str__(self):
		return f"Path command '{self.classname}' accepts no '{self.attr}' value"

class _attrs_struct(object):
	
	_fields = None # Required -- list to be extended in subclasses
	_subfields = [] # Optional -- list to be extended in subclasses
	
	def __init__(self, *args, defaults=None) -> None:
		self._unusedattrs = []
		self.setall(*args, defaults=defaults) 

	def getfields(self):
		return ",".join(self._fields)

	def setall(self, *args, defaults=None) -> None:
		used_fldindexes = set()
		lf = len(self._fields)
		la = len(args)
		for i, fld in enumerate(self._fields):
			if i < la:
				val = args[i]
				if not val is None:
					setattr(self, fld, str(val))
					used_fldindexes.add(i)
			else:
				revi = lf - i - 1
				if not defaults is None:
					if len(defaults) > revi:
						val = str(defaults[revi])
					else:
						val = str(defaults[-1])
					setattr(self, fld, val)
		if len(self._subfields) > 0:
			if len(self._subfields) == la - lf:
				for j, sfld in enumerate(self._subfields):
					idx = j + lf
					setattr(self, sfld, str(args[idx]))
					used_fldindexes.add(idx)
		l = len(used_fldindexes)
		if l > 0 and l < la:
			for idx in range(l, la):
				self._unusedattrs.append(args[idx])
		return self

	def getall(self) -> List:
		ret = []
		for fld in self._fields:
			ret.append(self.get(fld))
		return ret

	def getUnusedAttrs(self):
		return self._unusedattrs

	def has(self, p_attr: str):
		return p_attr in self._fields

	def hasHREF(self):
		ret = False
		for f in self._fields:
			if f.endswith("href"):
				ret = True
				break
		return ret

	def get(self, p_attr: str):
		ret = None
		if self.has(p_attr) and hasattr(self, p_attr):
			ret = getattr(self, p_attr)
		return ret

	def set(self, p_attr: str, p_value):
		if self.has(p_attr):
			setattr(self, p_attr, str(p_value))
		return self

	def setHREF(self, p_value):
		for f in self._fields:
			if f.endswith("href"):
				setattr(self, f, str(p_value))
				break
		return self

	def getNumeric(self, p_attr: str) -> float:
		ret = None
		if self.has(p_attr) and hasattr(self, p_attr):
			ret, _u = toNumberAndUnit(getattr(self, p_attr))
		return ret

	def __repr__(self):
		out = [self.__class__.__name__]
		for x in self.__dict__.keys():
			if x in self._fields:
				out.append(f"{x}={getattr(self, x)}")
		return ' '.join(out)

	# def toJSON(self):
	# 	out = {}
	# 	for x in self.__dict__.keys():
	# 		if x in self._fields:
	# 			out[x] = getattr(self, x)
	# 	return out

	def sharedItems(self, o: object) -> dict:
		return {f: getattr(self,f) for f in self._fields if f in dir(o) and hasattr(self,f) and getattr(self,f) == getattr(o,f)}

	def equality(self, o: object) -> bool:
		l = len([f for f in self._fields if hasattr(self, f) and not getattr(self, f) is None])
		return len(self.sharedItems(o)) == l

	def __eq__(self, o: object) -> bool:
		return self.equality(o)

	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)

	def setXmlAttrs(self, xmlel) -> None:  
		assert not xmlel is None
		for f in self._fields:
			if hasattr(self, f):
				val = getattr(self, f)
				if not val is None:
					assert not val == "None"
					xmlel.set(f, str(val))
		return self

	def getFromXmlAttrs(self, xmlel) -> None:  
		assert not xmlel is None
		for f in self._fields:
			if f in xmlel.keys():
				val = xmlel.get(f)
				if not val is None:
					setattr(self, f, xmlel.get(f))
		return self

	def cloneFrom(self, p_other):
		for l in [self._fields, self._subfields]:
			for fld in l:
				if hasattr(p_other, fld):
					setattr(self, fld, getattr(p_other, fld))
		return self

class _withunits_struct(_attrs_struct):

	def __init__(self, *args, defaults=None) -> None:
		self._units = None
		self._maxattrnum_to_applyunits = 4
		self._strictparsing = True # False enables non-strict parsing of additional attribs, stops rasing exception for non-units attributes
		if not "_units" in self._subfields:
			self._subfields.append("_units")
		super().__init__(*args, defaults=defaults)
		if not self._units is None:
			self._apply_units()

	def __eq__(self, o: object) -> bool:
		ret = False
		if self._units == o.getUnits():
			ret = self.equality(o)
			#ret = len(self.sharedItems(o)) == len(self._fields)
		return ret

	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)

	def _apply_units(self) -> None:
		assert not self._units is None
		if self._strictparsing:
			assert self._units in ('px', 'pt', 'em', 'rem', '%'), f"invalid units: '{self._units}' not in 'px', 'pt', 'em', 'rem' or '%'"
		if self._units in ('px', 'pt', 'em', 'rem', '%'):
			for fi, f in enumerate(self._fields):
				if fi >= self._maxattrnum_to_applyunits:
					break
				if not hasattr(self, f):
					continue
				val = getattr(self, f)
				numval = None
				try:
					numval = int(val)
				except ValueError:
					try:
						numval = float(val)
					except ValueError:
						pass
				if not numval is None and numval > 0:
					setattr(self, f, f"{numval}{self._units}")
		else:
			self._unusedattrs.append(self._units)
			self._units = None

	def getUnits(self) -> str:
		return self._units

	def setUnits(self, un: str) -> None:
		self._units = un
		self._apply_units()

	def iterUnitsRemoved(self):
		for f in self._fields:
			if not hasattr(self, f):
				continue
			val = getattr(self, f)
			if not self._units is None:
				val = val.replace(self._units, '')
			yield val

	def iterUnitsRemovedNum(self):
		for val in self.iterUnitsRemoved():
			yield removeDecsep(float(val))

class _kwarg_attrs_struct(object):
	
	_fields = None # Required -- list to be extended in subclasses
	_funciris = None
	
	def __init__(self, **kwargs) -> None:
		for f in self._fields:
			safekey = f.replace('-', '_')
			if safekey in kwargs.keys():
				if not kwargs[safekey] is None:
					preval = kwargs[safekey]
					if f in self._funciris and preval != 'inherit':
						val = f"url(#{preval})"
					else:
						val = preval
					setattr(self, f, val)

	def __repr__(self):
		out = [self.__class__.__name__]
		for x in self.__dict__.keys():
			if x in self._fields:
				out.append(f"{x}={getattr(self, x)}")
		return ' '.join(out)

	def setXmlAttrs(self, xmlel) -> None:  
		assert not xmlel is None
		for f in self._fields:
			if hasattr(self, f):
				val = getattr(self, f)
				if not val is None:
					assert not val == "None"
					xmlel.set(f, str(val))
		return self


class Env(_attrs_struct):
	_fields = ("minx",  "miny", "maxx", "maxy") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])
	def defFromPointList(self, p_ptlist):
		minx = MAXCOORD
		miny = MAXCOORD
		maxx = MINCOORD
		maxy = MINCOORD
		changed = False
		for pt in p_ptlist:
			changed = True
			vx = strictToNumber(pt.x)
			if vx < minx:
				minx = vx
			vy = strictToNumber(pt.y)
			if vy < miny:
				miny = vy
			if vx > maxx:
				maxx = vx
			if vy > maxy:
				maxy = vy
		if changed:
			self.minx = minx
			self.miny = miny
			self.maxx = maxx
			self.maxy = maxy
	def getWidth(self):
		a = strictToNumber(self.maxx)
		b = strictToNumber(self.minx)
		return a - b
	def getHeight(self):
		a = strictToNumber(self.maxy)
		b = strictToNumber(self.miny)
		return a - b
	def getMidPt(self) -> Pt:
		a = strictToNumber(self.minx)
		b = strictToNumber(self.miny)
		return Pt(a + (self.getWidth() / 2.0),
					b + (self.getHeight() / 2.0))
	def getRectParams(self):
		outlist = []
		outlist.append(self.minx)
		outlist.append(self.miny)
		outlist.append(self.getWidth())
		outlist.append(self.getHeight())
		return outlist
	def cloneFromOther(self, other):
		self.minx = other.minx
		self.miny = other.miny
		self.maxx = other.maxx
		self.maxy = other.maxy
		return self
	def centerAndDims(self, cntPt, dimx, dimy):
		self.minx = removeDecsep(strictToNumber(cntPt.x) - dimx/2.0)
		self.miny = removeDecsep(strictToNumber(cntPt.y) - dimy/2.0)
		self.maxx = removeDecsep(strictToNumber(cntPt.x) + dimx/2.0)
		self.maxy = removeDecsep(strictToNumber(cntPt.y) + dimy/2.0)
		return self
	def expandFromOther(self, other):
		a = strictToNumber(self.minx)
		b = strictToNumber(self.miny)
		c = strictToNumber(self.maxx)
		d = strictToNumber(self.maxy)
		e = strictToNumber(other.minx)
		f = strictToNumber(other.miny)
		g = strictToNumber(other.maxx)
		h = strictToNumber(other.maxy)
		if e < a:
			self.minx = e
		if f < b:
			self.miny = f
		if g > c:
			self.maxx = g
		if h > d:
			self.maxy = h
		return self
	def expandFromPoint(self, pt):
		a = strictToNumber(self.minx)
		b = strictToNumber(self.miny)
		c = strictToNumber(self.maxx)
		d = strictToNumber(self.maxy)
		if pt.x < a:
			self.minx = pt.x
		if pt.y < b:
			self.miny = pt.y
		if pt.x > c:
			self.maxx = pt.x
		if pt.y > d:
			self.maxy = pt.y
		return self
	def expand(self, ratio):
		pt = self.getMidPt()
		newhwidth = self.getWidth() * ratio * 0.5
		newhheight = self.getHeight() * ratio * 0.5
		self.minx = pt.x - newhwidth 
		self.miny = pt.y - newhheight 
		self.maxx = pt.x + newhwidth 
		self.maxy = pt.y + newhheight 	
		return self
	def invertY(self):
		tmp = self.maxy
		self.maxy = self.miny
		self.miny = tmp

# transforms

class transform_def(_attrs_struct):
	_fields = ()
	_optfields = ()
	_label = ""
	def getFromXmlAttrs(self, xmlel) -> None:  
		raise NotImplementedError("transform attribs not to be translated to xml attribs")
	def setXmlAttrs(self, xmlel) -> None:  
		raise NotImplementedError("transform attribs not to be translated to xml attribs")
	def validate(self):
		for f in self._fields:
			if not hasattr(self, f) and f not in self._optfields:
				raise TypeError(f"{self._label}, required value '{f}' not provided")
		return self
	def get(self):
		return f"{self._label}({','.join([getattr(self, f) for f in self._fields if hasattr(self, f)])})"
	def getvalue(self, p_field: str):
		ret = None
		if p_field in self._fields and hasattr(self, p_field):
			ret = getattr(self, p_field)
		return ret
	def setvalue(self, p_field: str, p_value):
		if p_field not in self._fields:
			raise WrongValueTransformDef(self, p_field)
		setattr(self, p_field, str(p_value))
		return self

class Mat(transform_def):
	_fields = ("a", "b", "c", "d", "e", "f")
	_label = "matrix"
	def __init__(self, *args) -> None:
		super().__init__(*args)
		self.validate()

class Trans(transform_def):
	_fields = ("tx", "ty")
	_optfields = ("ty",)
	_label = "translate"
	def __init__(self, *args) -> None:
		super().__init__(*args)
		self.validate()
	def yinvert(self, p_yheight):
		if hasattr(self, "ty"):
			setattr(self, "ty", str(p_yheight - strictToNumber(getattr(self, "ty"))))

class Scale(transform_def):
	_fields = ("sx", "sy")
	_optfields = ("sy",)
	_label = "scale"
	def __init__(self, *args) -> None:
		super().__init__(*args)
		self.validate()

class Rotate(transform_def):
	_fields = ("rotate-angle", "cx", "cy")
	_optfields = ("cx", "cy")
	_label = "rotate"
	def __init__(self, *args) -> None:
		super().__init__(*args)
		self.validate()

class SkewX(transform_def):
	_fields = ("skew-angle",)
	_label = "skewX"
	def __init__(self, *args) -> None:
		super().__init__(*args)
		self.validate()

class SkewY(transform_def):
	_fields = ("skew-angle",)
	_label = "skewY"
	def __init__(self, *args) -> None:
		super().__init__(*args)
		self.validate()

# Path commands

class path_command(_attrs_struct):
	_fields = ()
	_letter = ""
	#_y_valinverts = ()
	_y_signinverts = ()
	
	def __init__(self, *args) -> None:
		arglist = [glRd(arg) for arg in args]
		super().__init__(*arglist, defaults=None)
		self.letter = self._letter
		self.validate()
	def getLetter(self):
		return self.letter
	# def eqLetter(self, o) -> bool:
	# 	print("\n self:", self.getLetter(), ", other:", o.getLetter())
	# 	return self.getLetter() == o.getLetter()
	def getFromXmlAttrs(self, xmlel) -> None:  
		raise NotImplementedError("transform attribs not to translated to xml attribs")
	def setXmlAttrs(self, xmlel) -> None:  
		raise NotImplementedError("transform attribs not to translated to xml attribs")
	def validate(self):
		for f in self._fields:
			if not hasattr(self, f):
				raise TypeError(f"{self.letter}, required value '{f}' not provided")
		return self
	def get(self, omitletter: Optional[bool] = False):
		buf = []
		first_is_positive = False
		vals = [getattr(self, f) for f in self._fields]
		for i, v in enumerate(vals):
			if i == 0:
				buf.append(v)
				if float(v) >= 0:
					first_is_positive = True
			else:
				if float(v) >= 0:
					buf.append(' ')
				buf.append(v)
		if omitletter:
			if first_is_positive:
				ret = f" {''.join(buf)}"
			else:
				ret = ''.join(buf)
		else:
			ret = f"{self.letter}{''.join(buf)}"
		return ret
	def getvalue(self, p_field: str):
		ret = None
		if p_field in self._fields and hasattr(self, p_field):
			ret = getattr(self, p_field)
		return ret
	def setvalue(self, p_field: str, p_value):
		if p_field not in self._fields:
			raise WrongValuePathCmd(self, p_field)
		setattr(self, p_field, str(p_value))
		return self
	# def yinvert(self, p_yheight):
	# 	for f in self._y_valinverts:
	# 		self.setvalue(f, strictToNumber(self.getvalue(f)))

class rel_path_command(path_command):
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args)
		self.setRelative(relative)
		self.validate()
	def setRelative(self, is_relative: bool):
		self.relative = is_relative
		if self.relative:
			self.letter = self._letter.lower()
		else:
			self.letter = self._letter.upper()
	def isRelative(self):
		return self.relative

class pM(rel_path_command):
	"Move to"
	_fields = ("x", "y")
	_letter = "M"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		if hasattr(self, "y"):
			setattr(self, "y", str(p_yheight - strictToNumber(getattr(self, "y"))))
	
class pL(rel_path_command):
	"Line to"
	_fields = ("x", "y")
	_letter = "L"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		if hasattr(self, "y"):
			setattr(self, "y", str(p_yheight - strictToNumber(getattr(self, "y"))))

class pH(rel_path_command):
	"Horizontal line to"
	_fields = ("x")
	_letter = "H"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)

class pV(rel_path_command):
	"Vertical line to"
	_fields = ("y")
	_letter = "V"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		if hasattr(self, "y"):
			setattr(self, "y", str(p_yheight - strictToNumber(getattr(self, "y"))))

class pC(rel_path_command):
	"Cubic Bézier"
	_fields = ("x1", "y1", "x2", "y2", "x", "y")
	_letter = "C"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		for fld in ("y1", "y2", "y"):
			if hasattr(self, fld):
				setattr(self, fld, str(p_yheight - strictToNumber(getattr(self, fld))))

class pS(rel_path_command):
	"Shorthand cubic Bézier"
	_fields = ("x2", "y2", "x", "y")
	_letter = "S"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		for fld in ("y2", "y"):
			if hasattr(self, fld):
				setattr(self, fld, str(p_yheight - strictToNumber(getattr(self, fld))))

class pQ(rel_path_command):
	"Quadratic Bézier"
	_fields = ("x1", "y1", "x", "y")
	_letter = "Q"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		for fld in ("y1", "y"):
			if hasattr(self, fld):
				setattr(self, fld, str(p_yheight - strictToNumber(getattr(self, fld))))

class pT(rel_path_command):
	"Shorthand quadratic Bézier"
	_fields = ("x", "y")
	_letter = "T"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		if hasattr(self, "y"):
			setattr(self, "y", str(p_yheight - strictToNumber(getattr(self, "y"))))

class pA(rel_path_command):
	"Eliptical arc"
	_fields = ("rx", "ry", "x-axis-rotation", "large-arc-flag", "sweep-flag", "x", "y")
	_letter = "A"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)
	def yinvert(self, p_yheight):
		if hasattr(self, "y"):
			setattr(self, "y", str(p_yheight - strictToNumber(getattr(self, "y"))))

class pClose(path_command):
	_fields = ()
	_letter = "z"
	def __init__(self, *args) -> None:
		super().__init__(*args)

