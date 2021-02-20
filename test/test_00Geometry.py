

import inspect
from rpcbSVG.SVGLib import SVGContent
from test.testing import genFiles
from rpcbSVG.Symbols import Cross, XSight
from rpcbSVG.SVGStyleText import CSSSty, Sty
from rpcbSVG.Structs import Re
from rpcbSVG.Basics import GLOBAL_ENV
import pytest
from rpcbSVG.Geometry import Pta, vec2_segment_intersect


def test_00Intersect(capsys):

	la = (Pta(1,1), Pta(2,3))
	lb = (Pta(3,1.5), Pta(5,0))

	with capsys.disabled():

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

		# ----------------------------------------------

		lb = (Pta(1.1,1.5), Pta(5,0))

		ret = vec2_segment_intersect(*la, *lb)
		testret = [round(x,2) for x in ret]
		assert testret == [1.23, 1.45], testret

		# ----------------------------------------------

		lb = (Pta(-3.1,1.5), Pta(1,1.5))

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

		# ----------------------------------------------

		la = (Pta(-10,-1), Pta(1,1))
		lb = (Pta(-10,1), Pta(1,-1))

		ret = vec2_segment_intersect(*la, *lb)
		testret = [round(x,1) for x in ret]
		assert testret == [-4.5, 0.0], testret

		# ----------------------------------------------

		la = (Pta(-10,-1), Pta(-10,1))
		lb = (Pta(1,-1), Pta(1,1))

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

		la = (Pta(240, 400), Pta(640, 300))
		lb = (Pta(740, 355), Pta(740, 245))

		ret = vec2_segment_intersect(*la, *lb)
		assert ret is None, ret

def genCurveIntersectText(p_ynvert):

	# Coordinates rounded to 1 dec.place
	GLOBAL_ENV["ROUND"]["places"] = 1

	sc = SVGContent(Re(0,0,1600,1200), yinvert=p_ynvert).setIdentityViewbox()

	sc.setBackground(Sty('fill', '#E7E8EA'))

	# Styles to DEFS
	sc.addStyleRule(CSSSty('fill', '#434343', 'font-size', '14pt', 'font-family', 'Helvetica', selector='.text1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', 'red', 'stroke-width', 4, selector='.caixas'))
	sc.addStyleRule(CSSSty('stroke', 'grey', 'stroke-width', 1, selector='.aid1'))
	sc.addStyleRule(CSSSty('fill', 'none', 'stroke', '#404040', 'font-size', 24, 'font-family', 'Helvetica','stroke-width', 2, 'text-anchor', 'middle', selector='.lbls'))


	# SYMBOL DEFINITIONS ------------------------------------------------------
	#
	xsight = sc.addChild(XSight(46,46,8), todefs=True, noyinvert=True)
	crsymb_centerMarker = sc.addChild(Cross(20,20), todefs=True)
	#
	# =========================================================================

	return sc

def test_00X(capsys):

	with capsys.disabled():

		sc = genCurveIntersectText(False)
		genFiles(inspect.currentframe().f_code.co_name, sc)
