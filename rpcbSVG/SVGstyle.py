# -*- coding: utf-8 -*- 
'''
Created on 30 de Mar de 2014

@author: rui

Gerir estilos SVG
'''

import json

from math import ceil

def toCSS(indict):
	outbuf = []		
	toCSSItem(outbuf, indict)
	return '\n'.join(outbuf)
	
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

styleattrs_notserializable = ['symbscale','minfs']

class StyleAttribs(object):
	def toJson(self):
		idict = self.__dict__
		od = {}
		for k in list(idict.keys()):
			if k in styleattrs_notserializable:
				continue
			od[k.replace('_','-')] = idict[k]
		return json.dumps(od, indent=4)
	def toCSSDict(self, outdict):
		idict = self.__dict__
		for k in list(idict.keys()):
			if k in styleattrs_notserializable:
				continue
			if k.lower() == 'csskey':
				continue
			outdict[k.replace('_','-')] = idict[k]
		#outstr = json.dumps(outdict, indent=4, separators=(';', ': '))
		#return outstr.replace('\"','')
	def toCSS(self):
		outbuf = []		
		od = {}
		self.toCSSDict(od)
		toCSSItem(outbuf, od)
		return '\n'.join(outbuf)

class Stroke(StyleAttribs):
	def __init__(self, color, symbscale=1.0, w=None):
		self.stroke = color
		self.symbscale = symbscale
		if not w is None:
			self.setWidth(w*self.symbscale)
	def setWidth(self, w):
		self.stroke_width = '{0:.2f}'.format(float(w)*self.symbscale)
		#print 'setWidth:', w, self.symbscale, self.stroke_width
		return self
	def setLinejoin(self, lj):
		self.stroke_linejoin = lj
		return self
	def setLinecap(self, lc):
		self.stroke_linecap = lc
		return self
	def setOpacity(self, val):
		self.stroke_opacity = val
		return self
	def setDasharray(self, val):
		valsplits = [float(vs.strip()) for vs in val.split(',')]
		finalval = ['{0:.2f}'.format(vs*self.symbscale) for vs in valsplits]
		self.stroke_dasharray = ','.join(finalval)
		return self

class TextAttribs(StyleAttribs):
	def __init__(self, symbscale=1.0, minfs=1):
		self.font_family = None
		self.font_size = None
		self.symbscale = symbscale
		self.minfs = minfs
	def setFSize(self, fsize):
		sz = int(ceil(float(fsize) * self.symbscale))
		if sz < self.minfs:
			sz = self.minfs
		self.font_size = '{0:.2f}px'.format(sz)
		#print 'font-sz:', sz, self.font_size
		return self
	def setFFamily(self, val):
		self.font_family = val
		return self
	def setFWeight(self, val):
		self.font_weight = val
		return self
	def setTAnchor(self, val):
		self.text_anchor = val
		return self
					
class Fill(StyleAttribs):
	def __init__(self, color='none'):
		self.fill = color
	def setOpacity(self, val):
		self.fill_opacity = val
		return self
		
#if __name__ == "__main__":
	#r = Stroke('red', w=3)
	#print r.toCSS()
	
if __name__ == "__main__":
	d = {
	'rect': {
		'stroke': 'blue',
		'fill': 'red'
	}}
	outbuf = []
	toCSSItem(outbuf, d)
	print(('\n'.join(outbuf)))
	
	
