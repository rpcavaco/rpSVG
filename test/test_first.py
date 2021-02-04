
import pytest, re

from rpcbSVG.Basics import Pt, Env
from rpcbSVG.SVGLib import BaseSVGElem, Circle, Ellipse, Group, Line, Re, ReRC, \
	Rect, Style, SVGContent, SVGRoot, TagOutOfDirectUserManipulation, VBox600x800
from rpcbSVG.SVGstyle import Sty, CSSSty

from lxml import etree

# with capsys.disabled():

def test_CSSSty():
	assert str(CSSSty('stroke', 'white', selector="rect")) == "sel=rect fill=none stroke=white"
	with pytest.raises(TypeError):
		c = CSSSty('stroke', 'white')

def test_Re():
	reo = Re(1, 2, 200, 300)
	reo.setUnits('px')
	assert str(reo) == "Re x=1px y=2px width=200px height=300px"
	ref_dict = {'_units': 'px', 'x': '1px', 'y': '2px', 'width': '200px', 'height': '300px'}
	shared_items = {k: ref_dict[k] for k in ref_dict.keys() if k in dir(reo) and ref_dict[k] == getattr(reo,k)}
	assert len(shared_items) == 5
	assert list(reo.iterUnitsRemoved()) == ['1', '2', '200', '300']

def test_SVGRoot():
	s = SVGRoot(Re(2,3,100,200, "px"))
	r = s.addChild(Rect(0,0,30,40))
	assert str(r.getStruct()) == "Re x=0 y=0 width=30 height=40", r.getStruct()
	ref_dict = {'tag': 'rect', 'idprefix': 'Rec'}
	shared_items = {k: ref_dict[k] for k in ref_dict.keys() if k in dir(r) and ref_dict[k] == getattr(r,k)}
	assert len(shared_items) == 2
	assert str(r.getStruct()) == "Re x=0 y=0 width=30 height=40"
	assert etree.tostring(s.getEl()) == b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="2px" y="3px" width="100px" height="200px"><rect x="0" y="0" width="30" height="40"/></svg>'

def test_GroupSomeBasicShapes():
	s2 = SVGRoot(Re().full(), viewbox=VBox600x800())
	g = s2.addChild(Group()).setId("o_grupo")
	g.addChild(Circle(20, 30, 60))
	g.addChild(Ellipse(20, 30, 70, 80))
	g.addChild(Line(20, 30, 80, 90))
	assert etree.tostring(s2.getEl()) == b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 600 800"><g id="o_grupo"><circle cx="20" cy="30" r="60"/><ellipse cx="20" cy="30" rx="70" ry="80"/><line x1="20" y1="30" x2="80" y2="90"/></g></svg>'

def test_IdentVB():
	s = SVGRoot(Re(0,3,100,200)).setIdentityViewbox(scale=10.0)
	r = s.addChild(Circle(0,0,30))
	assert etree.tostring(s.getEl()) == b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="3" width="100" height="200" viewBox="0 30 1000 2000"><circle cx="0" cy="0" r="30"/></svg>'

def test_DirectUserManipulation():
	s = SVGContent(Re().full())
	with pytest.raises(TagOutOfDirectUserManipulation):
		s.addChild(BaseSVGElem("defs"))

def test_Envelope():
	s = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	s.addChild(Rect( Env().centerAndDims(Pt(12,34), 300, 800).getRectParams() ))
	retstr = s.toString().replace('\n', '')
	condens = re.sub(r"[\s]+"," ", retstr)
	assert condens ==  '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs/> <rect x="-138.0" y="-366.0" width="300.0" height="800.0" id="Rec0"/></svg>'''

def test_Sty():
	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(Rect(0,0,30,40, "px"))
	s1 = Sty('fill', 'red', 'stroke', 'green')
	s2 = r.setStyle(s1).getStyle(select='id')
	assert s1.diffDict(s2) == {'selector': (None, '#Rec0')}
	out = s2.toCSSString()
	condens = re.sub(r"[\s]+"," ", out)
	assert condens == "#Rec0 { fill: red; stroke: green; }", condens
	with pytest.raises(AssertionError):
		s3 = r.getStyle(select='class')

	r.setClass("testclass")
	s4 = r.getStyle(select='class')
	assert s1.diffDict(s4) == {'selector': (None, '.testclass')}
	s4.addFromDict({'stroke-width': '12'})
	str(s4) == "sel=.testclass fill=red stroke=green stroke-width=12"
	s4.addFromDict({'circle': {'stroke-opacity': '0.12'}})
	str(s4) == "sel=circle fill=red stroke=green stroke-opacity=0.12 stroke-width=12"

def test_styleElement():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(Rect(80,100,300,400))
	r.setClass('classz')

	selectstr = sc.addStyleRule(CSSSty('stroke', 'red', 'fill', 'blue', selector=r.getSel()))
	condens = re.sub(r"[\s]+"," ", sc.toString())
	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <style type="text/css"><![CDATA[#Rec0 { fill: blue; stroke: red; }]]></style> </defs> <rect x="80" y="100" width="300" height="400" id="Rec0" class="classz"/> </svg> """
	
	assert sc.delStyleRule(selectstr)

	selectstr = sc.addStyleRule(CSSSty('stroke', 'red', 'fill', 'blue', selector=r.getSel(select='class')))
	condens = re.sub(r"[\s]+"," ", sc.toString())
	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <style type="text/css"><![CDATA[.classz { fill: blue; stroke: red; }]]></style> </defs> <rect x="80" y="100" width="300" height="400" id="Rec0" class="classz"/> </svg> """

#	with capsys.disabled():

def test_similarElement(capsys):

	sc = SVGContent(ReRC().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(Rect(80,100,300,400))
	r2 = sc.addChild(Rect(80,100,300,400))
	with capsys.disabled():
		assert set(r.similitudeTo(r2)) == set(('TAG', 'STRUCT'))

	r3 = sc.addChild(Rect(80,100,300,400, "px"))
	assert r.similitudeTo(r3) == ['TAG']

	r4 = sc.addChild(Rect(80,100,300,400))
	s1 = Sty('fill', 'red', 'stroke', 'green')
	r4.setStyle(s1)
	assert set(r.similitudeTo(r4)) == set(('TAG', 'STRUCT'))

	r5 = sc.addChild(Rect(80,10,30,40, "px"))
	s2 = Sty('stroke', 'blue')
	r5.setStyle(s1)
	assert r.similitudeTo(r5) == ['TAG']

	r6 = sc.addChild(Rect(90,10,240,320))
	s1 = Sty('fill', 'red', 'stroke', 'green')
	r6.setStyle(s1)
	assert set(r4.similitudeTo(r6)) == set(('TAG', 'STYLE'))

		# with open('outtest/testeZZ.svg', 'w') as fl:
		#	fl.write(sc.toString())







