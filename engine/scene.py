#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *
from engine.object import *
from engine.sprite import *
from engine.physics import *

class Scene:
	def __init__(self,engine):
		self.objects = []
		self.engine = engine
	
	
	def add(self,obj):
		if isinstance(obj,list):
			for o in obj:
				if not o in self.objects:
					self.engine.physics.addBody(o)
					self.engine.drawer.addSprite(o)
					self.engine.physics.addCollider(o)
					self.objects.append(o)
		elif obj not in self.objects:
			self.engine.physics.addBody(obj)
			self.engine.drawer.addSprite(obj)
			self.engine.physics.addCollider(obj)
			self.objects.append(obj)
	
	
	def handle_event(self):
		self.onEventEnter()
		for event in pygame.event.get():
			self.onEventStay(event)
			if event.type == QUIT:
				self.engine.stop()
			for obj in self.objects:
				if isinstance(obj,Object):
					obj.handle_event(event)
		self.onEventExit()
	
	
	def update(self):
		self.onUpdateEnter()
		for obj in self.objects:
			if isinstance(obj,Object):
				obj.update()
		self.onUpdateExit()
	
	def start(self):
		self.engine.drawer.addSprites(self.objects)
		self.engine.physics.addCollider(self.objects)
		self.engine.physics.addBody(self.objects)
		self.onStart()
	
	def run(self):
		self.handle_event()
		self.update()
		self.onRun()
	
	def onStart(self):pass
	def onRun(self):pass
	
	def onEventEnter(self):pass
	def onEventExit(self):pass
	def onEventStay(self,event):pass
	
	def onUpdateEnter(self):pass
	def onUpdateExit(self):pass
	
	def onDrawEnter(self):pass
	def onDrawExit(self):pass
