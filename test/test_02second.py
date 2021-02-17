import pytest, re, json

from rpcbSVG.Basics import Pt, Mat, Trans, Scale, Rotate, SkewX, SkewY, pA, pC, pClose, pH, pM, pL, WrongValueTransformDef, pQ, pS, pT, pV
from rpcbSVG.SVGLib import Desc, Group, Polygon, Re, SVGContent, Circle, Rect, RectRC, Title, Use, Path, AnalyticalPath, Polyline
from rpcbSVG.SVGStyleText import Sty, CSSSty

# from lxml import etree

# with capsys.disabled():
def test_Use_RemoveChange():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	#sc = SVGContent(Re(10, 10, 600, 400, "px"), viewbox=VBox1280x1024())
	c = sc.addChild(Circle(20, 30, 60), todefs=True)
	c.setClass("batatas")

	ue1 = sc.addChild(Use(250,140,None,None, c.getSel()))
	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <circle cx="20" cy="30" r="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> </svg> """

	ue2 = sc.addChild(Use(Pt(20,12), c.getSel(select='class')))
	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <circle cx="20" cy="30" r="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> <use x="20" y="12" xlink:href=".batatas" id="Use2"/> </svg> """

	ue2.removeEl()
	del ue2

	s = Sty('stroke', 'blue', 'stroke-width', 10)
	ue1.setStyle(s)

	# Changing exisitng stroke-witdth to 20
	with ue1 as triplet:
		strct, styl, tr_list = triplet
		styl.set('stroke-width', 20)

	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"> <defs> <circle cx="20" cy="30" r="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1" fill="none" stroke="blue" stroke-width="20"/> </svg> """

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

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs/><rect x="200" y="200" width="300" height="400" id="Rec0" transform="rotate(45,250,300) translate(100,0)"/></svg>"""

	with r as triplet:
		strct, styl, tr_list = triplet
		tr_list[1].setvalue("tx", 150)

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs/><rect x="200" y="200" width="300" height="400" id="Rec0" transform="rotate(45,250,300) translate(150,0)"/></svg>"""

	with r as triplet:
		strct, styl, tr_list = triplet
		with pytest.raises(WrongValueTransformDef):		
			tr_list[1].setvalue("tL", 150)

def test_RoundRect():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	r = sc.addChild(RectRC(200,200,300,400, 10, 10))
	r.addTransform(Rotate(45,250,300))
	r.addTransform(Trans(100,0))

	assert sc.toString(pretty_print=False) == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs/><rect x="200" y="200" width="300" height="400" rx="10" ry="10" id="Rec0" transform="rotate(45,250,300) translate(100,0)"/></svg>"""

def test_JSON():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	c = sc.addChild(Circle(20, 30, 60), todefs=True)
	c.setClass("batatas")

	ue1 = sc.addChild(Use(250,140,None,None, c.getSel()))
	s = Sty('stroke', 'blue', 'stroke-width', 10)
	ue1.setStyle(s)

	assert sc.toJSON() == {"tag": "svg", "attribs": {"x": "0", "y": "0", "width": "100%", "height": "100%", "viewBox": "0 0 1000 1000"}, "content": [{"tag": "defs", "attribs": {}, "content": [{"tag": "style", "attribs": {}}, {"tag": "circle", "attribs": {"cx": "20", "cy": "30", "r": "60", "id": "Cir0", "class": "batatas"}}]}, {"tag": "use", "attribs": {"x": "250", "y": "140", "{http://www.w3.org/1999/xlink}href": "#Cir0", "id": "Use1", "fill": "none", "stroke": "blue", "stroke-width": "10"}}]}

	#with open('outtest/testeZZ.svg', 'w') as fl:
	#	fl.write(sc.toString(pretty_print=False))

def test_Paths():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	sc.addStyleRule(CSSSty('fill', 'red', 'stroke', 'green', selector='path'))
	pth = sc.addChild(Path("M10 12"))

	condens = re.sub(r"[\s]+"," ", sc.toString(pretty_print=False))

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs><style type="text/css"><![CDATA[path { fill: red; stroke: green; }]]></style></defs><path d="M10 12" id="Pat0"/></svg>"""

	with pytest.raises(TypeError):
		p = pM()
	with pytest.raises(TypeError):
		p = pM(12)

	p1 = pM(12, 24, 33, relative=True)	
	assert p1.get() == "m12 24"

	# relative=True will be ignored as it is first path command
	p2 = pM(120, 240, relative=True)	
	ap = sc.addChild(AnalyticalPath())
	ap.addCmd(p2)
	ap.refresh()

	condens = re.sub(r"[\s]+"," ", sc.toString(pretty_print=False))

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="100%" height="100%" viewBox="0 0 1000 1000"><defs><style type="text/css"><![CDATA[path { fill: red; stroke: green; }]]></style></defs><path d="M10 12" id="Pat0"/><path d="M120 240" id="Pat1"/></svg>"""


def test_PathCommands():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'green', 'stroke-width', '10', selector='.cambase'))

	sc.setBackground(Sty('fill', '#DEDEFD'))

	pts = [
		Pt(120, 140),
		Pt(290, 160),
		Pt(400, 160),

		Pt(550, 160),
		Pt(550, 300),
		Pt(400, 330),

		Pt(250, 500),
		Pt(400, 500),

		Pt(500, 600),

		Pt(500, 700),
		Pt(600, 700),

		Pt(700, 700),
		Pt(700, 800),

		Pt(900, 740),

		Pt(800, 500)
	]

	ap = sc.addChild(AnalyticalPath()).setClass("cambase")
	ap.addCmd(pM(*pts[0]))
	ap.addCmd(pL(*pts[1]))
	ap.addCmd(pL(*pts[2]))
	# Bezier
	ap.addCmd(pC(*pts[3], *pts[4], *pts[5]))
	ap.addCmd(pS(*pts[6], *pts[7]))
	# Horizontal e vertical
	ap.addCmd(pH(100, relative=True))
	ap.addCmd(pV(100, relative=True))
	# Quadratic bezier
	ap.addCmd(pQ(*pts[9], *pts[10]))
	ap.addCmd(pT(*pts[12]))

	ap.addCmd(pA(50,80, -14, 0,0, *pts[13]))
	# "rx", "ry", "x-axis-rotation", "large-arc-flag", "sweep-flag", "x", "y"
	ap.addCmd(pA(5,8, -14, 0,1, -100, -240, relative=True))
	ap.refresh()

	gr1 = sc.addChild(Group())
	gr1.setStyle(Sty('fill', 'white', 'stroke', 'green', 'stroke-width', '4'))
	for pt in pts:
		gr1.addChild(Circle(*pt,10))

	gr2 = sc.addChild(Group())
	gr2.setStyle(Sty('stroke', 'grey', 'stroke-width', '2', 'stroke-dasharray', '5,5'))

	ap2 = gr2.addChild(AnalyticalPath())
	ap2.addCmd(pM(*pts[2]))
	ap2.addCmd(pL(*pts[3]))

	ap2.addCmd(pM(*pts[4]))
	ap2.addCmd(pL(*pts[5]))

	ap2.addCmd(pM(*pts[6]))
	ap2.addCmd(pL(*pts[7]))

	ap2.addCmd(pM(*pts[8]))
	ap2.addCmd(pL(*pts[9]))

	ap2.addCmd(pM(*pts[9]))
	ap2.addCmd(pL(*pts[10]))

	ap2.addCmd(pM(*pts[10]))
	ap2.addCmd(pL(*pts[11]))

	ap2.addCmd(pM(*pts[11]))
	ap2.addCmd(pL(*pts[12]))
	ap2.refresh()

	with open('outtest/test_PathCommands.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True))

def test_PolylinePath():

	sc = SVGContent(Re().full()).setIdentityViewbox(scale=10.0)
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'green', 'stroke-width', '10', selector='.cambase'))

	pts = [
		Pt(120, 140), Pt(290, 160), Pt(400, 160),

		Pt(550, 160), Pt(550, 300), Pt(400, 330),

		Pt(250, 500), Pt(400, 500), Pt(500, 600),

		Pt(500, 700), Pt(600, 700), Pt(700, 700),
		Pt(700, 800), Pt(900, 740), Pt(800, 500),
		Pt(800,100), Pt(200,100)
	]

	ap = sc.addChild(AnalyticalPath()).setClass("cambase")
	ap.addPolylinePList(pts)

	ap.addCmd(pClose())

	gr1 = sc.addChild(Group())
	gr1.setStyle(Sty('fill', 'white', 'stroke', 'green', 'stroke-width', '4'))
	for pt in pts:
		gr1.addChild(Circle(*pt,10))

	with open('outtest/test_PolylinePath.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True))

def test_PolylinePolygon():

	sc = SVGContent(Re(0,0,1024,1000)).setIdentityViewbox()
	sc.addStyleRule(CSSSty('fill', 'darksalmon', 'fill-opacity', 0.6, 'stroke', 'darkmagenta', 'stroke-width', 2, selector='polygon'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'darkgoldenrod', 'stroke-width', 4, selector='polyline'))

	pts = [
		Pt(120, 140), Pt(290, 160), Pt(400, 160),

		Pt(550, 160), Pt(550, 300), Pt(400, 330),

		Pt(250, 500), Pt(400, 500), Pt(500, 600),

		Pt(500, 700), Pt(600, 700), Pt(700, 700),
		Pt(700, 800), Pt(900, 740), Pt(800, 500),
		Pt(800,100), Pt(200,100), Pt(120, 140)
	]

	pl = sc.addChild(Polygon())
	pl.addPList(pts)

	gr1 = sc.addChild(Group())
	gr1.setStyle(Sty('fill', 'white', 'stroke', 'green', 'stroke-width', '3'))
	for pt in pts:
		gr1.addChild(Circle(*pt,6))

	gr2 = sc.addChild(Group())
	gr2.addTransform(Trans(10,30))
	plg = gr2.addChild(Polyline())
	plg.addPList(pts[1:-1])

	with open('outtest/test_PolylinePoligon.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True))

def test_GroupDefsTitleDesc():

	sc = SVGContent(Re(0,0,1024,1000)).setIdentityViewbox()
	sc.addChild(Title("El teste de title, desc, etc ..."))
	desc = sc.addChild(Desc(), nsmap={"mydoc": "http://example.org/mydoc"})
	desc.addChildTag("{http://example.org/mydoc}bibtitle").text = "El simpático teste"
	desc.addChildTag("{http://example.org/mydoc}descr").text = "Eso es de un teste de puta madre!"

	gr1 = sc.addChild(Group())
	gr1.addTransform(Rotate(45,250,300))
	re = gr1.addChild(RectRC(200,200,600,400,10,20), todefs=True)
	gr1.addChild(Use(Pt(20,12), re.getSel()))
	re.setStyle(Sty('fill', 'white', 'stroke', 'green', 'stroke-width', '3'))

	result = sc.toString(pretty_print=False)
	assert result == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="1024" height="1000" viewBox="0 0 1024 1000"><defs/><title>El teste de title, desc, etc ...</title><desc xmlns:mydoc="http://example.org/mydoc"><mydoc:bibtitle>El simpático teste</mydoc:bibtitle><mydoc:descr>Eso es de un teste de puta madre!</mydoc:descr></desc><g id="G0" transform="rotate(45,250,300)"><defs id="Def1"><rect x="200" y="200" width="600" height="400" rx="10" ry="20" id="Rec2" fill="white" stroke="green" stroke-width="3"/></defs><use x="20" y="12" xlink:href="#Rec2" id="Use3"/></g></svg>""", result

	with open('outtest/test_GroupDefsTitleDesc.svg', 'w') as fl:
		fl.write(sc.toString(pretty_print=True))




	# with capsys.disabled():
	# 	print("\n>>>>>>>>>>")
	# 	print("\n<<<<<<<<<<")

	# with capsys.disabled():
	# 	print(condens)


