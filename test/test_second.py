

import pytest, re

from rpcbSVG.Basics import Pt #, Env
from rpcbSVG.SVGLib import Re, SVGContent, VBox1280x1024, Circle, Use # BaseSVGElem, Group, Rect, Style, SVGRoot, TagOutOfDirectUserManipulation, VBox600x800
from rpcbSVG.SVGstyle import Sty, CSSSty

#from lxml import etree


# with capsys.disabled():

def test_Use_RemoveChange(capsys):

	sc = SVGContent(Re(10, 10, 600, 400, "px"), viewbox=VBox1280x1024())
	c = sc.addChild(Circle(20, 30, 60), todefs=True)
	c.setClass("batatas")

	ue1 = sc.addChild(Use(250,140,None,None, c.getSel()))
	condens = re.sub(r"[\s]+"," ", sc.toString())
	
	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="10px" y="10px" width="600px" height="400px" viewBox="0 0 1280 1024"> <defs> <circle cx="20" cy="30" rad="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> </svg> """

	ue2 = sc.addChild(Use(Pt(20,12), c.getSel(select='class')))
	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="10px" y="10px" width="600px" height="400px" viewBox="0 0 1280 1024"> <defs> <circle cx="20" cy="30" rad="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> <use x="20" y="12" xlink:href=".batatas" id="Use2"/> </svg> """

	ue2.removeEl()
	del ue2

	s = Sty('stroke', 'blue', 'stroke-width', 10)
	ue1.setStyle(s)

	with ue1 as str_sty:
		strct, styl = str_sty
		styl.set('stroke-width', 20)

	condens = re.sub(r"[\s]+"," ", sc.toString())

	assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="10px" y="10px" width="600px" height="400px" viewBox="0 0 1280 1024"> <defs> <circle cx="20" cy="30" rad="60" id="Cir0" class="batatas"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1" fill="none" stroke="blue" stroke-width="20"/> </svg> """


