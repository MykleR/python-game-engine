#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.colors import *
from engine.object import Object



class Sprite(Object,pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,surface,groups=[],scene=None):
		pygame.sprite.Sprite.__init__(self,groups)
		Object.__init__(self,x,y,w,h,scene=scene)
		
		self.new_surface(surface)
			
	def onDraw(self):pass
	def onRotate(self):pass
	def onUpdateSurface(self):pass

	def new_surface(self,surface):
		self.onUpdateSurface()
		if isinstance(surface,pygame.Color) or (isinstance(surface,tuple) and len(surface)>=3):
			self.color = surface
			self.image = pygame.Surface(self.rect.size,pygame.SRCALPHA)
			self.image.fill(self.color)
			self.image = self.image.convert_alpha()
			self.origin_image = self.image
			#~ self.origin_image.lock()
		elif type(surface)==pygame.Surface:
			self.color = None
			self.image = pygame.transform.scale(surface,self.rect.size)
			self.image = self.image.convert_alpha()
			self.origin_image = surface.convert_alpha()
			#~ self.origin_image.lock()
	
	def rotate(self):
		self.image = pygame.transform.rotate(self.origin_image,-self.angle)
		self.rect = self.image.get_rect(center=self.pos)
		self.onRotate()
	
	
	def draw(self,surface):
		if self.image != None:
			surface.blit(self.image,self.rect)
			self.onDraw()
		


class TextSprite(Object,pygame.sprite.Sprite):
	def __init__(self,x,y,size,color,bgcolor=None,font=None,txt="",scene=None,groups=[]):
		pygame.sprite.Sprite.__init__(self,groups)
		Object.__init__(self,x,y,size,size,scene=scene)
		
		self.txt = txt
		self.path_font = font
		self.color = color
		self.bgcolor = bgcolor
		
		self.font = None
		self.image = None
		
		self.update()
	
	def load_font(self,path):
		return pygame.font.Font(path,self.rect.width)
	
	def update(self):
		self.font = self.load_font(self.path_font)
		self.image = self.font.render(self.txt,True,self.color).convert_alpha()
	
	def draw(self,surface,offset=(0,0)):
		if self.image != None:
			if self.bgcolor!=None:
				surface.fill(self.bgcolor)
			surface.blit(self.image,(self.rect.x+offset[0],self.rect.y+offset[1]))
		
		
		

