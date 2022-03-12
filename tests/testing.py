
import cairosvg

from os import makedirs
from os.path import exists, join as path_join

SVG_PATH = "outtest"
IMG_FOLDER = "bitmaps"

def genTestFilenames(p_test_name):

	svgf = path_join(SVG_PATH)
	if not exists(svgf):
		makedirs(svgf)
	imgf = path_join(svgf, IMG_FOLDER)
	if not exists(imgf):
		makedirs(imgf)

	svgp = path_join(svgf, f"{p_test_name}.svg")
	imgp = path_join(imgf, f"{p_test_name}.png")
	pdfp = path_join(imgf, f"{p_test_name}.pdf")

	return svgp, imgp, pdfp

def genFiles(p_test_name, p_svgcontent):

	sfile, bmfile, pdffile = genTestFilenames(p_test_name)

	with open(sfile, 'w') as fl:
		fl.write(p_svgcontent.toString(pretty_print=True, inc_declaration=True))

	outbs = p_svgcontent.toBytes(pretty_print=True, inc_declaration=True)

	cairosvg.svg2png(bytestring=outbs, write_to=bmfile)
	cairosvg.svg2pdf(bytestring=outbs, write_to=pdffile)

