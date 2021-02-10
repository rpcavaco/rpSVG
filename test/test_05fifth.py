
import cairosvg

from rpcbSVG.Symbols import Arrow, Asterisk, CircArrow, CircAsterisk, CircRegPoly, CircStar, CircWedge, Crescent, Cross, CrossSight, Diamond, RegPoly, Square, Star, SuspPointCirc, SuspPointSquare, SuspPointTriang, Wedge, XSight, XSymb

from rpcbSVG.Basics import GLOBAL_ENV, Pt, circleDividers
from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.SVGLib import Line, Re, SVGContent, Text, TextBoxA, Title, Use


def test_Diagramming(capsys):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	if True:
		sc = SVGContent(Re(0,0,1600,1200), yinvert=True).setIdentityViewbox()
	else:
		sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	sc.addChild(Title("Diagramming elements"))


	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	#
	# =========================================================================

	if sc.getYInvertFlag():
		title_height = 1060
	else:
		title_height = 140

	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 60, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Diagramming elements")

	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', 20, 'font-family', 'Helvetica', selector='.tb1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('stroke', '#E1E1E8', 'stroke-width', 2, selector='.aid1'))

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


	# # -- Triangle -----------------------------------------------------------
	# sc.addComment("Start Triangle")

	# thisleft = left
	# this_top = top_row1

	# us = sc.addChild(Use(Pt(thisleft,this_top), tri.getSel()).setStyle(symbstyle))

	# sc.addChild(Text(thisleft,code_height_row1(this_top))).\
	# 	setStyle(txstyle_small).\
	# 	setText("Wedge(40,46)")

	# sc.addChild(Text(thisleft,label_height_row1(this_top))).\
	# 	setStyle(tstyle).\
	# 	setText("Triangle")

	# # small center cross
	# sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	# sc.addComment("End Triangle")
	# # =========================================================================

	if sc.getYInvertFlag():
		tb1Y = 1000
	else:
		tb1Y = 200


	with capsys.disabled():

		tb = sc.addChild(TextBoxA(240, tb1Y, 500, 150))
		tb.getParagraph().setClass("tb1")
		tb.getRect().setClass("caixas")
		tb.setText("""O condutor individual não tem essa percepção 
		imaginando que, de forma irrealista, se lhe fosse dado 
		um corredor livre poderia ultrapassar todos os outros 
		automobilistas e, finalmente liberto, chegar 
		atempadamente e com total conforto ao seu destino.""")

		sc.addChild(Line(80,1100,240,tb1Y).setClass('aid1'))


	with open('outtest/test_Diagramming.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

	cairosvg.svg2png(bytestring=sc.toBytes(pretty_print=True, inc_declaration=True), write_to="outtest/test_Diagramming.png")

