

import pytest, re

from rpcbSVG.Basics import Pt, Mat, Trans, Scale, Rotate, SkewX, SkewY, WrongValueTransformDef
from rpcbSVG.SVGLib import Re, SVGContent, Circle, Rect, RectRC, Use 
from rpcbSVG.SVGstyle import Sty, CSSSty

#from lxml import etree


# with capsys.disabled():

def test_Use_RemoveChange():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	#sc = SVGContent(Re(10, 10, 600, 400, "px"), viewbox=VBox1280x1024())
	c = sc.addChild(Circle(20, 30, 60), todefs=True)
	c.setClass("batatas")

	ue1 = sc.addChild(Use(250,140,None,None, c.getSel()))
	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <circle cx="20" cy="30" r="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> </svg> """

	ue2 = sc.addChild(Use(Pt(20,12), c.getSel(select='class')))
	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <circle cx="20" cy="30" r="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> <use x="20" y="12" xlink:href=".batatas" id="Use2"/> </svg> """

	ue2.removeEl()
	del ue2

	s = Sty('stroke', 'blue', 'stroke-width', 10)
	ue1.setStyle(s)

	# Changing exisitng stroke-witdth to 20
	with ue1 as triplet:
		strct, styl, tr_list = triplet
		styl.set('stroke-width', 20)

	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <circle cx="20" cy="30" r="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1" fill="none" stroke="blue" stroke-width="20"/> </svg> """

	# with open('outtest/testeZZ.svg', 'w') as fl:
	# 	fl.write(sc.toString())

def test_TransformDefinitions():

	with pytest.raises(TypeError):
		mt = Mat()

	with pytest.raises(TypeError):
		mt = Mat(1, 2,3,4,5)

	mt = Mat(1, 2,30,4,5,6)
	assert mt.get() == "matrix(1,2,30,4,5,6)"

	with pytest.raises(TypeError):
		tr = Trans()
	tr = Trans(12)
	tr = Trans(12,24)
	assert tr.get() == "translate(12,24)"

	with pytest.raises(TypeError):
		x = Scale()
	sc = Scale(10)
	sc = Scale(14,34)
	assert sc.get() == "scale(14,34)"

	with pytest.raises(TypeError):
		x = Rotate()
	rt = Rotate(10)
	rt = Rotate(12,36,36)
	assert rt.get() == "rotate(12,36,36)"

	with pytest.raises(TypeError):
		x = SkewX()
	with pytest.raises(TypeError):
		x = SkewY()

	sk = SkewX(12,36,36)
	assert sk.get() == "skewX(12)"
	sk = SkewY(2,36,36)
	assert sk.get() == "skewY(2)"

def test_Transform():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(Rect(200,200,300,400))
	r.addTransform(Rotate(45,250,300))
	r.addTransform(Trans(100,0))

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs/><rect x="200" y="200" width="300" height="400" id="Rec0" transform="rotate(45,250,300) translate(100,0)"/></svg>"""

	with r as triplet:
		strct, styl, tr_list = triplet
		tr_list[1].setvalue("tx", 150)

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs/><rect x="200" y="200" width="300" height="400" id="Rec0" transform="rotate(45,250,300) translate(150,0)"/></svg>"""

	with r as triplet:
		strct, styl, tr_list = triplet
		with pytest.raises(WrongValueTransformDef):		
			tr_list[1].setvalue("tL", 150)

def test_RoundRect():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(RectRC(200,200,300,400, 10, 10))
	r.addTransform(Rotate(45,250,300))
	r.addTransform(Trans(100,0))

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs/><rect x="200" y="200" width="300" height="400" rx="10" ry="10" id="Rec0" transform="rotate(45,250,300) translate(100,0)"/></svg>"""

	#with open('outtest/testeZZ.svg', 'w') as fl:
	#	fl.write(sc.toString(pretty_print=False))



