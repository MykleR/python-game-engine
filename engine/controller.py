#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *
from engine.physics import *


class Controller:
	def __init__(self,keys):
		self.keys = keys
		
		self.vertical = 0
		self.horizontal = 0
	
	def get_axis(self,event):
		if event.type == KEYDOWN:
			if event.key == self.keys["RIGHT"]:
				self.horizontal = 1
			elif event.key == self.keys["LEFT"]:
				self.horizontal = -1
			elif event.key == self.keys["DOWN"]:
				self.vertical = 1
			elif event.key == self.keys["UP"]:
				self.vertical = -1
		elif event.type == KEYUP:
			if event.key == self.keys["RIGHT"]:
				if self.horizontal == 1:
					self.horizontal = 0
			elif event.key == self.keys["LEFT"]:
				if self.horizontal == -1:
					self.horizontal = 0
			elif event.key == self.keys["DOWN"]:
				if self.vertical == 1:
					self.vertical = 0
			elif event.key == self.keys["UP"]:
				if self.vertical == -1:
					self.vertical = 0 



class KinematicController(KinematicBody,Controller):
	def __init__(self,x,y,w,h,physics,keys,material=PhysicMaterial(),scene=None,
			wspeed=100,accel=15,deccel=0.15):
		
		Controller.__init__(self,keys)
		KinematicBody.__init__(self,x,y,w,h,physics,material=material,scene=scene)
		
		self.walkspeed=wspeed
		self.accel = accel
		self.deccel = deccel

	
	def handle_event(self,event):
		self.get_axis(event)
	
	def update(self):
		if self.velocity.x+self.horizontal*self.accel >= -self.walkspeed:
			if self.velocity.x+self.horizontal*self.accel <= self.walkspeed:
				self.velocity.x += self.horizontal*self.accel
		if self.velocity.y+self.vertical*self.accel >= -self.walkspeed:
			if self.velocity.y+self.vertical*self.accel <= self.walkspeed:
				self.velocity.y += self.vertical * self.accel
		
		if self.horizontal == 0:
			self.velocity.x -= self.velocity.x*self.deccel
		if self.vertical == 0:
			self.velocity.y -= self.velocity.y*self.deccel





class RigidBodyController(RigidBody,Controller):
	def __init__(self,x,y,w,h,physics,keys,material=PhysicMaterial(),scene=None,
			mspeed=1e10,jumpforce=98*2.7,wspeed=80,accel=5):
		
		
		Controller.__init__(self,keys)
		RigidBody.__init__(self,x,y,w,h,mspeed,physics,material=material,scene=scene)
		self.jumpforce = jumpforce
		self.walk_speed = wspeed
		self.accel = accel
		
	
	def handle_event(self,event):
		self.get_axis(event)

	def update(self):
		if self.horizontal > 0:
			if self.velocity.x+self.accel*self.physics.delta < self.walk_speed:
				self.addForce(Vector2(self.horizontal*self.accel,0))
		elif self.horizontal < 0:
			if self.velocity.x-self.accel*self.physics.delta > -self.walk_speed:
				self.addForce(Vector2(self.horizontal*self.accel,0))
				
		if self.vertical==-1:
			self.impulse(
				xforce=Vector2(self.jumpforce/2,self.jumpforce/1.5),
				yforce=Vector2(0,self.jumpforce)
			)
		
