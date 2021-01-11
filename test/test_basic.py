
import pytest
import codecs

from os.path import join as path_join

from rpcbSVG.SVGLib import FullDocWorldSVG, FullDocSVG
from rpcbSVG.SVGstyle import Stroke, Fill
from rpcbSVG.BasicGeom import Path, Point2D, list2AbsPath


def test_first():
	s = FullDocSVG(scale=10)
	s.addStyle('rect', Stroke('blue', w=3))
	s.addStyle('rect', Fill('red'))
	r = s.addRect(100, 100, 700, 560)
	idstr = r.get('id')
	#print("id:", idstr)

	s.addStyle(f"#{idstr}", Fill('orange'))
	
	with open(path_join("outtest", 'teste.svg'), 'w') as fl:
		fl.write(s.toString())


def test_path(capsys):
    
    pth = Path()
    pth.addPtToLinestring(Point2D(x=10, y=20))
    pth.addPtToLinestring(Point2D(x=14, y=6))
    pth.addPtToLinestring(Point2D(x=18, y=32))

    with capsys.disabled():
        print(list2AbsPath(pth.points))

       