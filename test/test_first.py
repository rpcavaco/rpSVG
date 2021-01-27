
import pytest, re

from rpcbSVG.Basics import Pt, Env
from rpcbSVG.SVGLib import BaseSVGElem, Circle, Group, Re, Rect, SVGContent, SVGRoot, TagOutOfDirectUserManipulation, VBox600x800
from rpcbSVG.SVGstyle import Sty

from lxml import etree

# with capsys.disabled():

def test_Re():
	reo = Re(1, 2, 200, 300)
	reo.setUnits('px')
	assert str(reo) == "x=1px y=2px width=200px height=300px"
	ref_dict = {'_units': 'px', 'x': '1px', 'y': '2px', 'width': '200px', 'height': '300px'}
	shared_items = {k: ref_dict[k] for k in ref_dict.keys() if k in reo.__dict__.keys() and ref_dict[k] == reo.__dict__[k]}
	assert len(shared_items) == 5
	assert list(reo.iterUnitsRemoved()) == ['1', '2', '200', '300']

def test_SVGRoot():
	s = SVGRoot(Re(2,3,100,200, "px"))
	r = s.addChild(Rect(0,0,30,40))
	assert str(r.getStruct()) == "x=0 y=0 width=30 height=40", r.getStruct()
	ref_dict = {'tag': 'rect', 'idprefix': 'Rec'}
	shared_items = {k: ref_dict[k] for k in ref_dict.keys() if k in r.__dict__.keys() and ref_dict[k] == r.__dict__[k]}
	assert len(shared_items) == 2
	assert str(r.getStruct()) == "x=0 y=0 width=30 height=40"
	assert etree.tostring(s.getEl()) == b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="2px" y="3px" width="100px" height="200px"><rect x="0" y="0" width="30" height="40"/></svg>'


def test_GroupCircle():
	s2 = SVGRoot(Re().full(), viewbox=VBox600x800())
	g = s2.addChild(Group()).setId("o_grupo")
	g.addChild(Circle(20, 30, 60))
	assert etree.tostring(s2.getEl()) == b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 600 800"><g id="o_grupo"><circle cx="20" cy="30" rad="60"/></g></svg>'

def test_IdentVB():
	s = SVGRoot(Re(0,3,100,200)).setIdentityViewbox(scale=10.0)
	r = s.addChild(Circle(0,0,30))
	assert etree.tostring(s.getEl()) == b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="3" width="100" height="200" viewBox="0 30 1000 2000"><circle cx="0" cy="0" rad="30"/></svg>'

def test_DirectUserManipulation():
	s = SVGContent(Re().full())
	with pytest.raises(TagOutOfDirectUserManipulation):
		s.addChild(BaseSVGElem("defs"))

def test_Envelope():
	s = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	s.addChild(Rect( Env().centerAndDims(Pt(12,34), 300, 800).getRectParams() ))
	retstr = s.toString().replace('\n', '')
	assert retstr ==  '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000">  <rect x="-138.0" y="-366.0" width="300.0" height="800.0" id="Rec0"/></svg>'''

def test_Sty():
	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(Rect(0,0,30,40, "px"))
	s1 = Sty('fill', 'red', 'stroke', 'green')
	s2 = r.setStyle(s1).getStyle()
	assert s1.diffDict(s2) == {'selector': (None, '#Rec0')}
	out = s2.toCSSString()
	condens = re.sub(r"[\s]+"," ", out)
	assert condens == "#Rec0 { fill: red; stroke: green; }", condens
	s3 = r.getStyle(select='class')
	assert s1 == s3, s1.diffDict(s3)
	r.setClass("testclass")
	s4 = r.getStyle(select='class')
	assert s1.diffDict(s4) == {'selector': (None, '.testclass')}
	s4.addFromDict({'stroke-width': '12'})
	str(s4) == "sel=.testclass fill=red stroke=green stroke-width=12"
	s4.addFromDict({'circle': {'stroke-opacity': '0.12'}})
	str(s4) == "sel=circle fill=red stroke=green stroke-opacity=0.12 stroke-width=12"





