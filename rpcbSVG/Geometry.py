
from numpy import empty_like, dot, array, ndarray

MINNUM = 0.0000001

def Pta(x, y):
	return array((x, y))

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
	perpend = vec2_perpendicular(vec_a)
	denomin = dot(perpend, vec_b)
	if abs(denomin) > MINNUM:
		numer = dot(perpend, vec_origins_separation)
		b_scalar_multiplier = numer / denomin
		intpt = b_scalar_multiplier * vec_b + b1
	else:
		b_scalar_multiplier = 0
		intpt = None
	return b_scalar_multiplier, intpt

def vec2_segment_intersect(a1,a2, b1,b2):
	"""Intersection of two line segments, each described by their extreme points:
			first: a1, a2
			second: b1, b2
		Returns:
			- None if segments don't intersect
			- the intersection point
	"""
	ret = None
	scal_mult, intersection = vec2_line_intersect(a1,a2, b1,b2)
	if not intersection is None:
		# print("scalar:", scal_mult)
		if scal_mult >= 0:
			if scal_mult <= 1.0:
				ret = intersection
	return ret
		



