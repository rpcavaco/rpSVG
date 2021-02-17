
from typing import Optional, Union
from math import atan, degrees
from re import split as re_split

from rpcbSVG.Basics import MINDELTA, Pt, Env, XLINK_NAMESPACE, _attrs_struct, _withunits_struct, _kwarg_attrs_struct, glRd, hashed_href, isNumeric, removeDecsep, strictToNumber, toNumberAndUnit


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
	def getValues(self):
		return [glRd(x[0]) for x in [toNumberAndUnit(v) for v in self.getall()]]
	def isEmpty(self):
		return [x[0] for x in [toNumberAndUnit(v) for v in self.getall()]] == [0,0,0,0]
	def yinvert(self, p_contentheight: Union[float, int]):
		h = strictToNumber(self.height)
		self.y = p_contentheight - strictToNumber(self.y) - h
		return self

class VBox(_attrs_struct):
	_fields = ("viewBox",)
	def __init__(self, *args) -> None:
		rect = None
		if len(args) == 1 and isinstance(args[0], list):
			rect = Re(*args[0])
		if len(args) > 1:
			rect = Re(*args)
		if not rect is None:
			cont = " ".join(list(rect.iterUnitsRemoved()))
			super().__init__(cont)
		else:
			super().__init__(*args)
	def cloneFromRect(self, p_rect: Re, scale: Optional[float] = None):
		if not scale is None:
			cont = " ".join([str(removeDecsep(round(float(at)) * scale)) for at in p_rect.iterUnitsRemoved()])
		else:
			cont = " ".join(list(p_rect.iterUnitsRemoved()))
		setattr(self, 'viewBox', cont)
	def getValues(self):
		ret = []
		val = getattr(self, 'viewBox')
		if len(val) > 0:
			ret = [x[0] for x in [toNumberAndUnit(v) for v in re_split(r"[\s]+", val)]]
		return ret
	def isEmpty(self):
		return [x[0] for x in [toNumberAndUnit(v) for v in self.getValues()]] == [0,0,0,0]

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
	def setRCRadiuses(self, rx, ry=None):
		self.rx = rx
		if ry is None:
			self.ry = rx
		else:
			self.ry = ry

class Ci(_withunits_struct):
	_fields = ("cx",  "cy", "r") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])
	def yinvert(self, p_contentheight: Union[float, int]):
		self.cy = p_contentheight - strictToNumber(self.cy)
		return self

class Elli(_withunits_struct):
	_fields = ("cx",  "cy", "rx", "ry") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=["0"])
	def yinvert(self, p_contentheight: Union[float, int]):
		self.cy = p_contentheight - strictToNumber(self.cy)
		return self

class Li(_withunits_struct):
	_fields = ("x1",  "y1", "x2", "y2") 
	def __init__(self, *args) -> None:
		l =  len(args)
		if l == 2 and isinstance(args[0], Pt) and isinstance(args[1], Pt):
			argslist = (args[0].x, args[0].y, args[1].x, args[1].y)
		else:
			argslist = args
		super().__init__(*argslist, defaults=["0"])
	def getAngle(self):
		ret = None
		dx = strictToNumber(getattr(self, "x2")) - strictToNumber(getattr(self, "x1"))
		dy = strictToNumber(getattr(self, "y2")) - strictToNumber(getattr(self, "y1"))
		if dx < MINDELTA:
			if dy > MINDELTA:
				ret = 90
			if dy < MINDELTA:
				ret = 270
		else:
			ret = degrees(atan(dy/dx))
		return ret
	def yinvert(self, p_contentheight: Union[float, int]):
		self.y1 = p_contentheight - strictToNumber(self.y1)
		self.y2 = p_contentheight - strictToNumber(self.y2)
		return self

class Us(_withunits_struct):
	_fields = ("x",  "y", "width", "height", f"{{{XLINK_NAMESPACE}}}href") 
	def __init__(self, *args) -> None:
		l =  len(args)
		argslist = None
		if l != 5:
			if l == 2:
				if isinstance(args[0], Pt) and isinstance(args[1], str):
					argslist = (glRd(args[0].x), glRd(args[0].y), None, None, args[1])
				elif isinstance(args[0], Re) and isinstance(args[1], str):
					argslist = (glRd(args[0].x), glRd(args[0].y), glRd(args[0].width), glRd(args[0].height), args[1])
				else:
					raise TypeError(f"'Us' element was given 2 arguments with types ({str(type(args[0]))},{str(type(args[1]))}), expected Pt+str or Re+str")
		if argslist is None:
			if l >= 4:
				argslist = [glRd(x) for x in args[:4]]
				if l > 4:
					argslist.extend(args[4:])
			else:
				argslist = args
			# argslist = [glRd(x) for x in args if isNumeric(x)]
		super().__init__(*argslist, defaults=None)
	def yinvert(self, p_contentheight: Union[float, int]):
		if hasattr(self, 'y'):
			prevval = strictToNumber(self.y)
			self.y = p_contentheight - prevval
		return self

class Pth(_withunits_struct):
	_fields = ("d") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)
	def hasPoints(self) -> bool:
		ret = False
		pts = self.get("d")
		if not pts is None:
			ret = len(pts) > 0
		return ret

class Pl(_withunits_struct):
	_fields = ("points",) 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)
	def hasPoints(self) -> bool:
		ret = False
		pts = self.get("points")
		if not pts is None:
			ret = len(pts) > 0
		return ret


class Mrk(_withunits_struct):
	_fields = ("refX", "refY", "markerWidth", "markerHeight", "orient", "markerUnits") 
	def __init__(self, *args) -> None:
		l = len(args)
		assert l >= 4, f"Mrk needs at least 4 arguments, {l} given"
		if l > 5:
			assert l[4] in (None, "strokeWidth", "userSpaceOnUse")
		if l > 6:
			assert isNumeric(l[5]) or l[5] == "auto"
		super().__init__(*args, defaults=None)

class MrkProps(_kwarg_attrs_struct):
	_fields = ("marker-start", "marker-mid", "marker-end")
	_funciris = _fields
	def __init__(self, marker_start: Optional[str] = None, marker_mid: Optional[str] = None, marker_end: Optional[str] = None) -> None:
		super().__init__(marker_start = marker_start, marker_mid = marker_mid, marker_end = marker_end)

class GraSt(_attrs_struct):
	_fields = ("offset", "stop-color", "stop-opacity") 
	def __init__(self, *args) -> None:
		super().__init__(*args, defaults=None)

class LiGra(_withunits_struct):
	_fields = ("x1",  "y1", "x2", "y2", f"{{{XLINK_NAMESPACE}}}href", "gradientUnits", "spreadMethod", "gradientTransform") 
	def __init__(self, *args) -> None:
		l =  len(args)
		if l >= 2 and isinstance(args[0], Pt) and isinstance(args[1], Pt):
			argslist = [args[0].x, args[0].y, args[1].x, args[1].y]
			argslist.extend(args[2:])
		else:
			argslist = args
		l2 = len(argslist)
		if l2 > 5:
			assert argslist[5] in ("userSpaceOnUse", "objectBoundingBox")
		if l2 > 6:
			assert argslist[6] in ("pad", "reflect", "repeat")
		super().__init__(*argslist)
	def yinvert(self, p_contentheight: Union[float, int]):
		self.y1 = p_contentheight - strictToNumber(self.y1)
		self.y2 = p_contentheight - strictToNumber(self.y2)
		return self

class RaGra(_withunits_struct):
	_fields = ("cx",  "cy", "r", "fx", "fy", f"{{{XLINK_NAMESPACE}}}href", "gradientUnits", "spreadMethod", "gradientTransform") 
	def __init__(self, *args) -> None:
		#argslist = list(args)
		l =  len(args)
		if l > 6:
			assert args[6] in ("userSpaceOnUse", "objectBoundingBox")
		if l > 7:
			assert args[7] in ("pad", "reflect", "repeat")
		super().__init__(*args)
	def yinvert(self, p_contentheight: Union[float, int]):
		self.cy = p_contentheight - strictToNumber(self.cy)
		self.fy = p_contentheight - strictToNumber(self.fy)
		return self

class Tx(_withunits_struct):
	_fields = ("x",  "y", "dx", "dy", "rotate", "textLength", "lengthAdjust") 
	def __init__(self, *args) -> None:
		l =  len(args)
		if l > 6:
			assert args[6] in ("spacing", "spacingAndGlyphs")
		super().__init__(*args)
	def yinvert(self, p_contentheight: Union[float, int]):
		if hasattr(self, "y"):
			self.y = p_contentheight - strictToNumber(self.y)
		if hasattr(self, "dy"):
			dyv, _u = toNumberAndUnit(self.dy)
			if dyv > 0:
				self.dy =  "-" + str(self.dy)
			else:
				self.dy =  str(self.dy)[1:]
		return self

class TxRf(_attrs_struct):
	_fields = (f"{{{XLINK_NAMESPACE}}}href",) 
	def __init__(self, p_text: str) -> None:
		super().__init__(hashed_href(p_text))

class TxPth(_withunits_struct):
	_fields = (f"{{{XLINK_NAMESPACE}}}href", "startOffset",  "method", "spacing") 
	def __init__(self, *args) -> None:
		argslist = list(args)
		l =  len(argslist)
		if l > 0:
			argslist[0] = hashed_href(argslist[0])
		if l > 2:
			assert argslist[2] in ("align", "stretch")
		if l > 3:
			assert argslist[3] in ("auto", "exact")
		super().__init__(*argslist)

class Img(_withunits_struct):
	_fields = ("x",  "y", "width", "height", f"{{{XLINK_NAMESPACE}}}href", "preserveAspectRatio") 
	def __init__(self, *args) -> None:
		l =  len(args)
		argslist = None
		if l != 6:
			if l == 2:
				if isinstance(args[0], Pt) and isinstance(args[1], str):
					argslist = (args[0].x, args[0].y, None, None, args[1])
				elif isinstance(args[0], Re) and isinstance(args[1], str):
					argslist = (args[0].x, args[0].y, args[0].width, args[0].height, args[1])
				else:
					raise TypeError(f"'Img' element was given 2 arguments with types ({str(type(args[0]))},{str(type(args[1]))}), expected Pt+str or Re+str")
		if argslist is None:
			argslist = args
		super().__init__(*argslist, defaults=None)
	def yinvert(self, p_contentheight: Union[float, int]):
		h = strictToNumber(self.height)
		self.y = p_contentheight - strictToNumber(self.y) - h
		return self

class Patt(_withunits_struct):
	_fields = ("x",  "y", "width", "height", "patternUnits", "patternTransform", f"{{{XLINK_NAMESPACE}}}href", "patternContentUnits", "preserveAspectRatio") 
	def __init__(self, *args) -> None:
		l =  len(args)
		argslist = list(args)
		if l != 9:
			if l > 4:
				assert argslist[4]  in ("userSpaceOnUse", "objectBoundingBox")
			elif l == 4:
				argslist.append("userSpaceOnUse") # adds automatically userSpaceOnUse if just 4 params are given
			if l > 7:
				assert argslist[7]  in ("userSpaceOnUse", "objectBoundingBox")
			if l > 6:
				argslist[6] = hashed_href(argslist[6])
		super().__init__(*argslist, defaults=None)
	def yinvert(self, p_contentheight: Union[float, int]):
		h = strictToNumber(self.height)
		self.y = p_contentheight - strictToNumber(self.y) - h
		return self

class Symb(VBox):
	_fields = ("viewBox", "preserveAspectRatio")
	def __init__(self, *viewboxargs, preserveAspectRatio=None) -> None:
		super().__init__(*viewboxargs)
		if not preserveAspectRatio is None:
			self.preserveAspectRatio = preserveAspectRatio

