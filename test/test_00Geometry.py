

import inspect
from rpSVG.SVGLib import Circle, Ellipse, Line, SVGContent, Text, Title, Use
from test.testing import genFiles
from rpSVG.Symbols import Cross, XSight
from rpSVG.SVGStyleText import CSSSty, Sty
from rpSVG.Structs import Re
from rpSVG.Basics import GLOBAL_ENV, Pt
import pytest
from rpSVG.Geometry import Elpg, Lna, Lng, Pta, ellipseIntersections, vec2_segment_intersect


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

def genCurveIntersectTest(p_ynvert):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', '20pt', 'font-family', 'Helvetica', selector='.text1'))
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
	pointsymb = sc.addChild(Circle(0,0,6), todefs=True)
	#
	# =========================================================================

	if sc.getYInvertFlag():
		title_height = 1060
	else:
		title_height = 140

	if p_ynvert:
		mainlabel = "Elliptical curve intersections (y-inverted)"
	else:
		mainlabel = "Elliptical curve intersections"

	sc.addChild(Title(mainlabel))

	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 40, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText(mainlabel)

	center = Pt(450, 510)
	wid_hei = (460, 390)
	rx = wid_hei[0] / 2
	ry = wid_hei[1] / 2
	larger_r = max(rx, ry)
	offset_axes = 34
	top_axes = center.y - larger_r - offset_axes
	bot_axes = center.y + larger_r + offset_axes
	left_axes = center.x - larger_r - offset_axes
	right_axes = center.x + larger_r + offset_axes
	sc.addChild(Ellipse(*center, rx, ry)).setClass('caixas')
	# Y
	sc.addChild(Line(center.x, top_axes, center.x, bot_axes)).setClass('aid1')
	# X
	sc.addChild(Line(left_axes, center.y, right_axes, center.y)).setClass('aid1')

	## Linha 1 ----------------------------------------------------------

	linex1 = center.x + 130
	linex2 = center.x + 200
	a = Pt(linex1, top_axes)
	b = Pt(linex2, bot_axes)
	sc.addChild(Use(a, extremesymb.getSel()).setClass('mrkr'))

	sc.addChild(Text(a.x+20, a.y+10)).\
		setClass('text1').\
		setText("A1")

	sc.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B1")

	sc.addChild(Use(b, extremesymb.getSel()).setClass('mrkr'))
	
	elip = Elpg(center, rx, ry=ry)
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	sc.addChild(Use(p1, pointsymb.getSel()).setClass('ptmrkr'))
	sc.addChild(Use(p2, pointsymb.getSel()).setClass('ptmrkr'))

	sc.addChild(Line(linex1, top_axes, *p2)).setClass('secondary')
	sc.addChild(Line(*p1, *p2)).setClass('aid2')
	sc.addChild(Line(*p1, linex2, bot_axes)).setClass('secondary')

	## Linha 2 ----------------------------------------------------------

	linex1 = linex2 = center.x + 40
	a = Pt(linex1, top_axes)
	b = Pt(linex2, bot_axes)
	sc.addChild(Use(a, extremesymb.getSel()).setClass('mrkr'))


	sc.addChild(Text(a.x+20, a.y+10)).\
		setClass('text1').\
		setText("A2")

	sc.addChild(Text(b.x+20, b.y+10)).\
		setClass('text1').\
		setText("B2")

	sc.addChild(Use(b, extremesymb.getSel()).setClass('mrkr'))
	
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	sc.addChild(Use(p1, pointsymb.getSel()).setClass('ptmrkr'))
	sc.addChild(Use(p2, pointsymb.getSel()).setClass('ptmrkr'))

	sc.addChild(Line(linex1, top_axes, *p2)).setClass('secondary')
	sc.addChild(Line(*p1, *p2)).setClass('aid2')
	sc.addChild(Line(*p1, linex2, bot_axes)).setClass('secondary')

	## Linha 3 ----------------------------------------------------------

	linex1 = left_axes
	linex2 = right_axes
	hor = top_axes + 160
	a = Pt(linex1, hor)
	b = Pt(linex2, hor)
	sc.addChild(Use(a, extremesymb.getSel()).setClass('mrkr'))


	sc.addChild(Text(a.x-50, a.y)).\
		setClass('text1').\
		setText("A3")

	sc.addChild(Text(b.x+20, b.y+20)).\
		setClass('text1').\
		setText("B3")

	sc.addChild(Use(b, extremesymb.getSel()).setClass('mrkr'))
	
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	sc.addChild(Use(p1, pointsymb.getSel()).setClass('ptmrkr'))
	sc.addChild(Use(p2, pointsymb.getSel()).setClass('ptmrkr'))

	sc.addChild(Line(linex1, hor, *p2)).setClass('secondary')
	sc.addChild(Line(*p1, *p2)).setClass('aid2')
	sc.addChild(Line(*p1, linex2, hor)).setClass('secondary')

	## Linha 4 ----------------------------------------------------------

	linex1 = left_axes
	linex2 = right_axes
	hor1 = top_axes + 460
	hor2 = top_axes + 240
	a = Pt(linex1, hor1)
	b = Pt(linex2, hor2)
	sc.addChild(Use(a, extremesymb.getSel()).setClass('mrkr'))


	sc.addChild(Text(a.x-50, a.y)).\
		setClass('text1').\
		setText("A4")

	sc.addChild(Text(b.x+20, b.y+20)).\
		setClass('text1').\
		setText("B4")

	sc.addChild(Use(b, extremesymb.getSel()).setClass('mrkr'))
	
	p1, p2 = ellipseIntersections(Lng(a,b), elip)
	sc.addChild(Use(p1, pointsymb.getSel()).setClass('ptmrkr'))
	sc.addChild(Use(p2, pointsymb.getSel()).setClass('ptmrkr'))

	sc.addChild(Line(linex1, hor1, *p2)).setClass('secondary')
	sc.addChild(Line(*p1, *p2)).setClass('aid2')
	sc.addChild(Line(*p1, linex2, hor2)).setClass('secondary')


	return sc

def test_00X(capsys):

	with capsys.disabled():

		sc = genCurveIntersectTest(False)
		genFiles(inspect.currentframe().f_code.co_name, sc)
