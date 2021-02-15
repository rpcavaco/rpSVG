


import cairosvg

from rpcbSVG.Symbols import Cross, Diamond, XSight

from rpcbSVG.Basics import GLOBAL_ENV, Pt
from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.SVGLib import Circle, Re, RectRC, SVGContent, Text, Title, Use
from rpcbSVG.Constructs import TextBox

SMALLTXT = """Ürümqi
Yiwu"""

SMALLTXT = """Ürümqi
Yiwu
Shèngsì"""

SMALLTXT1 = "Ürümqi"

def genTxBoxParagraph(p_ynvert, p_textjustify, p_capsys):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', '12pt', 'font-family', 'Helvetica', selector='.tb1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('stroke', 'black', 'stroke-width', 1, selector='.aid1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', '#404040', 'font-size', 28, 'font-family', 'Helvetica','stroke-width', 2, 'text-anchor', 'middle', selector='.lbls'))

	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.45, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfilldark'))
	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.3, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfillmed'))
	sc.addStyleRule(CSSSty('fill', 'red', 'fill-opacity', 0.1, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round', selector='.symbfilllight'))
	sc.addStyleRule(CSSSty('stroke', '#5E5E5E', 'stroke-width', 4, 'stroke-linejoin', 'round', selector='.symbinnerstroke'))

	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(46,46,2), todefs=True, noyinvert=True)
	crsymb_centerMarker = sc.addChild(Cross(20,20), todefs=True)
	#
	# =========================================================================

	if sc.getYInvertFlag():
		title_height = 1060
	else:
		title_height = 140

	if p_ynvert:
		if p_textjustify == "right":
			mainlabel = "Textbox and paragraph (y-inverted) - text right justified"
		elif p_textjustify == "center":
			mainlabel = "Textbox and paragraph (y-inverted) - text centered"
		else:
			mainlabel = "Textbox and paragraph (y-inverted) - text left justified"
	else:
		if p_textjustify == "right":
			mainlabel = "Textbox and paragraph - text right justified"
		elif p_textjustify == "center":
			mainlabel = "Textbox and paragraph - text centered"
		else:
			mainlabel = "Textbox and paragraph - text left justified"

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
		tb1Y = 940
	else:
		tb1Y = 250

	left = 140
	vstep = 280
	hstep = 480
	boxwidth = 190
	boxheight = 110
	boxdims = (boxwidth, boxheight)
	label_offset = 40
	left_offset = 20
	vert_offset = 90

	def lbly(p_sc, p_top, p_lbloffset):
		if p_sc.getYInvertFlag():
			lbly = p_top + p_lbloffset
		else:
			lbly = p_top - p_lbloffset
		return lbly

	def boxinsertion(p_nome_interno, p_label, p_lblanchor, p_anchor, p_tbanchoring, p_boxdims, p_text_just, p_paddingv, p_shape):
		
		sc.addComment(f"Start {p_nome_interno}")

		# sc.addChild(Use(Pt(*p_anchor), crsymb_centerMarker.getSel()).setClass('aid1'))

		sc.addChild(Text(*p_lblanchor)).\
			setClass('lbls').\
			setText(p_label)

		sc.addChild(Use(p_anchor, xsight.getSel()).setClass('aid1'))

		tb = TextBox(*p_anchor, *p_boxdims, anchor=p_tbanchoring, hjustify=p_text_just, paddingv=p_paddingv, vcenter_fontszpx='12pt')
		if p_shape == "rc":
			tb.setBaseShape(RectRC().setRCRadiuses(14).setClass("caixas"))
		elif p_shape == "circ":
			tb.setBaseShape(Circle().setClass("caixas"))
		elif p_shape == "dia":
			tb.setBaseShape(Diamond().setClass("caixas"))

		#def __init__(self, width, height, x=0, y=0, handle='cc') -> None:			

		sc.addChild(tb)
		tb.getParagraph().setClass("tb1")
		tb.setText(SMALLTXT)

		sc.addComment(f"End {p_nome_interno}")

	# # =========================================================================

	thisleft = left + left_offset + boxwidth/2
	top = tb1Y
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox RC", "Rounded corners", lbl_anchor, anchor, 'cc', boxdims, "center", 88, "rc")

	# # =========================================================================

	thisleft = thisleft + hstep	
	top = tb1Y
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox CircC", "Circular", lbl_anchor, anchor, 'cc', boxdims, "center", 30, "circ")

	# # =========================================================================

	thisleft = thisleft + hstep	
	top = tb1Y
	boxy = top

	if sc.getYInvertFlag():
		boxy = top - vert_offset
	else:
		boxy = top + vert_offset

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBox Diamond", "Diamond", lbl_anchor, anchor, 'cc', (220,140), "center", 140, "dia")


	return sc


def test_X(capsys):
	with capsys.disabled():
		
		sc = genTxBoxParagraph(False, "left", capsys)

		with open('outtest/test_X.svg', 'w') as fl:
			fl.write(sc.toString(pretty_print=True, inc_declaration=True))

		cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_X.png")
