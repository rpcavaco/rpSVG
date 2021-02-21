
from math import sqrt
from rpSVG.Basics import Elp, Ln, Pt, lineEquationParams, ptGetAngle
from numpy import empty_like, dot, array, ndarray

MINNUM = 0.0000001

###############################################################################
# Vector geometry using numpy
###############################################################################

def Pta(x, y):
	return array((float(x), float(y)))

def Lna(pt1, pt2):
	return (Pta(*pt1), Pta(*pt2))

def Elpa(pt, rx, ry=None, vertang=0):
	if ry is None:
		ret = (Pta(*pt), float(rx), None, float(vertang))
	else:
		ret = (Pta(*pt), float(rx), float(ry), float(vertang))
	return ret

def vec2_perpendicular(p_a):
	assert isinstance(p_a, ndarray)
	b = empty_like(p_a)
	b[0] = -p_a[1]
	b[1] = p_a[0]
	return b

def vec2_line_intersect(a1,a2, b1,b2):
	"""Intersection of two infinite lines, described by 2 points each:
			first: a1, a2
			second: b1, b2
		Returns a tuple with:
			- scalar multiplier of vector representation of segment from line B
			- the intersection point
		In case of parallel lines, this method returns 0 as scalar and None as intersection point.
	"""
	assert isinstance(a1, ndarray)
	assert isinstance(a2, ndarray)
	assert isinstance(b1, ndarray)
	assert isinstance(b2, ndarray)
	vec_a = a2-a1
	vec_b = b2-b1
	vec_origins_separation = a1-b1
	perpend_a = vec2_perpendicular(vec_a)
	perpend_b = vec2_perpendicular(vec_b)
	denomin = dot(perpend_a, vec_b)
	new_vec = None
	if abs(denomin) > MINNUM:
		a_scalar_multiplier = dot(perpend_b, vec_origins_separation) / denomin
		numer = dot(perpend_a, vec_origins_separation)
		b_scalar_multiplier = numer / denomin
		new_vec = b_scalar_multiplier * vec_b
		intpt = new_vec + b1
	else:
		a_scalar_multiplier = 0
		b_scalar_multiplier = 0
		intpt = None
	return a_scalar_multiplier, b_scalar_multiplier, intpt

def vec2_segment_intersect(a1,a2, b1,b2):
	"""Intersection of two line segments, each described by their extreme points:
			first: a1, a2
			second: b1, b2
		Returns:
			- None if segments don't intersect
			- the intersection point
	"""
	ret = None
	a_scal_mult, b_scal_mult, intersection = vec2_line_intersect(a1,a2, b1,b2)
	#print("scalar:", a_scal_mult, b_scal_mult, intersection)
	if not intersection is None:
		if a_scal_mult >= 0 and a_scal_mult <= 1.0:
			if b_scal_mult >= 0 and b_scal_mult <= 1.0:
				ret = intersection
	return ret
		

###############################################################################
# Algebraic calculations
###############################################################################

def Ptg(x, y):
	return Pt(float(x), float(y))

def Lng(pt1, pt2):
	return Ln(Ptg(*pt1), Ptg(*pt2))

def Elpg(pt, rx, ry=None, vertang=0):
	if ry is None:
		ret = Elp(Ptg(*pt), float(rx), None, float(vertang))
	else:
		ret = Elp(Ptg(*pt), float(rx), float(ry), float(vertang))
	return ret

def ellipseIntersections(p_line: Ln, p_ellipse: Elp):
	"source: http://www.ambrsoft.com/TrigoCalc/Circles2/Ellipse/EllipseLine.htm"
	print("\nintersect line:", p_line, ", ellipse:",p_ellipse )
	tipo, m, c = lineEquationParams(*p_line)
	a = p_ellipse.rx
	b = p_ellipse.ry
	print("a,b:", a, b)
	a2 = pow(a, 2)
	b2 = pow(b, 2)
	h = p_ellipse.pt.x
	k = p_ellipse.pt.y
	if tipo == "vertical":
		c2 = pow(c,2)
		p = (b / a) * sqrt(abs(a2 - c2 - pow(h,2) + (2 * c * h)))
		ya = k + p
		yb = k - p
		xa = xb = c
	elif tipo == "horizontal":
		c2 = pow(c,2)
		k2 = pow(k,2)
		sqrv = abs(b2 - c2 - k2 + (2 * c * k))
		p = (a / b) * sqrt(sqrv)
		xa = h + p
		xb = h - p
		ya = yb = c
	elif tipo == "oblique":
		phi = c - k
		phi2 = pow(phi,2)
		h2 = pow(h,2)
		m2 = pow(m,2)
		p1 = b2 * h - a2 * m * phi
		p2 = a * b * sqrt(abs(b2 + a2 * m2 - 2 * m * phi * h - phi2 - m2 * h2))
		denom = b2 + a2 * m2
		xa = (p1 + p2) / denom
		xb = (p1 - p2) / denom
		ya = m * xa + c
		yb = m * xb + c

	return Pt(xa, ya), Pt(xb, yb)




