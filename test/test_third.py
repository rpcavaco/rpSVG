

import pytest

from rpcbSVG.Basics import Pt, Rotate, polar2rect, ptAdd, ptGetAngle
from rpcbSVG.SVGstyle import CSSSty, Sty
from rpcbSVG.SVGLib import Circle, Group, Line, Marker, Mrk, MrkProps, Polygon, Polyline, Re, SVGContent

#	with capsys.disabled():

def test_Marker(capsys):

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


	#with capsys.disabled():
	#	print("\nmr:", mr)
