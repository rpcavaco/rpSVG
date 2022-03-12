
import inspect
import pytest
import cairosvg

from tests.testing import genFiles

from rpSVG.Geometry import Lna, Pta, vec2_segment_intersect
from rpSVG.Symbols import Cross, Cylinder, Diamond, Server, XSight
from rpSVG.Basics import GLOBAL_ENV, Pt, ptAdd
from rpSVG.SVGStyleText import CSSSty, Sty
from rpSVG.SVGLib import Line, Re, RectRC, SVGContent, Text, Title, Use
from rpSVG.Constructs import TextBox

def generateDiagramming(p_ynvert, p_vcenter_fontszpx, p_capsys):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	vcenter_fontszpx = p_vcenter_fontszpx

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', vcenter_fontszpx, 'font-family', 'Helvetica', selector='.tb1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('stroke', 'grey', 'stroke-width', 1, selector='.aid1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', '#404040', 'font-size', 24, 'font-family', 'Helvetica','stroke-width', 2, 'text-anchor', 'middle', selector='.lbls'))

	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.45, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfilldark'))
	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.3, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfillmed'))
	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.1, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfilllight'))
	sc.addStyleRule(CSSSty('stroke', '#8B8B8B', 'stroke-width', 4, 'stroke-linejoin', 'round', selector='.symbinnerstroke'))

	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(46,46,8), todefs=True, noyinvert=True)
	crsymb_centerMarker = sc.addChild(Cross(20,20), todefs=True)
	#
	# =========================================================================

	if sc.getYInvertFlag():
		title_height = 1060
	else:
		title_height = 140

	if p_ynvert:
		mainlabel = "Diagram (y-inverted)"
	else:
		mainlabel = "Diagram"

	sc.addChild(Title(mainlabel))

	if sc.getYInvertFlag():
		tb1Y = 800
	else:
		tb1Y = 400

	top = tb1Y	
	left = 240
	anchor = Pt(left, top)
	boxdims = (200, 110)


	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 40, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText(mainlabel)

	tb1 = TextBox(*anchor, *boxdims, anchoring="cc", hjustify="center", vcenter_fontszpx=vcenter_fontszpx)
	tb1.setBaseShape(RectRC().setRCRadiuses(14).setClass("caixas"))
	sc.addChild(tb1)
	tb1.getParagraph().setClass("tb1")
	tb1.setText("""Ürümqi
Yiwu""")

	anchor = ptAdd(anchor, Pt(400, -100))

	tb2 = TextBox(*anchor, *boxdims, anchoring="cc", hjustify="center", vcenter_fontszpx=vcenter_fontszpx)
	tb2.setBaseShape(RectRC().setRCRadiuses(14).setClass("caixas"))
	sc.addChild(tb2)
	tb2.getParagraph().setClass("tb1")
	tb2.setText("""Shèngsì
Shenzhen""")

	p1 = tb1.getAnchor()
	p2 = tb2.getAnchor()

	#la = Lna(Pta(*p1), Pta(*p2))
	la = Lna(p1, p2)
	print("la:", la)




	#sc.addChild(Circle(*tb1.getAnchor(), 30)).setStyle(Sty('stroke', '#DA6D1F', 'stroke-width', 6))
	#sc.addChild(Circle(*tb2.getAnchor(), 30)).setStyle(Sty('stroke', '#7D27EF', 'stroke-width', 6))

	lst_contour = tb1.getContour()
	got_X1 = None
	for k in lst_contour:
		lb = Lna(*k)
		intrsct = vec2_segment_intersect(*la, *lb)
		if not intrsct is None:
			got_X1 = intrsct


	lst_contour = tb2.getContour()
	print("lst_crnpts:", lst_contour)
	got_X2 = None
	for i, k in enumerate(lst_contour):
		lb = Lna(*k)

		intrsct = vec2_segment_intersect(*la, *lb)
		print(i, lb, 'X:', intrsct)
		if not intrsct is None:
			got_X2 = intrsct

	sc.addChild(Line(*got_X1, *got_X2).setStyle(Sty('stroke', '#DA6D1F', 'stroke-width', 6)))

	return sc

def test_07Diagramming(capsys):

	with capsys.disabled():
	
		sc = generateDiagramming(False, '18pt', capsys)
		genFiles(inspect.currentframe().f_code.co_name, sc)

def generateX(p_ynvert, p_vcenter_fontszpx, p_capsys):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	vcenter_fontszpx = p_vcenter_fontszpx

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', vcenter_fontszpx, 'font-family', 'Helvetica', selector='.tb1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('stroke', 'grey', 'stroke-width', 1, selector='.aid1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', '#404040', 'font-size', 24, 'font-family', 'Helvetica','stroke-width', 2, 'text-anchor', 'middle', selector='.lbls'))

	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.45, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfilldark'))
	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.3, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfillmed'))
	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.1, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfilllight'))
	sc.addStyleRule(CSSSty('stroke', '#8B8B8B', 'stroke-width', 4, 'stroke-linejoin', 'round', selector='.symbinnerstroke'))

	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(46,46,8), todefs=True, noyinvert=True)
	crsymb_centerMarker = sc.addChild(Cross(20,20), todefs=True)
	#
	# =========================================================================

	if sc.getYInvertFlag():
		title_height = 1060
	else:
		title_height = 140

	if p_ynvert:
		mainlabel = "Diagram (y-inverted)"
	else:
		mainlabel = "Diagram"

	sc.addChild(Title(mainlabel))

	if sc.getYInvertFlag():
		tb1Y = 800
	else:
		tb1Y = 400

	top = tb1Y	
	left = 240
	anchor = Pt(left, top)
	boxdims = (200, 110)


	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 40, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText(mainlabel)

	tb1 = TextBox(*anchor, *boxdims, anchoring="cc", hjustify="center", vcenter_fontszpx=vcenter_fontszpx)
	tb1.setBaseShape(RectRC().setRCRadiuses(14).setClass("caixas"))
	sc.addChild(tb1)
	tb1.getParagraph().setClass("tb1")
	tb1.setText("""Ürümqi
Yiwu""")

	anchor = ptAdd(anchor, Pt(400, -100))

	tb2 = TextBox(*anchor, *boxdims, anchoring="cc", hjustify="center", vcenter_fontszpx=vcenter_fontszpx)
	tb2.setBaseShape(RectRC().setRCRadiuses(14).setClass("caixas"))
	sc.addChild(tb2)
	tb2.getParagraph().setClass("tb1")
	tb2.setText("""Shèngsì
Shenzhen""")

	p1 = tb1.getAnchor()
	p2 = tb2.getAnchor()

	#la = Lna(Pta(*p1), Pta(*p2))
	la = Lna(p1, p2)
	print("la:", la)




	#sc.addChild(Circle(*tb1.getAnchor(), 30)).setStyle(Sty('stroke', '#DA6D1F', 'stroke-width', 6))
	#sc.addChild(Circle(*tb2.getAnchor(), 30)).setStyle(Sty('stroke', '#7D27EF', 'stroke-width', 6))

	lst_contour = tb1.getContour()
	got_X1 = None
	for k in lst_contour:
		lb = Lna(*k)
		intrsct = vec2_segment_intersect(*la, *lb)
		if not intrsct is None:
			got_X1 = intrsct


	lst_contour = tb2.getContour()
	print("lst_crnpts:", lst_contour)
	got_X2 = None
	for i, k in enumerate(lst_contour):
		lb = Lna(*k)

		intrsct = vec2_segment_intersect(*la, *lb)
		print(i, lb, 'X:', intrsct)
		if not intrsct is None:
			got_X2 = intrsct

	sc.addChild(Line(*got_X1, *got_X2).setStyle(Sty('stroke', '#DA6D1F', 'stroke-width', 6)))

	return sc


def _test_07X(capsys):

	with capsys.disabled():
	
		sc = generateX(False, '18pt', capsys)
		genFiles(inspect.currentframe().f_code.co_name, sc)

