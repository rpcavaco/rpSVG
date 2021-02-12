
import cairosvg

from rpcbSVG.Symbols import Arrow, Asterisk, CircArrow, CircAsterisk, CircRegPoly, CircStar, CircWedge, Crescent, Cross, CrossSight, Diamond, RegPoly, Square, Star, SuspPointCirc, SuspPointSquare, SuspPointTriang, Wedge, XSight, XSymb

from rpcbSVG.Basics import GLOBAL_ENV, Pt, circleDividers
from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.SVGLib import Circle, Line, Re, SVGContent, Text, TextBoxA, TextParagraph, Title, Use

LARGE_TEXT = """O condutor individual não tem essa 
percepção imaginando que, de forma 
irrealista, se lhe fosse dado um corredor livre 
poderia ultrapassar todos os outros 
automobilistas e, finalmente liberto, chegar 
atempadamente e com total conforto ao 
seu destino."""

# with p_capsys.disabled():

def genTxBoxParagraph(p_ynvert, p_textjustify, p_capsys):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	sc.addChild(Title("Textbox and paragraph"))

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', '14pt', 'font-family', 'Helvetica', selector='.tb1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('stroke', 'blue', 'stroke-width', 3, selector='.aid1'))
	sc.addStyleRule(CSSSty('fill', 'blue', 'font-size', 28, 'font-family', 'Helvetica', selector='.lbls'))

	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(36,22,8), todefs=True, noyinvert=True)
	#
	# =========================================================================

	if sc.getYInvertFlag():
		title_height = 1060
	else:
		title_height = 140

	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 60, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Textbox and paragraph")

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
		tb1Y = 960
	else:
		tb1Y = 240

	left = 140
	vstep = 280
	hstep = 480
	boxwidth = 390
	boxheight = 180
	boxdims = (boxwidth, boxheight)
	label_offset = 20

	def lbly(p_sc, p_top, p_lbloffset):
		if p_sc.getYInvertFlag():
			lbly = p_top + p_lbloffset
		else:
			lbly = p_top - p_lbloffset
		return lbly

	def boxinsertion(p_nome_interno, p_label, p_lblanchor, p_anchor, p_tbanchoring, p_boxdims, p_text_just):
		sc.addComment(f"Start {p_nome_interno}")

		sc.addChild(Text(*p_lblanchor)).\
			setClass('lbls').\
			setText(p_label)

		sc.addChild(Use(p_anchor, xsight.getSel()).setClass('aid1'))

		
		tb = sc.addChild(TextBoxA(*p_anchor, *p_boxdims, anchor=p_tbanchoring, tjustify=p_text_just))
		tb.getParagraph().setClass("tb1")
		tb.getRect().setClass("caixas")
		tb.setText(LARGE_TEXT)

		sc.addComment(f"End {p_nome_interno}")


	# # =========================================================================

	thisleft = left		
	top = tb1Y
	boxy = top

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBoxA LT", "Left - Top anchoring", lbl_anchor, anchor, 'lt', boxdims, p_textjustify)

	# # =========================================================================
	thisleft = left		
	if sc.getYInvertFlag():
		top = top - vstep
	else:
		top = top + vstep
	boxy = top

	anchor = Pt(thisleft+boxwidth/2, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBoxA CT", "Center - Top anchoring", lbl_anchor, anchor, 'ct', boxdims, p_textjustify)

	# # =========================================================================
	thisleft = left		
	if sc.getYInvertFlag():
		top = top - vstep
	else:
		top = top + vstep
	boxy = top

	anchor = Pt(thisleft+boxwidth, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBoxA RT", "Right - Top anchoring", lbl_anchor, anchor, 'rt', boxdims, p_textjustify)

	# # =========================================================================
	thisleft = left	+ hstep	
	top = tb1Y
	boxy = top

	if sc.getYInvertFlag():
		anchor = Pt(thisleft, boxy-boxheight/2)
	else:
		anchor = Pt(thisleft, boxy+boxheight/2)
		
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBoxA LC", "Left - Center anchoring", lbl_anchor, anchor, 'lc', boxdims, p_textjustify)

	# # =========================================================================
	thisleft = left	+ hstep	
	if sc.getYInvertFlag():
		top = top - vstep
		boxy = top-boxheight/2
	else:
		top = top + vstep
		boxy = top+boxheight/2

	anchor = Pt(thisleft+boxwidth/2, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion("TextBoxA CC", "Center - Center anchoring", lbl_anchor, anchor, 'cc', boxdims, p_textjustify)

	# # =========================================================================
	nome = "TextBoxA RC"
	sc.addComment(f"Start {nome}")

	thisleft = left	+ hstep	
	if sc.getYInvertFlag():
		top = top - vstep
		boxy = top-boxheight/2
	else:
		top = top + vstep
		boxy = top+boxheight/2

	anchor = Pt(thisleft+boxwidth, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion(nome, "Right - Center anchoring", lbl_anchor, anchor, 'rc', boxdims, p_textjustify)

	# # =========================================================================
	nome = "TextBoxA LB"

	thisleft = left	+ 2 * hstep	
	top = tb1Y
	if sc.getYInvertFlag():
		boxy = top-boxheight
	else:
		boxy = top+boxheight

	anchor = Pt(thisleft, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion(nome, "Left - Bottom anchoring", lbl_anchor, anchor, 'lb', boxdims, p_textjustify)

	# # =========================================================================
	nome = "TextBoxA CB"

	thisleft = left	+ 2 * hstep	
	if sc.getYInvertFlag():
		top = top - vstep
		boxy = top-boxheight
	else:
		top = top + vstep
		boxy = top+boxheight

	anchor = Pt(thisleft+boxwidth/2, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion(nome, "Center - Bottom anchoring", lbl_anchor, anchor, 'cb', boxdims, p_textjustify)

	# # =========================================================================
	nome = "TextBoxA RB"

	thisleft = left	+ 2 * hstep	
	if sc.getYInvertFlag():
		top = top - vstep
		boxy = top-boxheight
	else:
		top = top + vstep
		boxy = top+boxheight

	anchor = Pt(thisleft+boxwidth, boxy)
	lbl_anchor = (thisleft,lbly(sc, top, label_offset))

	boxinsertion(nome, "Right - Bottom anchoring", lbl_anchor, anchor, 'rb', boxdims, p_textjustify)

	return sc

def test_TxBoxParagraph_YInvert():

	sc = genTxBoxParagraph(True, "left", None)

	with open('outtest/test_TxBoxParagraph_YInvert.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_TxBoxParagraph_YInvert.png")

def test_TxBoxParagraph():

	sc = genTxBoxParagraph(False, "left", None)

	with open('outtest/test_TxBoxParagraph.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_TxBoxParagraph.png")

def test_TxBoxParagraph_YInvertCenterJust():

	sc = genTxBoxParagraph(True, "center", None)

	with open('outtest/test_TxBoxParagraph_YInvertCenterJust.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_TxBoxParagraph_YInvertCenterJust.png")

def test_TxBoxParagraph_CenterJust():

	sc = genTxBoxParagraph(False, "center", None)

	with open('outtest/test_TxBoxParagraph_CenterJust.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_TxBoxParagraph_CenterJust.png")

def test_TxBoxParagraph_YInvertRightJust():

	sc = genTxBoxParagraph(True, "right", None)

	with open('outtest/test_TxBoxParagraph_YInvertRightJust.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_TxBoxParagraph_YInvertRightJust.png")

def test_TxBoxParagraph_RightJust():

	sc = genTxBoxParagraph(False, "right", None)

	with open('outtest/test_TxBoxParagraph_RightJust.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_TxBoxParagraph_RightJust.png")
