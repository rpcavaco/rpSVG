# -*- coding: utf-8 -*- 
'''
Created on 22 de Mai de 2014

@author: rui

'''

from copy import deepcopy


class Point2D(object):
	def __init__(self, x=0, y=0, other=None):
		self.x = x
		self.y = y
		self.cloneFrom(other)
	def set(self, x=0, y=0):
		self.x = x
		self.y = y
	def cloneFrom(self, otherpt):
		if not otherpt is None:
			self.x = otherpt.x
			self.y = otherpt.y
	def setReference(self, otherpt):
		if not otherpt is None:
			self.x = otherpt.x + self.x
			self.y = otherpt.y + self.y

class Envelope(object):
	def __init__(self):
		self.minx = 0
		self.miny = 0
		self.maxx = 0
		self.maxy = 0
	def getWidth(self):
		return self.maxx - self.minx
	def getHeight(self):
		return self.maxy - self.miny
	def getRectParams(self, outlist):
		del outlist[:]
		outlist.append(self.minx)
		outlist.append(self.miny)
		outlist.append(self.getWidth())
		outlist.append(self.getHeight())
	def getMidPt(self, outpt):
		outpt.x = self.minx + (self.getWidth() / 2.0)
		outpt.y = self.miny + (self.getHeight() / 2.0)
	def cloneFromOther(self, other):
		self.minx = other.minx
		self.miny = other.miny
		self.maxx = other.maxx
		self.maxy = other.maxy
	def expandFromOther(self, other):
		if other.minx < self.minx:
			self.minx = other.minx
		if other.miny < self.miny:
			self.miny = other.miny
		if other.maxx > self.maxx:
			self.maxx = other.maxx
		if other.maxy > self.maxy:
			self.maxy = other.maxy
	def expandFromPoint(self, pt):
		if pt.x < self.minx:
			self.minx = pt.x
		if pt.y < self.miny:
			self.miny = pt.y
		if pt.x > self.maxx:
			self.maxx = pt.x
		if pt.y > self.maxy:
			self.maxy = pt.y
	def expand(self, ratio):
		pt = Point2D()
		self.getMidPt(pt)
		newhwidth = self.getWidth() * ratio * 0.5
		newhheight = self.getHeight() * ratio * 0.5
		self.minx = pt.x - newhwidth 
		self.miny = pt.y - newhheight 
		self.maxx = pt.x + newhwidth 
		self.maxy = pt.y + newhheight 
	
# 	def extractFromPath(self, inlist, mirrory=False):
# 		for pair in pairwise(inlist):
# 			x, y = pair
# 			if mirrory:
# 				y = -y
# 		if x < self.minx:
# 			self.minx = x
# 		if y < self.miny:
# 			self.miny = y
# 		if x > self.maxx:
# 			self.maxx = x
# 		if y > self.maxy:
# 			self.maxy = y




	

	
