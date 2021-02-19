

import pytest

from rpcbSVG.Geometry import Pta, vec2_segment_intersect



def test_00Geometry():

	la = (Pta(1,1), Pta(2,3))
	lb = (Pta(3,1.5), Pta(5,0))

	# with capsys.disabled():

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None, ret

	# ----------------------------------------------

	lb = (Pta(1.1,1.5), Pta(5,0))

	ret = vec2_segment_intersect(*la, *lb)
	testret = [round(x,2) for x in ret]
	assert testret == [1.23, 1.45]

	# ----------------------------------------------

	lb = (Pta(-3.1,1.5), Pta(1,1.5))

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None

	# ----------------------------------------------

	la = (Pta(-10,-1), Pta(1,1))
	lb = (Pta(-10,1), Pta(1,-1))

	ret = vec2_segment_intersect(*la, *lb)
	testret = [round(x,1) for x in ret]
	assert testret == [-4.5, 0.0]

	# ----------------------------------------------

	la = (Pta(-10,-1), Pta(-10,1))
	lb = (Pta(1,-1), Pta(1,1))

	ret = vec2_segment_intersect(*la, *lb)
	assert ret is None


