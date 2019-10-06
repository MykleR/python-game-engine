#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

class Object:
	def __init__(self,x,y,w,h,r=0,scene=None):
		self.rect = Rect(0,0,w,h)
		self.pos = Vector2(x,y)
		self.rect.center = self.pos
		self.angle = r
		self.scene = scene
		if scene!=None:scene.add(self)
		
		
	def update_rect(self):
		self.rect.center = self.pos
	
	def handle_event(self,event=None):pass
	def update(self):pass
