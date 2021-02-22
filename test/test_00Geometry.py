

import inspect
from rpSVG.SVGLib import AnalyticalPath, Circle, Ellipse, Group, Line, SVGContent, Text, Title, Use
from test.testing import genFiles
from rpSVG.Symbols import Cross, XSight
from rpSVG.SVGStyleText import CSSSty, Sty
from rpSVG.Structs import Re
from rpSVG.Basics import GLOBAL_ENV, Pt, Rotate, pA, pL, pM, ptAdd
import pytest
from rpSVG.Geometry import Elpg, Lng, Ptg, ellipseIntersections, ellipticalArcCenter, vec2_area2, vec2_arecollinear, vec2_crossprod_det, vec2_rotate, vec2_segment_intersect


#@pytest.mark.solo
def test_00Colinearity(capsys):

	pA = Ptg(0,0)
	pB = Ptg(4,3)
	pP = Ptg(2,1.5)

	ret = vec2_arecollinear(pA, pB, pP, inside_segment=True)
	assert ret

	pP = Ptg(4,3)
	ret = vec2_arecollinear(pA, pB, pP, inside_segment=True)
	assert ret

	pP = Ptg(4.013333332,3.01)
	ret = vec2_arecollinear(pA, pB, pP, inside_segment=True)
	assert not ret

	pP = Ptg(4.013333332,3.01)
	ret = vec2_arecollinear(pA, pB, pP, inside_segment=False)
	assert ret

	pP = Ptg(-0.013333333,-0.01)
	ret = vec2_arecollinear(pA, pB, pP, inside_segment=True)
	assert not ret

	pP = Ptg(2.5,1.5)
	ret = vec2_arecollinear(pA, pB, pP)
	assert not ret

def test_00Rotation():

	ct = Ptg(3,2)
	p1 = Ptg(5,2)
	assert vec2_rotate(p1, 90, center=ct) == Ptg(3,4)

def test_00Intersect():

	la = (Ptg(1,1), Ptg(2,3))
	lb = (Ptg(3,1.5), Ptg(5,0))

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None, ret

	# ----------------------------------------------

	lb = (Ptg(1.1,1.5), Ptg(5,0))

	ret = vec2_segment_intersect(*la, *lb)
	testret = [round(x,2) for x in ret]
	assert testret == [1.23, 1.45], testret

	# ----------------------------------------------

	lb = (Ptg(-3.1,1.5), Ptg(1,1.5))

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None, ret

	# ----------------------------------------------

	la = (Ptg(-10,-1), Ptg(1,1))
	lb = (Ptg(-10,1), Ptg(1,-1))

	ret = vec2_segment_intersect(*la, *lb)
	testret = [round(x,1) for x in ret]
	assert testret == [-4.5, 0.0], testret

	# ----------------------------------------------

	la = (Ptg(-10,-1), Ptg(-10,1))
	lb = (Ptg(1,-1), Ptg(1,1))

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None, ret

	la = (Ptg(240, 400), Ptg(640, 300))
	lb = (Ptg(740, 355), Ptg(740, 245))

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None, ret


def genCompleteEllipsePart(p_sc, p_centerx, p_centery, p_symbdict, rot=0):

	def rot_ab(p_a, p_b, p_ac, p_rot):
		if p_rot != 0:
			ra = vec2_rotate(Ptg(*p_a), p_rot, center=p_ac)
			rb = vec2_rotate(Ptg(*p_b), p_rot, center=p_ac)
		else:
			ra = p_a
			rb = p_b
		return ra, rb

	_rot = rot

	center = Pt(p_centerx, p_centery)
	wid_hei = (340, 250)
	rx = wid_hei[0] / 2
	ry = wid_hei[1] / 2
	offset_axes = 42
	top_axes = center.y - ry - offset_axes
	bot_axes = center.y + ry + offset_axes
	left_axes = center.x - rx - offset_axes
	right_axes = center.x + rx + offset_axes

	gr1 = p_sc.addChild(Group())
	if _rot != 0:
		gr1.addTransform(Rotate(abs(_rot), *center))
	gr1.addChild(Ellipse(*center, rx, ry)).setClass('caixas')
	# Y
	gr1.addChild(Line(center.x, top_axes, center.x, bot_axes)).setClass('aid1')
	# X
	gr1.addChild(Line(left_axes, center.y, right_axes, center.y)).setClass('aid1')

	## Linha 1 ----------------------------------------------------------

	linex1 = center.x + 90
	linex2 = center.x + 130
	ac = Ptg(*center)
	a = Pt(linex1, top_axes)
	b = Pt(linex2, bot_axes)

	ra, rb = rot_ab(a, b, ac, _rot)

	gr1.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))

	gr1.addChild(Text(a.x+20, a.y+10)).\
		setClass('text1').\
		setText("A1")

	gr1.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B1")

	gr1.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	
	elip = Elpg(center, rx, ry=ry, vertang=_rot)
	p1, p2 = ellipseIntersections(Lng(a,b), elip)

	p_sc.addChild(Use(p1, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))
	p_sc.addChild(Use(p2, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))

	p_sc.addChild(Line(*ra, *p2)).setClass('secondary')
	p_sc.addChild(Line(*p1, *p2)).setClass('aid2')
	p_sc.addChild(Line(*p1, *rb)).setClass('secondary')

	## Linha 2 ----------------------------------------------------------

	linex1 = linex2 = center.x + 20
	a = Pt(linex1, top_axes)
	b = Pt(linex2, bot_axes)

	ra, rb = rot_ab(a, b, ac, _rot)

	gr1.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))

	gr1.addChild(Text(a.x+20, a.y+10)).\
		setClass('text1').\
		setText("A2")

	gr1.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B2")

	gr1.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	p_sc.addChild(Use(p1, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))
	p_sc.addChild(Use(p2, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))

	p_sc.addChild(Line(*ra, *p2)).setClass('secondary')
	p_sc.addChild(Line(*p1, *p2)).setClass('aid2')
	p_sc.addChild(Line(*p1, *rb)).setClass('secondary')

	## Linha 3 ----------------------------------------------------------

	linex1 = left_axes
	linex2 = right_axes
	hor = top_axes + 130
	a = Pt(linex1, hor)
	b = Pt(linex2, hor)

	ra, rb = rot_ab(a, b, ac, _rot)

	gr1.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))


	gr1.addChild(Text(a.x-50, a.y+8)).\
		setClass('text1').\
		setText("A3")

	gr1.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B3")

	gr1.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	p_sc.addChild(Use(p1, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))
	p_sc.addChild(Use(p2, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))

	p_sc.addChild(Line(*ra, *p2)).setClass('secondary')
	p_sc.addChild(Line(*p1, *p2)).setClass('aid2')
	p_sc.addChild(Line(*p1, *rb)).setClass('secondary')

	## Linha 4 ----------------------------------------------------------

	linex1 = left_axes
	linex2 = right_axes
	hor1 = top_axes + 260
	hor2 = top_axes + 70
	a = Pt(linex1, hor1)
	b = Pt(linex2, hor2)

	ra, rb = rot_ab(a, b, ac, _rot)

	gr1.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))


	gr1.addChild(Text(a.x-50, a.y+12)).\
		setClass('text1').\
		setText("A4")

	gr1.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B4")

	gr1.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	p_sc.addChild(Use(p1, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))
	p_sc.addChild(Use(p2, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))

	p_sc.addChild(Line(*ra, *p2)).setClass('secondary')
	p_sc.addChild(Line(*p1, *p2)).setClass('aid2')
	p_sc.addChild(Line(*p1, *rb)).setClass('secondary')

def genEllipticArcPart(p_sc, p_centerx, p_centery, p_symbdict, rot=0):

	width = 400
	deltah = 100
	deltav = 60
	height = 380

	hw = width / 2
	hh = height / 2
	deltaXarc = hw - deltah
	deltaYarc = hh - deltav
	left = p_centerx - hw
	right = p_centerx + deltah
	top1 = p_centery - hh
	top2 = p_centery + deltav

	radiiL = (200, 150)
	radiiS = (20, 16)

	p0 = Pt(left, top1)
	p1 = ptAdd(p0,Pt(deltaXarc,deltaYarc))
	ct = ellipticalArcCenter(p0, p1, *radiiL, largearcflag=0, sweepflag=0, angle=0)
	elip = Elpg(ct, radiiL[0], ry=radiiL[1], vertang=rot)

	a = Pt(left, top1 + deltaYarc)
	b = Pt(left+deltaXarc, top1)

	pInt1, pInt2 = ellipseIntersections(Lng(a,b), elip)
	area1 = vec2_area2((p0, pInt1, p1))
	area2 = vec2_area2((p0, pInt2, p1))
	if area2 > area1:
		intpt = pInt1
	else:
		intpt = pInt2

	p_sc.addChild(Use(ct, p_symbdict["crsymb"].getSel()).setClass('mrkr'))
	with p_sc.addChild(AnalyticalPath()).setClass('caixas') as pth:
		pth.addCmd(pM(*p0))
		pth.addCmd(pA(*radiiL,rot,0,0,*p1))

	p_sc.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	p_sc.addChild(Text(a.x-50, a.y+12)).\
		setClass('text1').\
		setText("A1")
	p_sc.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B1")
	p_sc.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))

	p_sc.addChild(Use(intpt, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))

	# #########################################################################

	p0 = Pt(right, top1)
	p1 = Pt(right+deltaXarc, top1+deltaYarc)
	ct = ellipticalArcCenter(p0, p1, *radiiS, largearcflag=1, sweepflag=0, angle=0)
	p_sc.addChild(Use(ct, p_symbdict["crsymb"].getSel()).setClass('mrkr'))

	elip = Elpg(ct, radiiS[0], ry=radiiS[1], vertang=rot)

	with p_sc.addChild(AnalyticalPath()).setClass('caixas') as pth:
		pth.addCmd(pM(*p0))
		pth.addCmd(pA(*radiiS,rot,1,0,*p1))

	a = Pt(right-30, top1 + deltaYarc + 20)
	b = Pt(right+deltaXarc-50, top1+30)

	pInt1, pInt2 = ellipseIntersections(Lng(a,b), elip)
	area1 = vec2_area2((p0, pInt1, p1))
	area2 = vec2_area2((p0, pInt2, p1))
	# large-arc = 1
	# print(area2, area1)
	# if False and abs(area2) < abs(area1):
	if True:
		intpt = pInt1
	else:
		intpt = pInt2

	p_sc.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	p_sc.addChild(Text(a.x-50, a.y+12)).\
		setClass('text1').\
		setText("A1")
	p_sc.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B1")
	p_sc.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))

	p_sc.addChild(Use(intpt, p_symbdict["pointsymb"].getSel()).setClass('ptmrkr'))

	# #########################################################################

	# p0 = Pt(left, top2)
	# p1 = Pt(right+deltaXarc, top1+deltaYarc)
	# ct = ellipticalArcCenter(p0, p1, *radiiS, largearcflag=1, sweepflag=0, angle=0)
	# p_sc.addChild(Use(ct, p_symbdict["crsymb"].getSel()).setClass('mrkr'))
	# with p_sc.addChild(AnalyticalPath()).setClass('caixas') as pth:
	# 	pth.addCmd(pM(left, top2))
	# 	pth.addCmd(pA(*radiiL,rot,0,1,deltaXarc,deltaYarc,relative=True))

	# with p_sc.addChild(AnalyticalPath()).setClass('caixas') as pth:
	# 	pth.addCmd(pM(right, top2))
	# 	pth.addCmd(pA(*radiiS,rot,1,1,deltaXarc,deltaYarc,relative=True))



# "rx", "ry", "x-axis-rotation", "large-arc-flag", "sweep-flag", "x", "y



def genCurveIntersectTest(p_ynvert):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', '16pt', 'font-family', 'Helvetica', selector='.text1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', '#B90000', 'stroke-width', 4, selector='.secondary'))
	sc.addStyleRule(CSSSty('stroke', 'grey', 'stroke-width', 1, selector='.aid1'))
	sc.addStyleRule(CSSSty('stroke', 'grey', 'stroke-width', 3, 'stroke-dasharray', '5,3', selector='.aid2'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', '#404040', 'font-size', '20pt', 'font-family', 'Helvetica','stroke-width', 2, 'text-anchor', 'middle', selector='.lbls'))
	sc.addStyleRule(CSSSty('stroke', 'black', selector='.mrkr'))
	sc.addStyleRule(CSSSty('stroke', 'black', 'fill', 'white', 'stroke-width', 2, selector='.ptmrkr'))

	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(16,16,2), todefs=True, noyinvert=True)
	crsymb = sc.addChild(Cross(30,30), todefs=True)
	extremesymb = xsight
	pointsymb = sc.addChild(Circle(0,0,6), todefs=True, noyinvert=True)
	#
	# =========================================================================

	if p_ynvert:
		title_height = 1060
		mainlabel = "Elliptical curve intersections (y-inverted)"
		topY = 790
		row2Y = 300
	else:
		title_height = 140
		mainlabel = "Elliptical curve intersections"
		topY = 410
		row2Y = 900

	sc.addChild(Title(mainlabel))

	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 40, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText(mainlabel)

	sdict = {"crsymb": crsymb, "extremesymb": extremesymb, "pointsymb": pointsymb}

	genCompleteEllipsePart(sc, 400, topY, sdict)

	if p_ynvert:
		rot_ang = -30
	else:
		rot_ang = 30

	genCompleteEllipsePart(sc, 1120, topY, sdict, rot=rot_ang)

	sc.addComment("Ellipitcal Arcs")

	genEllipticArcPart(sc, 400, row2Y, sdict, rot=0)

	return sc

@pytest.mark.solo
def test_00CurveIntersectTest_(capsys):

	with capsys.disabled():

		sc = genCurveIntersectTest(False)
		genFiles(inspect.currentframe().f_code.co_name, sc)

def test_00CurveIntersectTestYInv(capsys):

	with capsys.disabled():

		sc = genCurveIntersectTest(True)
		genFiles(inspect.currentframe().f_code.co_name, sc)
