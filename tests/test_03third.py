


import cairosvg
import pytest, inspect

from os.path import exists, join as path_join

from tests.testing import genFiles

from rpSVG.Structs import VBox
from rpSVG.Basics import Pt, Rotate, pA, pC, pQ, pS, pT, polar2rectDegs, ptAdd, ptGetAngle
from rpSVG.SVGStyleText import CSSSty, Sty
from rpSVG.SVGLib import AnalyticalPath, Circle, Ellipse, GradientStop, Group, Image, Line, LinearGradient, Marker, MrkProps, Pattern, Polygon, Polyline, RadialGradient, Re, Rect, RectRC, SVGContent, TRef, TSpan, Text, TextParagraph, TextPath, Title, Use

#	with capsys.disabled():

def test_03Marker():

	def pttrans(p_pt, p_ang):
		return (p_pt, ptAdd(p_pt, polar2rectDegs(p_ang, 30)))

	sc = SVGContent(Re(0,0,1200,1000)).setIdentityViewbox()
	sc.addStyleRule(CSSSty('stroke', 'grey', 'stroke-width', 2, selector='.aids'))
	
	# Define markers =======================================================

	mrkattrs = (3.5,10,7, "auto")
	pol = Polygon().addPList( (Pt(10,0), Pt(10,7), Pt(0, 3.5)) )
	mr1 = sc.addChild(Marker(2,*mrkattrs), todefs=True)
	mr1.addChild(pol)
	pol.setStyle(Sty('fill', 'red'))
	
	mr2 = sc.addChild(Marker(8,*mrkattrs), todefs=True)
	gr = mr2.addChild(Group())
	gr.addChild(pol.clone().setStyle(Sty('fill', 'blue')))
	gr.addTransform(Rotate(180,5,3.5))

	# node vertices marker
	mr3 = sc.addChild(Marker(3,3,6,6, 0), todefs=True)
	c = mr3.addChild(Circle(3,3,2)).setStyle(Sty('fill', 'powderblue', 'fill-opacity', '0.8'))

	# End define markers ===================================================

	# Line

	pA = Pt(50,200)
	pB = Pt(600,800)

	ln = sc.addChild(Line(pA, pB, marker_props=MrkProps(marker_start=mr1.getId(), marker_end=mr2.getId())))
	ln.setStyle(Sty('stroke', 'green', 'stroke-width', 6))

	ang = ln.getStruct().getAngle() - 90

	# grey ticks
	sc.addChild(Line( *pttrans(pA, ang) ).setClass('aids'))
	sc.addChild(Line( *pttrans(pB, ang) ).setClass('aids'))

	pts = [
		Pt(220,100),
		Pt(240,260),
		Pt(290,330),
		Pt(590,440),
		Pt(840,610),
		Pt(900,800)
	]

	ang1 = ptGetAngle(pts[0],pts[1]) - 90
	ang2 = ptGetAngle(pts[4],pts[5]) - 90

	# Pline
	plg = sc.addChild(Polyline(  marker_props=MrkProps(marker_start=mr1.getId(), marker_mid=mr3.getId(), marker_end=mr2.getId())  ))
	plg.addPList(pts).setStyle(Sty('stroke', 'blue', 'stroke-width', 5))

	# grey ticks again
	sc.addChild(Line( *pttrans(pts[0], ang1) ).setClass('aids'))
	sc.addChild(Line( *pttrans(pts[5], ang2) ).setClass('aids'))

	genFiles(inspect.currentframe().f_code.co_name, sc)

def test_03Gradient():

	sc = SVGContent(Re(0,0,1600,1000)).setIdentityViewbox()

	gr1 = sc.addChild(LinearGradient().setId("the_grad"), todefs=True)   
	st1 = gr1.addChild(GradientStop("20%", "navy"))
	gr1.addChild(GradientStop("80%", "aqua"))
	gr1.addChild(GradientStop("95%", "blanchedalmond"))
	gr1.addChild(GradientStop("100%", "white"))

	assert st1.getStruct().getfields() == "offset,stop-color,stop-opacity"

	gr2 = sc.addChild(RadialGradient(1150,700,200,1150,700, None, 'userSpaceOnUse').setId("the_rgrad"), todefs=True)   
	gr2.addChild(GradientStop("0%", "mediumblue"))
	gr2.addChild(GradientStop("60%", "white"))
	gr2.addChild(GradientStop("80%", "white"))
	gr2.addChild(GradientStop("100%", "navy"))

	assert gr2.getStruct().getfields() == "cx,cy,r,fx,fy,{http://www.w3.org/1999/xlink}href,gradientUnits,spreadMethod,gradientTransform"

	sc.setBackground(Sty('fill', '#000029'))

	sc.addChild(RectRC(200,50,500,400,10,20)).setStyle(Sty('fill', 'url(#the_grad)', 'stroke', 'black'))
	
	sc.addChild(RectRC(850,500,600,400,10,20)).setStyle(Sty('fill', 'url(#the_rgrad)', 'stroke', 'black'))

	genFiles(inspect.currentframe().f_code.co_name, sc)

def test_03Text():

	plist= [
		Pt(100,900),
		Pt(280,990),
		Pt(460,820),
		Pt(640,930),
		Pt(820,890),
		Pt(1000,1100)
	]

	sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()

	# Not displayed on browsers, only on gnome viewers
	td = sc.addChild(Text(), todefs=True).setText("Gatos ao ataque")

	ap = sc.addChild(AnalyticalPath(), todefs=True)
	ap.addPolylinePList(plist)

	p = Pt(800,600)

	tx = sc.addChild(Text(*p))   
	tx.setStyle(Sty('fill', 'teal', 'font-size', 70, 'text-anchor', 'middle'))
	tx.setText("Aproveitar para fazer um ")

	# gliphs dont rotate on gnome implementation

	# Option 1 to rotate grlyphs, uglier
	#ts = tx.addChild(TSpan(None, None, None, None, -20).setStyle(Sty('fill', 'red')).setText("grande")  )

	ts = tx.addChild(TSpan().setStyle(Sty('fill', 'red')).setText("grande")  )
	assert ts.getStruct().getfields() == "x,y,dx,dy,rotate,textLength,lengthAdjust"
	
	# Option 2 to rotate grlyphs, prettier
	ts.setStructAttr("rotate", -20)

	ts.tailText(" anúncio")

	tx.addTransform(Rotate(45,*p))

	assert tx.getStruct().getfields() == "x,y,dx,dy,rotate,textLength,lengthAdjust"

	# browsers dont display this, gnome does
	tx2 = sc.addChild(Text(200,900))   
	tx2.setStyle(Sty('fill', 'green', 'font-size', 90))
	tx2.addChild(TRef(td.getId()))

	# along path - Gnome implementatio doesn't displays

	tx3 = sc.addChild(Text().setStructAttr("dy", 10))   
	tx3.setStyle(Sty('fill', '#6A5ACD', 'font-size', '30pt', 'font-family', 'Helvetica', 'text-anchor', 'middle'))
	tp = tx3.addChild(TextPath(ap.getId(), '48%'))
	tp.setText("Muito e muito texto espalhado ao longo deste caminho ...")

	us = sc.addChild(Use().setStyle(Sty('stroke', 'grey', 'stroke-width', 2, 'stroke-linejoin', 'round')))
	us.setHREFAttr(ap.getSel())

	genFiles(inspect.currentframe().f_code.co_name, sc)

def test_03Image():

	sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()

	path = path_join("assets", "test_image.jpg")
	assert exists(path)

	sc.addChild(Image(100,100,1400,916,path))

	genFiles(inspect.currentframe().f_code.co_name, sc)

def test_03YInvert():

	sc = SVGContent(Re(0,0,1600,1200), yinvert=True).setViewbox(VBox(0,40,1600,1200))
	sc.addStyleRule(CSSSty('stroke', '#E1E1E8', 'stroke-width', 2, selector='.aid1'))
	sc.addStyleRule(CSSSty('stroke', '#46474C', 'stroke-width', 2, selector='.aid2'))
	sc.addStyleRule(CSSSty('stroke', '#494949', 'fill', '#F68E4C', 'stroke-width', 2, selector='.uses'))

	sc.addChild(Title("Y Axis inversion test"))

	# Define markers =======================================================

	# Common items to both arrow terminators
	mrkattrs = (1.5, 5, 3, "auto")
	plist = (Pt(5,0), Pt(5,3), Pt(0, 1.5))

	# Start arrow terminator
	mr1 = sc.addChild(Marker(3,*mrkattrs), todefs=True)

	# Should not add points to Polygon prior to addChild if yinvert needed to be applied, wouldn't function properly. Warning is issued
	with pytest.warns(UserWarning):
		fakepol = mr1.addChild(Polygon().addPList(plist), noyinvert=False)

	# Correct way of adding points if yinversion was to be applied.
	# In fact we don't need it to be applied here in this case, but works properly 
	#  either you need, or don't need, to yinvert
	pol = mr1.addChild(Polygon(), noyinvert=True)
	pol.addPList(plist)
	pol.setStyle(Sty('fill', '#AED7FE'))

	# End arrow terminator -- noyinvert=True
	mr2 = sc.addChild(Marker(2,*mrkattrs), todefs=True)
	gr = mr2.addChild(Group())
	pol2 = gr.addChild(Polygon().setStyle(Sty('fill', '#313163')), noyinvert=True)
	pol2.addPList(plist)
	gr.addTransform(Rotate(180,2.5,1.5))

	# node vertices marker
	mr3 = sc.addChild(Marker(0.5,0.5,1,1, 0), todefs=True, noyinvert=True)
	mr3.addChild(Circle(0.5,0.5,0.5)).setStyle(Sty('fill', 'navyblue', 'fill-opacity', '0.8'))

	# End define markers ===================================================


	# Reference red rect to be "used" later, non y-inverted
	rsrc = sc.addChild(Rect(0, 0,60,60), todefs=True, noyinvert=True)

	gr1 = sc.addChild(LinearGradient(0, 1800, 0, -400, None, "userSpaceOnUse").setId("the_grad"), todefs=True)   
	gr1.addChild(GradientStop(0, "#303B8E", 1))
	gr1.addChild(GradientStop(1, "#DFE0EA", 1))

	plist= [
		Pt(570,860),
		Pt(640,670),
		Pt(700,740)
	]

	ap = sc.addChild(AnalyticalPath(
				marker_props=MrkProps(
					marker_start=mr1.getId(), 
					marker_mid=mr3.getId(),
					marker_end=mr2.getId()
				)
			).setStyle(Sty('stroke', 'white', 'stroke-width', 4)), todefs=True)
	ap.addPolylinePList(plist)

	ap.addCmd(pQ(760,810,820,670))
	ap.addCmd(pT(920,670))
	ap.addCmd(pC(940,750,1030,760,1050,690))
	ap.addCmd(pS(1150,690,1160,710))
	ap.addCmd(pA(80, 60, 32, 0,1, 1450, 450))
	ap.refresh()

	sc.setBackground(Sty('stroke', 'black', 'fill', 'url(#the_grad)'))

	# Guides pointing to end of polyline
	# sc.addChild(Line(570,860, 600, 890).setClass('aid1'))
	# sc.addChild(Line(1450, 450, 1490,420).setClass('aid2'))

	# Red rect "uses"

	sc.addChild(Text(70, 860)).\
		setStyle(Sty('fill', '#E9E9E9', 'font-size', 20, 'font-family', 'Helvetica')).\
		setText(f"y: 860")

	for col in range(3):
		x = 140 + col * 100
		for row in range(3):
			y = 860 - row * 90
			sc.addChild(Use(Pt(x,y), rsrc.getSel())).setClass('uses')


	r = sc.addChild(RectRC(120,60,300,480, 10, 10))
	r.setStyle(Sty('fill', '#3739E1'))

	sc.addChild(Text(70, 60)).\
		setStyle(Sty('fill', 'black', 'font-size', 20, 'font-family', 'Helvetica')).\
		setText("y: 60")

	title_height = 1050
	sc.addChild(Text(140,title_height)).\
		setStyle(Sty('fill', 'white', 'font-size', 80, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Y Axis inversion test")

	txtrows = [
		"Viewbox y is set as y=40,",
		"shifting the entire drawing",
		"down by 40 units."
	]

	sc.addChild(TextParagraph(1040, 950, txtrows).\
		setStyle(Sty('fill', 'white', 'font-size', 40, 'font-family', 'Helvetica')))

	sc.addChild(Text(70, title_height)).\
		setStyle(Sty('fill', '#E9E9E9', 'font-size', 20, 'font-family', 'Helvetica')).\
		setText(f"y: {title_height}")

	# sc.addChild(Line(200,1100,60,1100).setClass('aid1'))

	sc.addChild(Circle(750, 300, 240)).setStyle(Sty('stroke', 'dodgerblue', 'stroke-width', 6))
	sc.addChild(Ellipse(750, 300, 160, 220)).setStyle(Sty('stroke', '#0054A6', 'stroke-width', 2))

	sc.addChild(Text(750, 300)).\
		setStyle(Sty('fill', 'black', 'font-size', 20, 'font-family', 'Helvetica')).\
		setText("y: 300")

	sc.addChild(Line(650,300,740,300).setClass('aid2'))
	sc.addChild(Line(740,210,740,300).setClass('aid2'))

	path = path_join("assets", "test_image.jpg")
	sc.addChild(Image(1080,60, 420, 287,path))

	sc.addChild(Text(1020, 60)).\
		setStyle(Sty('fill', 'black', 'font-size', 20, 'font-family', 'Helvetica')).\
		setText("y: 60")

	r2 = sc.addChild(Rect(1080,60, 420, 287))
	r2.setStyle(Sty('stroke', '#494949'))

	us = sc.addChild(Use().setStyle(Sty('stroke', 'white', 'stroke-width', 2, 'stroke-linejoin', 'round')))
	us.setHREFAttr(ap.getSel())

	genFiles(inspect.currentframe().f_code.co_name, sc)

def test_03Comment():

	sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()

	sc.setBackground(Sty('stroke', 'black', 'fill', 'navy'))

	sc.addComment("Just a simple comment")

	sc.addChild(Line(100,100,1500,1100).setStyle(Sty('stroke', '#494949', 'stroke-width', 8)))

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="1600" height="1200" viewBox="0 0 1600 1200"><defs/><rect x="0" y="0" width="1600" height="1200" id="Rec0" fill="navy" stroke="black"/><!--Just a simple comment--><line x1="100" y1="100" x2="1500" y2="1100" fill="none" stroke="#494949" stroke-width="8" id="Lin1"/></svg>"""

def test_03Pattern():

	sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()
	sc.setBackground(Sty('fill', '#E7E8EA'))

	sc.addChild(Title("Pattern test"))


	patt = sc.addChild(Pattern(10,10,50,70, "userSpaceOnUse",'rotate(14)'), todefs=True)
	patt.addChild(Rect(5,5,10,10)).setStyle(Sty('fill', 'blue'))
	patt.addChild(Rect(20,5,10,10)).setStyle(Sty('fill', 'blue'))
	patt.addChild(Rect(31,5,6,10)).setStyle(Sty('fill', 'blue'))

	patt.addChild(Rect(5,20,10,10)).setStyle(Sty('fill', '#2567FF'))
	patt.addChild(Rect(5,35,10,10)).setStyle(Sty('fill', '#419EFF'))

	title_height = 200
	sc.addChild(Text(300,title_height)).\
		setStyle(Sty('fill', '#7C7C7C', 'font-size', 60, 'font-family', 'Helvetica', 'font-weight', 'bold')).\
		setText("Pattern test")

	sc.addChild(Rect(300,250,1000,800).setStyle(Sty('fill', 'white')))
	sc.addChild(Rect(300,250,1000,800).setStyle(Sty('stroke', 'black', 'fill', patt.getSelector(funciri=True))))

	genFiles(inspect.currentframe().f_code.co_name, sc)

