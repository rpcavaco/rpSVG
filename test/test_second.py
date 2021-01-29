

import pytest, re

from rpcbSVG.Basics import Pt #, Env
from rpcbSVG.SVGLib import Re, SVGContent, VBox1280x1024, Circle, Use # BaseSVGElem, Group, Rect, Style, SVGRoot, TagOutOfDirectUserManipulation, VBox600x800
from rpcbSVG.SVGstyle import Sty, CSSSty

#from lxml import etree




def test_Re2(capsys):
	with capsys.disabled():
		sc = SVGContent(Re(10, 10, 600, 400, "px"), viewbox=VBox1280x1024())
		c = sc.addChild(Circle(20, 30, 60), todefs=True)

		ue1 = sc.addChild(Use(250,140,None,None, c.getSel()))
		condens = re.sub(r"[\s]+"," ", sc.toString())
		assert condens == """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="10px" y="10px" width="600px" height="400px" viewBox="0 0 1280 1024"> <defs> <circle cx="20" cy="30" rad="60" id="Cir0"/> </defs> <use x="250" y="140" xlink:href="#Cir0" id="Use1"/> </svg> """

	# reo = Re(1, 2, 200, 300)
	# reo.setUnits('px')
	# assert str(reo) == "x=1px y=2px width=200px height=300px"
	# ref_dict = {'_units': 'px', 'x': '1px', 'y': '2px', 'width': '200px', 'height': '300px'}
	# shared_items = {k: ref_dict[k] for k in ref_dict.keys() if k in dir(reo) and ref_dict[k] == getattr(reo,k)}
	# assert len(shared_items) == 5
	# assert list(reo.iterUnitsRemoved()) == ['1', '2', '200', '300']
