
from math import sqrt, cos, sin, sqrt, radians
from typing import Optional, Union
from rpSVG.Basics import Elp, Ln, MINDELTA, NANODELTA, Pt, lineEquationParams, ptAdd, ptGetAngle, ptMult, ptSub
#from numpy import empty_like, dot, array, ndarray, radians, sin, cos, cross
#from numpy.linalg import norm

def Ptg(x, y):
	return Pt(float(x), float(y))

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


# def Pta(x, y):
# 	return array((float(x), float(y)))

# def Lna(pt1, pt2):
# 	return (Pta(*pt1), Pta(*pt2))

# def aToPt(p_pt: ndarray):
# 	return Pt(p_pt[0], p_pt[1])

# def Elpa(pt, rx, ry=None, vertang=0):
# 	if ry is None:
# 		ret = (Pta(*pt), float(rx), None, float(vertang))
# 	else:
# 		ret = (Pta(*pt), float(rx), float(ry), float(vertang))
# 	return ret

# def vec2_perpendicular0(p_a):
# 	assert isinstance(p_a, ndarray)
# 	b = empty_like(p_a)
# 	b[0] = -p_a[1]
# 	b[1] = p_a[0]
# 	return b

def vec2_perpendicular(p_a: Pt):
	assert isinstance(p_a, Pt)
	return Pt(-p_a.y, p_a.x)

def vec2_dotprod(p_a: Pt, p_b: Pt):
	assert isinstance(p_a, Pt)
	assert isinstance(p_b, Pt)
	return p_a.x * p_b.x + p_a.y * p_b.y

def vec2_crossprod_det(p_a: Pt, p_b: Pt):
	assert isinstance(p_a, Pt)
	assert isinstance(p_b, Pt)
	return p_a.x * p_b.y - p_a.y * p_b.x

def vec2_len2(p_a: Pt, p_b: Pt):
	assert isinstance(p_a, Pt)
	assert isinstance(p_b, Pt)
	vec_a = ptSub(p_b, p_a)
	return vec_a.x * vec_a.x + vec_a.y * vec_a.y


# def vec2_line_intersect0(a1,a2, b1,b2):
# 	"""Intersection of two infinite lines, described by 2 points each:
# 			first: a1, a2
# 			second: b1, b2
# 		Returns a tuple with:
# 			- scalar multiplier of vector representation of segment from line B
# 			- the intersection point
# 		In case of parallel lines, this method returns 0 as scalar and None as intersection point.
# 	"""
# 	assert isinstance(a1, ndarray)
# 	assert isinstance(a2, ndarray)
# 	assert isinstance(b1, ndarray)
# 	assert isinstance(b2, ndarray)
# 	vec_a = a2-a1
# 	vec_b = b2-b1
# 	vec_origins_separation = a1-b1
# 	perpend_a = vec2_perpendicular(vec_a)
# 	perpend_b = vec2_perpendicular(vec_b)
# 	denomin = dot(perpend_a, vec_b)
# 	new_vec = None
# 	if abs(denomin) > MINNUM:
# 		a_scalar_multiplier = dot(perpend_b, vec_origins_separation) / denomin
# 		numer = dot(perpend_a, vec_origins_separation)
# 		b_scalar_multiplier = numer / denomin
# 		new_vec = b_scalar_multiplier * vec_b
# 		intpt = new_vec + b1
# 	else:
# 		a_scalar_multiplier = 0
# 		b_scalar_multiplier = 0
# 		intpt = None
# 	return a_scalar_multiplier, b_scalar_multiplier, intpt

def vec2_line_intersect(a1: Pt,a2: Pt, b1: Pt, b2: Pt, mindelta=NANODELTA):
	"""Intersection of two infinite lines, described by 2 points each:
			first: a1, a2
			second: b1, b2
		Returns a tuple with:
			- scalar multiplier of vector representation of segment from line B
			- the intersection point
		In case of parallel lines, this method returns 0 as scalar and None as intersection point.
	"""
	assert isinstance(a1, Pt)
	assert isinstance(a2, Pt)
	assert isinstance(b1, Pt)
	assert isinstance(b2, Pt)
	vec_a = ptSub(a2,a1)
	vec_b = ptSub(b2,b1)
	vec_origins_separation = ptSub(a1,b1)
	perpend_a = vec2_perpendicular(vec_a)
	perpend_b = vec2_perpendicular(vec_b)
	denomin = vec2_dotprod(perpend_a, vec_b)
	new_vec = None
	if abs(denomin) > mindelta:
		a_scalar_multiplier = vec2_dotprod(perpend_b, vec_origins_separation) / denomin
		numer = vec2_dotprod(perpend_a, vec_origins_separation)
		b_scalar_multiplier = numer / denomin
		new_vec = ptMult(b_scalar_multiplier, vec_b)
		intpt = ptAdd(new_vec,  b1)
	else:
		a_scalar_multiplier = 0
		b_scalar_multiplier = 0
		intpt = None
	return a_scalar_multiplier, b_scalar_multiplier, intpt

# def vec2_segment_intersect0(a1,a2, b1,b2):
# 	"""Intersection of two line segments, each described by their extreme points:
# 			first: a1, a2
# 			second: b1, b2
# 		Returns:
# 			- None if segments don't intersect
# 			- the intersection point
# 	"""
# 	ret = None
# 	a_scal_mult, b_scal_mult, intersection = vec2_line_intersect(a1,a2, b1,b2)
# 	#print("scalar:", a_scal_mult, b_scal_mult, intersection)
# 	if not intersection is None:
# 		if a_scal_mult >= 0 and a_scal_mult <= 1.0:
# 			if b_scal_mult >= 0 and b_scal_mult <= 1.0:
# 				ret = intersection
# 	return ret

def vec2_segment_intersect(a1: Pt,a2: Pt, b1: Pt, b2: Pt):
	"""Intersection of two line segments, each described by their extreme points:
			first: a1, a2
			second: b1, b2
		Returns:
			- None if segments don't intersect
			- the intersection point
	"""
	assert isinstance(a1, Pt)
	assert isinstance(a2, Pt)
	assert isinstance(b1, Pt)
	assert isinstance(b2, Pt)
	ret = None
	a_scal_mult, b_scal_mult, intersection = vec2_line_intersect(a1,a2, b1,b2)
	#print("scalar:", a_scal_mult, b_scal_mult, intersection)
	if not intersection is None:
		if a_scal_mult >= 0 and a_scal_mult <= 1.0:
			if b_scal_mult >= 0 and b_scal_mult <= 1.0:
				ret = intersection
	return ret

# def vec2_rotation_mat(p_degangle):
#     angle = radians(p_degangle)
#     return (
#         cos(angle), -sin(angle)],
#         [sin(angle),  cos(angle)]
#     )

# def vec2_scale_mat(p_scale):
#     return array([
#         [p_scale, 0],
#         [0, p_scale]
#     ])

def vec2_rotation_mat(p_degangle):
    angle = radians(p_degangle)
    return (
        (cos(angle), -sin(angle)),
        (sin(angle),  cos(angle))
    )

def vec2_scale_mat(p_scale):
    return (
        (p_scale, 0),
        (0, p_scale)
    )

# def vec2_rotate0(p_pt: ndarray, p_degangle: Union[float, int], center: Optional[ndarray] = None):
# 	assert isinstance(p_pt, ndarray)
# 	if not center is None:
# 		assert isinstance(center, ndarray)
# 		r1 = p_pt - center
# 		r2 = vec2_rotation_mat(p_degangle) @ r1
# 		ret = r2 + center
# 	else:
# 		ret = vec2_rotation_mat(p_degangle) @ p_pt
# 	return ret

def vec2_matmult(p_mat, p_pt: Pt):
	return Pt(
		p_pt.x * p_mat[0][0] + p_pt.y * p_mat[0][1],
		p_pt.x * p_mat[1][0] + p_pt.y * p_mat[1][1]
	)

def vec2_rotate(p_pt: Pt, p_degangle: Union[float, int], center: Optional[Pt] = None):
	assert isinstance(p_pt, Pt)
	if not center is None:
		assert isinstance(center, Pt)
		r1 = ptSub(p_pt, center)
		r2 = vec2_matmult(vec2_rotation_mat(p_degangle), r1)
		ret = ptAdd(r2, center)
	else:
		ret = vec2_matmult(p_pt, vec2_rotation_mat(p_degangle))
	return ret

# def vec2_arecollinear(p_p1: ndarray, p_p2: ndarray, p_p3: ndarray, mindelta=MINDELTA, inside_segment=False):
# 	assert isinstance(p_p1, ndarray)
# 	assert isinstance(p_p2, ndarray)
# 	assert isinstance(p_p3, ndarray)

# 	ret = False
# 	vec_a = p_p2-p_p1
# 	vec_b = p_p3-p_p1

# 	cp = cross(vec_a, vec_b)
# 	if abs(cp) < mindelta:

# 		if not inside_segment:
# 			ret = True
# 		else:
# 			dp = dot(vec_a, vec_b)
# 			len2 = vec_a[0] * vec_a[0] + vec_a[1] * vec_a[1]

# 			ret = True if dp > -mindelta and dp < len2 + mindelta else False
# 	return ret

def vec2_arecollinear(p_p1: Pt, p_p2: Pt, p_p3: Pt, mindelta=MINDELTA, inside_segment=False):
	assert isinstance(p_p1, Pt)
	assert isinstance(p_p2, Pt)
	assert isinstance(p_p3, Pt)

	ret = False
	vec_a = ptSub(p_p2, p_p1)
	vec_b = ptSub(p_p3, p_p1)

	cp = vec2_crossprod_det(vec_a, vec_b)
	print("cp", cp, mindelta, vec_a, vec_b)
	if abs(cp) < mindelta:

		if not inside_segment:
			ret = True
		else:
			dp = vec2_dotprod(vec_a, vec_b)
			len2 = vec_a[0] * vec_a[0] + vec_a[1] * vec_a[1]
			ret = True if dp > -mindelta and dp < len2 + mindelta else False
	return ret



def ellipseIntersections(p_line: Ln, p_ellipse: Elp):
	"""Uses numpy if p_ellipse has rotation angle.
	Algorithm source: http://www.ambrsoft.com/TrigoCalc/Circles2/Ellipse/EllipseLine.htm"""
	tipo, m, c = lineEquationParams(*p_line)
	a = p_ellipse.rx
	b = p_ellipse.ry
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

	if p_ellipse.ang != 0:
		pa = vec2_rotate(Ptg(xa, ya), p_ellipse.ang, center=Ptg(h,k))
		pb = vec2_rotate(Ptg(xb, yb), p_ellipse.ang, center=Ptg(h,k))
		ret = Pt(pa[0], pa[1]), Pt(pb[0], pb[1])
	else:
		ret = Pt(xa, ya), Pt(xb, yb)


	return ret

def ellipticalArcCenter(p_p0: Pt, p_p1: Pt, p_rx, p_ry, largearcflag=0, sweepflag=0, angle=0):
	"""Code source: Batik Project (adapted from Java)
	http://svn.apache.org/repos/asf/xmlgraphics/batik/branches/svg11/sources/org/apache/batik/ext/awt/geom/ExtendedGeneralPath.java
	"""

	p0 = Ptg(*p_p0)
	p1 = Ptg(*p_p1)

	dx2 = (p0.x - p1.x) / 2.0
	dy2 = (p0.y - p1.y) / 2.0
	_angle = radians(angle % 360)
	cosAngle = cos(_angle)
	sinAngle = sin(_angle)

	x1 = cosAngle * dx2 + sinAngle * dy2
	y1 = -sinAngle * dx2 + cosAngle * dy2

	rx = abs(p_rx)
	ry = abs(p_ry)
	Prx = rx * rx
	Pry = ry * ry
	Px1 = x1 * x1
	Py1 = y1 * y1
	# check that radii are large enough
	radiiCheck = Px1/Prx + Py1/Pry
	if radiiCheck > 1:
		rx = sqrt(radiiCheck) * rx
		ry = sqrt(radiiCheck) * ry
		Prx = rx * rx
		Pry = ry * ry

	sign = -1 if largearcflag == sweepflag else 1
	sq0 = ((Prx*Pry)-(Prx*Py1)-(Pry*Px1)) / ((Prx*Py1)+(Pry*Px1))
	sq = 0 if sq0 < 0 else sq0
	coef = sign * sqrt(sq)
	cx1 = coef * ((rx * y1) / ry)
	cy1 = coef * -((ry * x1) / rx)

	sx2 = (p0.x + p1.x) / 2.0
	sy2 = (p0.y + p1.y) / 2.0

	cx = sx2 + (cosAngle * cx1 - sinAngle * cy1)
	cy = sy2 + (sinAngle * cx1 + cosAngle * cy1)

	return Pt(cx, cy)



