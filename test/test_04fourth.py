

from rpcbSVG.Symbols import Arrow, Asterisk, CircArrow, CircAsterisk, CircRegPoly, CircStar, CircWedge, Crescent, Cross, CrossSight, Diamond, RegPoly, Square, Star, SuspPointCirc, SuspPointSquare, SuspPointTriang, Wedge, XSight, XSymb

from rpcbSVG.Basics import GLOBAL_ENV, Pt, circleDividers
from rpcbSVG.SVGStyleText import Sty
from rpcbSVG.SVGLib import Re, SVGContent, Text, Title, Use


def test_Symbols1():

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 2

	sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()
	sc.setBackground(Sty('fill', '#E7E8EA'))

	sc.addChild(Title("Symbol library test 1"))


	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(24,36,7), todefs=True)
	xsight_centerMarker = sc.addChild(XSight(36,36,10), todefs=True)
	xsymb = sc.addChild(XSymb(24,36), todefs=True)
	crosssight = sc.addChild(CrossSight(38,38, 6), todefs=True)
	crosssight_centerMarker = sc.addChild(CrossSight(38,38, 10), todefs=True)
	dsymb_cc = sc.addChild(Diamond(80,60, handle='cc'), todefs=True)
	dsymb_lc = sc.addChild(Diamond(30,80, handle='lc'), todefs=True)
	dsymb_rc = sc.addChild(Diamond(30,80, handle='rc'), todefs=True)
	dsymb_ct = sc.addChild(Diamond(80,30, handle='ct'), todefs=True)
	dsymb_cb = sc.addChild(Diamond(80,30, handle='cb'), todefs=True)
	crsymb_centerMarker = sc.addChild(Cross(10,10), todefs=True)
	crsymb_xs_centerMarker = sc.addChild(Cross(5,5), todefs=True)
	crsymb = sc.addChild(Cross(60,80), todefs=True)
	sqrsymb = sc.addChild(Square(60), todefs=True)
	asteri = sc.addChild(Asterisk(30), todefs=True)
	fan = sc.addChild(Asterisk(30, separation=14), todefs=True)
	circasteri = sc.addChild(CircAsterisk(22, 30), todefs=True)
	circfan = sc.addChild(CircAsterisk(22, 30, separation=10), todefs=True)
	arr = sc.addChild(Arrow(65, 30, 60, 30), todefs=True)
	arrlc = sc.addChild(Arrow(36, 12, 24, 14, handle='cb'), todefs=True)
	circarr = sc.addChild(CircArrow(58, 16, 38, 20, coffset=8), todefs=True)
	#
	# =========================================================================

	title_height = 140
	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 60, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Symbol library test 1")

	tstyle = Sty('fill', 'none', 'stroke', '#404040', 'font-size', 30, 'font-family', 'Helvetica', 'text-anchor', 'middle', 'stroke-width', 2)
	txstyle_small = Sty('fill', 'none', 'stroke', '#404040', 'font-size', 16, 'font-family', 'Monospace', 'text-anchor', 'middle', 'stroke-width', 2)
	txstyle_xsmall = Sty('fill', 'black', 'stroke', '#404040', 'font-size', 14, 'font-family', 'Monospace', 'text-anchor', 'middle', 'stroke-width', 2)
	symbstyle = Sty('fill', 'red', 'fill-opacity', 0.3, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round')

	def code_height_row1(p_topval):
		return p_topval + 75

	def label_height_row1(p_topval):
		return p_topval + 120

	left = 240
	hstep = 280
	vstep = 230

	top_row1 = 260

	top_row2 = top_row1 + vstep
	top_row3 = top_row1 + 2 * vstep
	top_row4 = top_row1 + 3 * vstep

	# -- X Sight -----------------------------------------------------------
	sc.addComment("Start 'X Sight'")

	thisleft = left
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), xsight.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("XSight(24,36,7)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("X Sight")

	# extra small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_xs_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End 'X Sight'")
	# =========================================================================


	# -- 'X' symbol -----------------------------------------------------------
	sc.addComment("Start 'X'")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), xsymb.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("XSymb(60,80)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("X")

	# small center crosssight
	sc.addChild(Use(Pt(thisleft,this_top), crosssight_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End 'X'")
	# =========================================================================

	
	# -- CrossSight ----------------------------------------------------------------
	sc.addComment("Start CrossSight")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), crosssight.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CrossSight(38,38, 6)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("CrossSight")

	# extra small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_xs_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End CrossSight")
	# =========================================================================

	# -- Cross ----------------------------------------------------------------
	sc.addComment("Start Cross")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), crsymb.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Cross(60,80)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Cross")

	# small center X sight
	sc.addChild(Use(Pt(thisleft,this_top), xsight_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Cross")
	# =========================================================================

	# -- Square -----------------------------------------------------------
	sc.addComment("Start Square")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), sqrsymb.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Square(60)")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Square")

	sc.addComment("End Square")
	# =========================================================================

	## SECOND ROW ####

	# -- Diamond cc -----------------------------------------------------------
	sc.addComment("Start Diamond CC")

	thisleft = left
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), dsymb_cc.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Diamond(80,60,handle='cc')")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Diamond")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Diamond CC")
	# =========================================================================

	# -- Diamond lc -----------------------------------------------------------
	sc.addComment("Start Diamond LC")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), dsymb_lc.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_xsmall).\
		setText("Diamond(30,80,handle='lc')")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Diamond LC")
	# =========================================================================

	# -- Diamond rc -----------------------------------------------------------
	sc.addComment("Start Diamond RC")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), dsymb_rc.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_xsmall).\
		setText("Diamond(30,80,handle='rc')")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Diamond RC")
	# =========================================================================

	sc.addChild(Text(thisleft + (hstep/2),label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Different diamond placements")

	# -- Diamond ct -----------------------------------------------------------
	sc.addComment("Start Diamond CT")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), dsymb_ct.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_xsmall).\
		setText("Diamond(80,30, handle='ct')")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Diamond CT")
	# =========================================================================

	# -- Diamond cb -----------------------------------------------------------
	sc.addComment("Start Diamond CB")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), dsymb_cb.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_xsmall).\
		setText("Diamond(80,30, handle='cb')")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Diamond CB")
	# =========================================================================

	## third ROW ####

	# -- Asterisk -----------------------------------------------------------
	sc.addComment("Start Asterisk")

	thisleft = left + hstep / 2
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), asteri.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Asterisk(60)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Asterisk")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Asterisk")
	# =========================================================================

	# -- Fan -----------------------------------------------------------
	sc.addComment("Start Fan")

	thisleft = thisleft + hstep
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), fan.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Asterisk(60,14)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Fan")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Fan")
	# =========================================================================

	# -- Circled Asterisk -----------------------------------------------------------
	sc.addComment("Start Circled Asterisk")

	thisleft = thisleft + hstep
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), circasteri.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircAsterisk(22,30)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled Asterisk")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Asterisk")
	# =========================================================================

	# -- Circled Fan -----------------------------------------------------------
	sc.addComment("Start Circled Fan")

	thisleft = thisleft + hstep
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), circfan.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircAsterisk(22,30,10)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled Fan")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Fan")
	# =========================================================================

	## FOURTH ROW ### 

	# -- Arrow ----------------------------------------------------------------
	sc.addComment("Start Arrow")

	thisleft = left  + 0.5 * hstep
	# thisleft = thisleft + hstep
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), arr.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Arrow(65,30,60,30)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Arrow")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Arrow")
	# =========================================================================

	# -- Arrow CB -------------------------------------------------------------
	sc.addComment("Start Arrow CB")

	#thisleft = left
	thisleft = thisleft + 1.5 * hstep
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), arrlc.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Arrow(36,12,24,14,handle='cb')")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Arrow CB")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Arrow CB")
	# =========================================================================

	# -- Circled Arrow ----------------------------------------------------------------
	sc.addComment("Start Circled Arrow")

	# thisleft = left
	thisleft = thisleft + 1.5 * hstep
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), circarr.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircArrow(58,16,38,20,8)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled Arrow")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Arrow")
	# =========================================================================

	with open('outtest/test_Symbols1.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))


def genSymbols2(yinvert):

	# Coordinates rounded to 1 dec.place
	# GLOBAL_ENV["ROUND"]["places"] = 2

	sc = SVGContent(Re(0,0,1600,1200), yinvert=yinvert).setIdentityViewbox()
	sc.setBackground(Sty('fill', '#E7E8EA'))

	sc.addChild(Title("Symbol library test 2"))

	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	crsymb_centerMarker = sc.addChild(Cross(10,10), todefs=True)
	#crosssight_centerMarker = sc.addChild(CrossSight(38,38, 10), todefs=True)
	xsight_centerMarker = sc.addChild(XSight(26,26, 8), todefs=True)
	tri = sc.addChild(Wedge(40,46), todefs=True)
	circtri = sc.addChild(CircWedge(32,32,coffset=5), todefs=True)
	wedge = sc.addChild(Wedge(40,46,indent=10), todefs=True)
	circwedge = sc.addChild(CircWedge(40,46,indent=10,coffset=5), todefs=True)
	cresc = sc.addChild(Crescent(32), todefs=True)
	susppt1 = sc.addChild(SuspPointCirc(32), todefs=True)
	susppt2 = sc.addChild(SuspPointSquare(40), todefs=True)
	susppt3 = sc.addChild(SuspPointTriang(40), todefs=True)
	star1 = sc.addChild(Star(32, 24, 5), todefs=True)
	star2 = sc.addChild(Star(32, 24, 8, rot=22.5), todefs=True)
	cstar = sc.addChild(CircStar(30, 14, 10, coffset=7), todefs=True)
	penta = sc.addChild(RegPoly(32, 5), todefs=True)
	hexa = sc.addChild(RegPoly(32,6, rot=20), todefs=True)
	sun = sc.addChild(CircAsterisk(38, 22, separation=30), todefs=True)
	cpenta = sc.addChild(CircRegPoly(32, 5, coffset=7), todefs=True)
	chept = sc.addChild(CircRegPoly(38,8, rot=9, coffset=-14), todefs=True)


	#
	# =========================================================================

	title_height = 140
	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 60, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Symbol library test 2")

	tstyle = Sty('fill', 'none', 'stroke', '#404040', 'font-size', 30, 'font-family', 'Helvetica', 'text-anchor', 'middle', 'stroke-width', 2)
	txstyle_small = Sty('fill', 'none', 'stroke', '#404040', 'font-size', 16, 'font-family', 'Monospace', 'text-anchor', 'middle', 'stroke-width', 2)
	# txstyle_xsmall = Sty('fill', 'black', 'stroke', '#404040', 'font-size', 14, 'font-family', 'Monospace', 'text-anchor', 'middle', 'stroke-width', 2)
	symbstyle = Sty('fill', 'red', 'fill-opacity', 0.5, 'stroke', 'red', 'stroke-width', 3, 'stroke-linejoin', 'round')

	def code_height_row1(p_topval):
		return p_topval + 75

	def label_height_row1(p_topval):
		return p_topval + 120

	left = 320
	hstep = 280
	vstep = 230

	top_row1 = 280

	top_row2 = top_row1 + vstep
	top_row3 = top_row1 + 2 * vstep
	top_row4 = top_row1 + 3 * vstep


	# -- Triangle -----------------------------------------------------------
	sc.addComment("Start Triangle")

	thisleft = left
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), tri.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Wedge(40,46)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Triangle")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Triangle")
	# =========================================================================

	# -- Circled Triangle -----------------------------------------------------------
	sc.addComment("Start Circled Triangle")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), circtri.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircWedge(32,32,5)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled Triangle")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Triangle")
	# =========================================================================

	# -- Circled Triangle -----------------------------------------------------------
	sc.addComment("Start Wedge")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), wedge.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Wedge(40,46,10)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Wedge")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Wedge")
	# =========================================================================

	# -- Circled Wedge -----------------------------------------------------------
	sc.addComment("Start Circled Wedge")

	thisleft = thisleft + hstep
	this_top = top_row1

	us = sc.addChild(Use(Pt(thisleft,this_top), circwedge.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircWedge(40,46,indent=10,coffset=5)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled Wedge")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Wedge")
	# =========================================================================
	
	# -- Crescent -------------------------------------------------------------
	sc.addComment("Start Crescent")

	thisleft = left
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), cresc.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Crescent(32)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Crescent")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Crescent")
	# =========================================================================
	
	# -- Suspension point 1 ---------------------------------------------------
	sc.addComment("Start Suspension point 1")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), susppt1.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("SuspPointCirc(32)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Suspension 1")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), xsight_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Suspension point 1")
	# =========================================================================
	
	# -- Suspension point 2 ---------------------------------------------------
	sc.addComment("Start Suspension point 2")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), susppt2.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("SuspPointSquare(40)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Suspension 2")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), xsight_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Suspension point 2")
	# =========================================================================
	
	# -- Suspension point 3 ---------------------------------------------------
	sc.addComment("Start Suspension point 3")

	thisleft = thisleft + hstep
	this_top = top_row2

	us = sc.addChild(Use(Pt(thisleft,this_top), susppt3.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("SuspPointTriang(40)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Suspension 3")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), xsight_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Suspension point 3")
	# =========================================================================
	
	## ROW 3

	# -- Sun -----------------------------------------------------------
	sc.addComment("Start Sun")

	thisleft = left
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), sun.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircAsterisk(38,22,30)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Sun")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Sun")
	# =========================================================================

	# -- Star 1  ---------------------------------------------------
	sc.addComment("Start Star 1")

	thisleft = thisleft + hstep
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), star1.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Star(32,24,5)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Star 1")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Star 1")
	# =========================================================================

	# -- Star 2 ---------------------------------------------------
	sc.addComment("Start Star 2")

	thisleft = thisleft + hstep
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), star2.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("Star(32,24,8,rot=22.5)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Star 2")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Star")
	# =========================================================================

	# -- Circled Star ---------------------------------------------------
	sc.addComment("Start Circled Star")

	thisleft = thisleft + hstep
	this_top = top_row3

	us = sc.addChild(Use(Pt(thisleft,this_top), cstar.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircStar(30,14,10,coffset=7)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled Star")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Star")
	# =========================================================================

	## ROW 4

	# -- Pentagon ---------------------------------------------------
	sc.addComment("Start Pentagon")

	thisleft = left
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), penta.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("RegPoly(32, 5)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Pentagon")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Pentagon")
	# =========================================================================

	# -- Hexagon ---------------------------------------------------
	sc.addComment("Start Hexagon")

	thisleft = thisleft + hstep
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), hexa.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("RegPoly(32,6,rot=20)")

	sc.addChild(Text(thisleft,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Hexagon")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Hexagon")
	# =========================================================================

	# -- Circled Pentagon ---------------------------------------------------
	sc.addComment("Start Circled Pentagon")

	thisleft = thisleft + hstep
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), cpenta.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top)-16)).\
		setStyle(txstyle_small).\
		setText("CircRegPoly(32,5,coffset=7)")

	sc.addChild(Text(thisleft + hstep/2,label_height_row1(this_top))).\
		setStyle(tstyle).\
		setText("Circled regular polygons")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Pentagon")
	# =========================================================================

	# -- Circled Octagon ---------------------------------------------------
	sc.addComment("Start Circled Octagon")

	thisleft = thisleft + hstep
	this_top = top_row4

	us = sc.addChild(Use(Pt(thisleft,this_top), chept.getSel()).setStyle(symbstyle))

	sc.addChild(Text(thisleft,code_height_row1(this_top))).\
		setStyle(txstyle_small).\
		setText("CircRegPoly(38,8,rot=9,coffset=-14)")

	# sc.addChild(Text(thisleft,label_height_row1(this_top))).\
	# 	setStyle(tstyle).\
	# 	setText("Octagon")

	# small center cross
	sc.addChild(Use(Pt(thisleft,this_top), crsymb_centerMarker.getSel()).setStyle(Sty('stroke', 'black')))

	sc.addComment("End Circled Octagon")
	# =========================================================================


	if yinvert:
		fname = 'outtest/test_Symbols2_yinv.svg'
	else:
		fname = 'outtest/test_Symbols2.svg'


	with open(fname, 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))


def test_Symbols2(capsys):

	with capsys.disabled():

		genSymbols2(False)
		genSymbols2(True)


# 	with capsys.disabled():

# 		#sc = SVGContent(Re(0,0,1600,1200))
# 		sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
# 		sc.setBackground(Sty('fill', '#E9E9E9'))

# 	with open('outtest/test_x.svg', 'w') as fl:
# 		fl.write(sc.toString(pretty_print=True, inc_declaration=True))


# def test_X(capsys):

# 	with capsys.disabled():
# 		print("\n")
# 		for i, pt in enumerate(circleDividers(Pt(10,8), 100, 4, 0)):
# 			print(i,pt)