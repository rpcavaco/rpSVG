
from collections import namedtuple

from typing import Optional

Pt = namedtuple("Pt", "x y")

MAXCOORD = 99999999999.9
MINCOORD = -MAXCOORD
MINDELTA = 0.001
NANODELTA = 0.000001

def ptCoincidence(pa: Pt, pb: Pt, mindelta=MINDELTA):
	return abs(pa.x - pb.x) < mindelta and abs(pa.y - pb.y)  < mindelta

def removeDecsep(p_val):
	r = round(p_val)
	if r == p_val:
		ret = r
	else:
		ret = p_val
	return ret

def ptEnsureStrings(p_pt: Pt):
	ret = Pt(None, None)
	if not isinstance(p_pt.x, str):
		ret = ret._replace(x=str(removeDecsep(p_pt.x)))
	else:
		ret = ret._replace(x=p_pt.x)
	if not isinstance(p_pt.y, str):
		ret = ret._replace(y=str(removeDecsep(p_pt.y)))
	else:
		ret = ret._replace(y=p_pt.y)
	return ret

#def polar2rect(ang, rad):
#	return POINTS_FORMAT.format(cos(ang) * rad, sin(ang) * rad )

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


# def ptList2AbsPolylinePath(p_ptlist, mirrory=False, close=False):
# 	strcomps = []
# 	for pi, pt in enumerate(p_ptlist):
# 		if mirrory:
# 			pt.y = -pt.y
# 		if pi == 0:
# 			strcomps.append("M{0:.4f} {1:.4f}".format(*pt))
# 		elif pi == 1:
# 			strcomps.append("L{0:.4f} {1:.4f}".format(*pt))
# 		else:
# 			strcomps.append(" {0:.4f} {1:.4f}".format(*pt))
# 	if close:
# 		strcomps.append(" z")
# 	return "".join(strcomps)	

class _attrs_struct(object):
	
	_fields = None # Required -- list to be extended in subclasses
	_subfields = [] # Optional -- list to be extended in subclasses
	
	def __init__(self, *args, defaults=None) -> None:
		self.setall(*args, defaults=defaults) 

	def setall(self, *args, defaults=None) -> None:
		for i, fld in enumerate(self._fields):
			if i < len(args):
				val = args[i]
				if not val is None:
					setattr(self, fld, str(val))
			else:
				revi = len(self._fields) - i - 1
				if not defaults is None:
					if len(defaults) > revi:
						val = str(defaults[revi])
					else:
						val = str(defaults[-1])
					setattr(self, fld, val)
		if len(self._subfields) > 0:
			if len(self._subfields) == len(args) - len(self._fields):
				for j, sfld in enumerate(self._subfields):
					idx = j + len(self._fields)
					setattr(self, sfld, str(args[idx]))
		return self

	def has(self, p_attr: str):
		return p_attr in self._fields

	def get(self, p_attr: str):
		ret = None
		if self.has(p_attr) and hasattr(self, p_attr):
			ret = getattr(self, p_attr)
		return ret

	def set(self, p_attr: str, p_value):
		if self.has(p_attr):
			setattr(self, p_attr, str(p_value))

	def getNumeric(self, p_attr: str) -> float:
		ret = None
		if self.has(p_attr) and hasattr(self, p_attr):
			val = getattr(self, p_attr)
			ret = float(val)
		return ret

	def __repr__(self):
		out = []
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
		for f in self._fields:
			if hasattr(self, f):
				val = getattr(self, f)
				if not val is None:
					assert not val == "None"
					xmlel.set(f, str(val))
		return self

	def getFromXmlAttrs(self, xmlel) -> None:  
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
		assert self._units in ('px', 'pt', 'em', 'rem', '%'), f"invalid units: '{self._units}' not in 'px', 'pt', 'em', 'rem' or '%'"
		for f in self._fields:
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

	def getNumeric(self, p_attr: str) -> float:
		ret = None
		if self.has(p_attr) and hasattr(self, p_attr):
			val = getattr(self, p_attr)
			if not self._units is None:
				val = val.replace(self._units, '')
			ret = float(val)
		return ret

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
			if pt.x < minx:
				minx = pt.x
			if pt.y < miny:
				miny = pt.y
			if pt.x > maxx:
				maxx = pt.x
			if pt.y > maxy:
				maxy = pt.y
		if changed:
			self.minx = minx
			self.miny = miny
			self.maxx = maxx
			self.maxy = maxy
	def getWidth(self):
		return float(self.maxx) - float(self.minx)
	def getHeight(self):
		return float(self.maxy) - float(self.miny)
	def getMidPt(self) -> Pt:
		return Pt(self.minx + (self.getWidth() / 2.0),
					self.miny + (self.getHeight() / 2.0))
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
		self.minx = cntPt.x - dimx/2.0
		self.miny = cntPt.y - dimy/2.0
		self.maxx = cntPt.x + dimx/2.0
		self.maxy = cntPt.y + dimy/2.0
		return self
	def expandFromOther(self, other):
		if other.minx < self.minx:
			self.minx = other.minx
		if other.miny < self.miny:
			self.miny = other.miny
		if other.maxx > self.maxx:
			self.maxx = other.maxx
		if other.maxy > self.maxy:
			self.maxy = other.maxy
		return self
	def expandFromPoint(self, pt):
		if pt.x < self.minx:
			self.minx = pt.x
		if pt.y < self.miny:
			self.miny = pt.y
		if pt.x > self.maxx:
			self.maxx = pt.x
		if pt.y > self.maxy:
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

# transforms

class transform_def(_attrs_struct):
	_fields = ()
	_optfields = ()
	_label = ""
	def getFromXmlAttrs(self, xmlel) -> None:  
		raise NotImplementedError("transform attribs not to translated to xml attribs")
	def setXmlAttrs(self, xmlel) -> None:  
		raise NotImplementedError("transform attribs not to translated to xml attribs")
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
	
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)
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

class pL(rel_path_command):
	"Line to"
	_fields = ("x", "y")
	_letter = "L"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)

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

class pC(rel_path_command):
	"Cubic Bézier"
	_fields = ("x1", "y1", "x2", "y2", "x", "y")
	_letter = "C"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)

class pS(rel_path_command):
	"Shorthand cubic Bézier"
	_fields = ("x2", "y2", "x", "y")
	_letter = "S"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)

class pQ(rel_path_command):
	"Quadratic Bézier"
	_fields = ("x1", "y1", "x", "y")
	_letter = "Q"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)

class pT(rel_path_command):
	"Shorthand quadratic Bézier"
	_fields = ("x", "y")
	_letter = "T"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)

class pA(rel_path_command):
	"Eliptical arc"
	_fields = ("rx", "ry", "x-axis-rotation", "large-arc-flag", "sweep-flag", "x", "y")
	_letter = "A"
	def __init__(self, *args, relative: Optional[bool] = False) -> None:
		super().__init__(*args, relative=relative)





class pClose(path_command):
	_fields = ()
	_letter = "z"
	def __init__(self, *args) -> None:
		super().__init__(*args)





	
