import json

from math import ceil

STYLE_ATTRIBS = [ 
	'font', 
    'font-family',
    'font-size',
    'font-size-adjust',
    'font-stretch',
    'font-style',
    'font-variant',
    'font-weight',
    'direction',
    'letter-spacing',
    'text-decoration',
    'unicode-bidi',
    'word-spacing',
    'clip', 
    'color',
    'cursor',
    'display',
    'overflow', 
    'visibility',
    'clip-path',
    'clip-rule',
    'mask',
    'opacity',
    'enable-background',
    'filter',
    'flood-color',
    'flood-opacity',
    'lighting-color',
    'stop-color',
    'stop-opacity',
	'pointer-events',
    'color-interpolation',
    'color-interpolation-filters',
    'color-profile',
    'color-rendering',
    'fill',
    'fill-opacity',
    'fill-rule',
    'image-rendering',
    'marker',
    'marker-end',
    'marker-mid',
    'marker-start',
    'shape-rendering',
    'stroke',
    'stroke-dasharray',
    'stroke-dashoffset',
    'stroke-linecap',
    'stroke-linejoin',
    'stroke-miterlimit',
    'stroke-opacity',
    'stroke-width',
    'text-rendering',
    'alignment-baseline',
    'baseline-shift',
    'dominant-baseline',
    'glyph-orientation-horizontal',
    'glyph-orientation-vertical',
    'kerning',
    'text-anchor',
    'writing-mode'
]

def toCSSItem(outbuf, indict, depth=-1):
	dp = depth + 1
	indent = '\t' * dp
	for k in list(indict.keys()):
		if isinstance(indict[k], dict):
			outbuf.append('{0}{1} {{'.format(indent, k))
			toCSSItem(outbuf, indict[k], depth=dp)
			outbuf.append('{0} }}'.format(indent))
		else:
			outbuf.append('{0}{1}: {2};'.format(indent, k, indict[k]))

def toCSS(indict):
	outbuf = []		
	toCSSItem(outbuf, indict)
	return '\n'.join(outbuf)
	
