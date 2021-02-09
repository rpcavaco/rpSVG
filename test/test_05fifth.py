
from rpcbSVG.Symbols import Arrow, Asterisk, CircArrow, CircAsterisk, CircRegPoly, CircStar, CircWedge, Crescent, Cross, CrossSight, Diamond, RegPoly, Square, Star, SuspPointCirc, SuspPointSquare, SuspPointTriang, Wedge, XSight, XSymb

from rpcbSVG.Basics import GLOBAL_ENV, Pt, circleDividers
from rpcbSVG.SVGStyleText import Sty
from rpcbSVG.SVGLib import Re, SVGContent, Text, TextBoxA, Title, Use


def test_Diagramming():

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=True).setIdentityViewbox()
	sc.setBackground(Sty('fill', '#E7E8EA'))

	sc.addChild(Title("Diagramming elements"))


	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	#
	# =========================================================================

	title_height = 1060
	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 60, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Diagramming elements")

	tstyle = Sty('fill', 'none', 'stroke', '#404040', 'font-size', 30, 'font-family', 'Helvetica', 'text-anchor', 'middle', 'stroke-width', 2)
	txstyle_small = Sty('fill', 'none', 'stroke', '#404040', 'font-size', 16, 'font-family', 'Monospace', 'text-anchor', 'middle', 'stroke-width', 2)
	# txstyle_xsmall = Sty('fill', 'black', 'stroke', '#404040', 'font-size', 14, 'font-family', 'Monospace', 'text-anchor', 'middle', 'stroke-width', 2)
	symbstyle = Sty('stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round')

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



	tb = sc.addChild(TextBoxA(240, 490, 500, 380).setStyle(Sty('stroke', 'black')))
	tb.setText("""O condutor individual não tem essa percepção imaginando que, de forma irrealista, 
	se lhe fosse dado um corredor livre poderia ultrapassar todos os outros automobilistas e, finalmente liberto, chegar atempadamente e com total conforto ao seu destino. 
Assim, quando lhe surge a visão de um corredor ciclável, a "miragem do canal livre" toma forma e a tentação de o invadir torna-se irresistível. Se não contrariássemos essa tentação, nem o trânsito andaria melhor nem os novos ciclistas teriam a proteção que merecem e que a cidade procura dar-lhes.""")


	with open('outtest/test_Diagramming.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))
