

import inspect
from rpSVG.SVGLib import Circle, Ellipse, Group, Line, SVGContent, Text, Title, Use
from test.testing import genFiles
from rpSVG.Symbols import Cross, XSight
from rpSVG.SVGStyleText import CSSSty, Sty
from rpSVG.Structs import Re
from rpSVG.Basics import GLOBAL_ENV, Pt, Rotate
import pytest
from rpSVG.Geometry import Elpg, Lna, Lng, Pta, aToPt, ellipseIntersections, vec2_rotate, vec2_segment_intersect


def test_00Intersect(capsys):

	la = (Pta(1,1), Pta(2,3))
	lb = (Pta(3,1.5), Pta(5,0))

	with capsys.disabled():

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

		# ----------------------------------------------

		lb = (Pta(1.1,1.5), Pta(5,0))

		ret = vec2_segment_intersect(*la, *lb)
		testret = [round(x,2) for x in ret]
		assert testret == [1.23, 1.45], testret

		# ----------------------------------------------

		lb = (Pta(-3.1,1.5), Pta(1,1.5))

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

		# ----------------------------------------------

		la = (Pta(-10,-1), Pta(1,1))
		lb = (Pta(-10,1), Pta(1,-1))

		ret = vec2_segment_intersect(*la, *lb)
		testret = [round(x,1) for x in ret]
		assert testret == [-4.5, 0.0], testret

		# ----------------------------------------------

		la = (Pta(-10,-1), Pta(-10,1))
		lb = (Pta(1,-1), Pta(1,1))

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

		la = (Pta(240, 400), Pta(640, 300))
		lb = (Pta(740, 355), Pta(740, 245))

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret


def genCITPart(p_sc, p_centerx, p_centery, p_symbdict, rot=0):

	def rot_ab(p_a, p_b, p_ac, p_rot):
		if p_rot != 0:
			ra = aToPt(vec2_rotate(Pta(*p_a), rot, center=p_ac))
			rb = aToPt(vec2_rotate(Pta(*p_b), rot, center=p_ac))
		else:
			ra = p_a
			rb = p_b
		return ra, rb

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
	if rot != 0:
		gr1.addTransform(Rotate(rot,*center))
	gr1.addChild(Ellipse(*center, rx, ry)).setClass('caixas')
	# Y
	gr1.addChild(Line(center.x, top_axes, center.x, bot_axes)).setClass('aid1')
	# X
	gr1.addChild(Line(left_axes, center.y, right_axes, center.y)).setClass('aid1')

	## Linha 1 ----------------------------------------------------------

	linex1 = center.x + 90
	linex2 = center.x + 130
	ac = Pta(*center)
	a = Pt(linex1, top_axes)
	b = Pt(linex2, bot_axes)

	ra, rb = rot_ab(a, b, ac, rot)

	gr1.addChild(Use(a, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))

	gr1.addChild(Text(a.x+20, a.y+10)).\
		setClass('text1').\
		setText("A1")

	gr1.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B1")

	gr1.addChild(Use(b, p_symbdict["extremesymb"].getSel()).setClass('mrkr'))
	
	elip = Elpg(center, rx, ry=ry, vertang=rot)
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

	ra, rb = rot_ab(a, b, ac, rot)

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

	ra, rb = rot_ab(a, b, ac, rot)

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

	ra, rb = rot_ab(a, b, ac, rot)

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
	# crsymb_centerMarker = sc.addChild(Cross(30,30), todefs=True)
	extremesymb = xsight
	pointsymb = sc.addChild(Circle(0,0,6), todefs=True, noyinvert=True)
	#
	# =========================================================================

	if p_ynvert:
		title_height = 1060
		mainlabel = "Elliptical curve intersections (y-inverted)"
		topY = 790
	else:
		title_height = 140
		mainlabel = "Elliptical curve intersections"
		topY = 410

	sc.addChild(Title(mainlabel))

	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 40, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText(mainlabel)

	genCITPart(sc, 400, topY, {"extremesymb": extremesymb, "pointsymb": pointsymb,})
	genCITPart(sc, 1120, topY, {"extremesymb": extremesymb, "pointsymb": pointsymb,}, rot=30)

	return sc

def test_00Rotation():

	ct = Pta(3,2)
	p1 = Pta(5,2)
	assert vec2_rotate(p1, 90, center=ct).all() == Pta(3,4).all()

def test_00CurveIntersectTest_(capsys):

	with capsys.disabled():

		sc = genCurveIntersectTest(False)
		genFiles(inspect.currentframe().f_code.co_name, sc)

def test_00_CurveIntersectTestYInv(capsys):

	with capsys.disabled():

		sc = genCurveIntersectTest(True)
		genFiles(inspect.currentframe().f_code.co_name, sc)
