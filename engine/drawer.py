#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.sprite import Sprite,TextSprite
from engine.colors import *
from engine.physics import Collider

class Drawer(threading.Thread):
	def __init__(self,fps,window=None):
		threading.Thread.__init__(self)
		
		self.window=window
		self.fps = fps
		self.clock = pygame.time.Clock()
		
		self.colors = []
		self.sprites = []
		self.sprites_group=pygame.sprite.Group()
		self.current_fps = 0
		self.alive = threading.Event()
		self.alive.set()
		self.hitbox = False


	def onDraw(self):pass


	def clear(self):
		self.sprites = []
		self.sprites_group = pygame.sprite.Group()
		self.colors = []
	
	def addSprite(self,obj):
		if isinstance(obj,Sprite) or isinstance(obj,TextSprite):
			self.sprites_group.add(obj)
			self.sprites.append(obj)
		elif isinstance(obj,pygame.Color) or (isinstance(obj,tuple) and len(obj)>=3):
			self.colors.append(obj)
	
	def addSprites(self,objs):
		for obj in objs:
			self.addSprite(obj)


	def run(self):
		while self.alive.isSet():
			if self.window != None:
				self.onDraw()
				for color in self.colors:
					self.window.fill(color)
				for sprite in self.sprites:
					sprite.draw(self.window)
				
				if self.hitbox:
					for sprite in self.sprites:
						if isinstance(sprite,Collider):
							pygame.draw.line(self.window,WHITE,sprite.hit_rect.topleft,sprite.hit_rect.topright,3)
							pygame.draw.line(self.window,WHITE,sprite.hit_rect.topleft,sprite.hit_rect.bottomleft,3)
							pygame.draw.line(self.window,WHITE,sprite.hit_rect.topright,sprite.hit_rect.bottomright,3)
							pygame.draw.line(self.window,WHITE,sprite.hit_rect.bottomleft,sprite.hit_rect.bottomright,3)
				
				pygame.display.update()
				self.clock.tick(self.fps)
				self.current_fps = self.clock.get_fps()
				

	def stop(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)
