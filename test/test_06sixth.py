


import inspect

import pytest
from test.testing import genFiles
import cairosvg

from rpcbSVG.Symbols import Cross, Cylinder, Diamond, Server, XSight

from rpcbSVG.Basics import GLOBAL_ENV, Pt
from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.SVGLib import Circle, Re, RectRC, SVGContent, Text, Title, Use
from rpcbSVG.Constructs import TextBox

SMALLTXT2 = """Ürümqi
Yiwu"""

SMALLTXT3 = """Ürümqi
Yiwu
Shèngsì"""

SMALLTXT4 = """Ürümqi
Yiwu
Shèngsì
Shenzhen"""

SMALLTXT1 = "Ürümqi"

SMALLTXT5 = """Ürümqi
Yiwu
Shèngsì
Shenzhen
Gaozhou"""

def genTxBoxParagraph(p_ynvert, p_vcenter_fontszpx, p_capsys):

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
	sc.addStyleRule(CSSSty('stroke', '#5E5E5E', 'stroke-width', 4, 'stroke-linejoin', 'round', selector='.symbinnerstroke'))

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
		mainlabel = "Textbox, multiline and various shapes (y-inverted) - text centered"
	else:
		mainlabel = "Textbox, multiline and various shapes - text centered"

	sc.addChild(Title(mainlabel))


	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 40, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText(mainlabel)

	def code_height_row1(p_topval):
		return p_topval + 75

	def label_height_row1(p_topval):
		return p_topval + 120

	left = 240
	hstep = 280
	vstep = 230

	top_row1 = 260
	title_height = 1060

	top_row2 = top_row1 + vstep
	top_row3 = top_row1 + 2 * vstep
	top_row4 = top_row1 + 3 * vstep

	if sc.getYInvertFlag():
		tb1Y = 1000
	else:
		tb1Y = 200

	left = 140
	vstep = 190
	hstep = 270
	boxwidth = 170
	boxheight = 90
	boxdims = (boxwidth, boxheight)
	label_offset = -10
	left_offset = 10
	vert_offset = 90

	def lbly(p_sc, p_top, p_lbloffset):
		if p_sc.getYInvertFlag():
			lbly = p_top + p_lbloffset
		else:
			lbly = p_top - p_lbloffset
		return lbly

	def boxinsertion(p_nome_interno, p_label, p_lblanchor, p_anchor, p_tbanchoring, p_boxdims, p_text_just, p_paddingv, p_shape, txt=None):
		
		sc.addComment(f"Start {p_nome_interno}")

		# sc.addChild(Use(Pt(*p_anchor), crsymb_centerMarker.getSel()).setClass('aid1'))

		if len(p_label) > 0:
			sc.addChild(Text(*p_lblanchor)).\
				setClass('lbls').\
				setText(p_label)

		sc.addChild(Use(p_anchor, xsight.getSel()).setClass('aid1'))

		tb = TextBox(*p_anchor, *p_boxdims, anchor=p_tbanchoring, hjustify=p_text_just, paddingv=p_paddingv, vcenter_fontszpx=vcenter_fontszpx)
		if p_shape == "rc":
			tb.setBaseShape(RectRC().setRCRadiuses(14).setClass("caixas"))
		elif p_shape == "circ":
			tb.setBaseShape(Circle().setClass("caixas"))
		elif p_shape == "dia":
			tb.setBaseShape(Diamond().setClass("caixas"))
		elif p_shape == "cyl":
			tb.setBaseShape(Cylinder(0,0,pitch_ratio=0.3))
		elif p_shape == "srv":
		 	tb.setBaseShape(Server(0,0,0, rotation=18, projangle=145))

		if not txt is None:
			sc.addChild(tb)
			tb.getParagraph().setClass("tb1")
			tb.setText(txt)

		sc.addComment(f"End {p_nome_interno}")

	# # =========================================================================

	thisleft = left + left_offset + boxwidth/2
	top = tb1Y
	boxy = top
	rc_boxdims = (boxdims[0], 1.5*boxdims[1])

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox RC", "Rounded corners", lbl_anchor, anchor, 'cc', boxdims, "center", 88, "rc",  txt=SMALLTXT1)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox CircC", "Circular", lbl_anchor, anchor, 'cc', (boxdims[1], boxdims[1]), "center", 30, "circ",  txt=SMALLTXT1)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox Diamond", "Diamond", lbl_anchor, anchor, 'cc',  (boxdims[0], boxdims[1]), "center", 140, "dia",  txt=SMALLTXT1)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox DB", "Database", lbl_anchor, anchor, 'cc', (boxdims[0], 0.8*boxdims[1]), "center", 140, "cyl",  txt=SMALLTXT1)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox SRV", "Server", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "srv",  txt=SMALLTXT1)

	# # =========================================================================
	#   NEXT Line
	# # =========================================================================
	# # =========================================================================


	thisleft = left + left_offset + boxwidth/2
	top = top + vstep - 40
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox RC", "", lbl_anchor, anchor, 'cc', boxdims, "center", 88, "rc",  txt=SMALLTXT2)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox CircC", "", lbl_anchor, anchor, 'cc', boxdims, "center", 30, "circ",  txt=SMALLTXT2)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox Diamond", "", lbl_anchor, anchor, 'cc', (220,140), "center", 140, "dia",  txt=SMALLTXT2)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox DB", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "cyl",  txt=SMALLTXT2)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox SRV", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "srv",  txt=SMALLTXT2)


	# # =========================================================================
	#   NEXT Line
	# # =========================================================================
	# # =========================================================================


	thisleft = left + left_offset + boxwidth/2
	top = top + vstep
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox RC", "", lbl_anchor, anchor, 'cc', rc_boxdims, "center", 88, "rc",  txt=SMALLTXT3)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox CircC", "", lbl_anchor, anchor, 'cc', boxdims, "center", 30, "circ",  txt=SMALLTXT3)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox Diamond", "", lbl_anchor, anchor, 'cc', (220,140), "center", 140, "dia",  txt=SMALLTXT3)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox DB", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "cyl",  txt=SMALLTXT3)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox SRV", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "srv",  txt=SMALLTXT3)

	# # =========================================================================
	#   NEXT Line
	# # =========================================================================
	# # =========================================================================


	thisleft = left + left_offset + boxwidth/2
	top = top + vstep
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox RC", "", lbl_anchor, anchor, 'cc', rc_boxdims, "center", 88, "rc",  txt=SMALLTXT4)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox CircC", "", lbl_anchor, anchor, 'cc', boxdims, "center", 30, "circ",  txt=SMALLTXT4)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox Diamond", "", lbl_anchor, anchor, 'cc', (220,140), "center", 140, "dia",  txt=SMALLTXT4)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox DB", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "cyl",  txt=SMALLTXT4)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox SRV", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "srv",  txt=SMALLTXT4)

	# # =========================================================================
	#   NEXT Line
	# # =========================================================================
	# # =========================================================================


	thisleft = left + left_offset + boxwidth/2
	top = top + vstep
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox RC", "", lbl_anchor, anchor, 'cc', rc_boxdims, "center", 88, "rc",  txt=SMALLTXT5)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox CircC", "", lbl_anchor, anchor, 'cc', boxdims, "center", 30, "circ",  txt=SMALLTXT5)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox Diamond", "", lbl_anchor, anchor, 'cc', (220,140), "center", 140, "dia",  txt=SMALLTXT5)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox DB", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "cyl",  txt=SMALLTXT5)

	# # =========================================================================

	thisleft = thisleft + hstep	
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox SRV", "", lbl_anchor, anchor, 'cc', boxdims, "center", 140, "srv",  txt=SMALLTXT5)

	return sc

	genFiles(inspect.currentframe().f_code.co_name, sc)

@pytest.mark.textbox
def test_06TextBoxMultilineShapesSmall(capsys):
	with capsys.disabled():
		
		sc = genTxBoxParagraph(False, '12pt', capsys)
		genFiles(inspect.currentframe().f_code.co_name, sc)

@pytest.mark.textbox
def test_06TextBoxMultilineShapesSmallYI(capsys):
	with capsys.disabled():
		
		sc = genTxBoxParagraph(False, '12pt', capsys)
		genFiles(inspect.currentframe().f_code.co_name, sc)

@pytest.mark.textbox
def test_06TextBoxMultilineShapesNormal(capsys):
	with capsys.disabled():
		
		sc = genTxBoxParagraph(False, '16pt', capsys)
		genFiles(inspect.currentframe().f_code.co_name, sc)

@pytest.mark.textbox
def test_06TextBoxMultilineShapesNormalYI(capsys):
	with capsys.disabled():
		
		sc = genTxBoxParagraph(False, '16pt', capsys)
		genFiles(inspect.currentframe().f_code.co_name, sc)
