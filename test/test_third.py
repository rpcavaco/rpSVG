

import pytest

from rpcbSVG.Basics import Pt, Rotate, polar2rect, ptAdd, ptGetAngle
from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.SVGLib import Circle, GradientStop, Group, Line, LinearGradient, Marker, Mrk, MrkProps, Polygon, Polyline, RadialGradient, Re, RectRC, SVGContent, TRef, TSpan, Text

#	with capsys.disabled():

def test_Marker():

	def pttrans(p_pt, p_ang):
		return (p_pt, ptAdd(p_pt, polar2rect(p_ang, 30)))

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

	with open('outtest/test_Marker.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True))


def test_Gradient():

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

	sc.addChild(RectRC(200,50,500,400,10,20)).setStyle(Sty('fill', 'url(#the_grad)', 'stroke', 'black'))
	
	sc.addChild(RectRC(850,500,600,400,10,20)).setStyle(Sty('fill', 'url(#the_rgrad)', 'stroke', 'black'))

	with open('outtest/test_Gradient.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))

def test_Text():

	sc = SVGContent(Re(0,0,1600,1200)).setIdentityViewbox()
	td = sc.addChild(Text(), todefs=True).setText("Gatos ao ataque")

	p = Pt(800,600)

	tx = sc.addChild(Text(*p))   
	tx.setStyle(Sty('fill', 'teal', 'font-size', 70, 'text-anchor', 'middle'))
	tx.setText("Aproveitar para fazer um ")

	# gliphs dont rotate on gnome implementation
	ts = tx.addChild(TSpan(None, None, None, None, -20).setStyle(Sty('fill', 'red')).setText("grande")  )
	ts.tailText(" anúncio")

	tx.addTransform(Rotate(45,*p))

	assert tx.getStruct().getfields() == "x,y,dx,dy,rotate,textLength,lengthAdjust"


	tx2 = sc.addChild(Text(200,900))   
	tx2.setStyle(Sty('fill', 'green', 'font-size', 90))
	tx2.addChild(TRef(td.getId()))

	with open('outtest/test_Text.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True, inc_declaration=True))


	#with capsys.disabled():
	#	print("\nmr:", mr)
