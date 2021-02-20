
from numpy import empty_like, dot, array, ndarray

MINNUM = 0.0000001

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
		




