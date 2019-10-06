from engine.engine_lib import *

from engine.sprite import Sprite
from engine.colors import *
from engine.physics import *
from engine.controller import *

import math


pygame.init()



class Block(Sprite,Collider):
	def __init__(self,x,y,w,h,color,material=PhysicMaterial(),groups=[],scene=None):
		Sprite.__init__(self,x,y,w,h,color,groups=groups)
		Collider.__init__(self,x,y,w,h,material=material,scene=scene)




class TopDownPlayer(KinematicController,Sprite):
	def __init__(self,x,y,w,h,color,physics,groups=[],scene=None,
			keys={"LEFT":K_LEFT,"RIGHT":K_RIGHT,"UP":K_UP,"DOWN":K_DOWN}):
		
		Sprite.__init__(self,x,y,w,h,color,groups=groups)
		KinematicController.__init__(self,x,y,w,h,physics,keys,scene=scene)
		



class Player(Sprite,RigidBodyController):
	def __init__(self,x,y,w,h,surface,physics,material=PhysicMaterial(),groups=[],
			mspeed=1e10,jumpforce=98*2.7,wspeed=80,accel=20,scene=None,
			keys={"LEFT":K_LEFT,"RIGHT":K_RIGHT,"UP":K_UP,"DOWN":K_DOWN}):
	
		Sprite.__init__(self,x,y,w,h,surface,groups=groups)
		RigidBodyController.__init__(self,x,y,w,h,physics,keys,
			material=material,scene=scene,
			mspeed=mspeed,jumpforce=jumpforce,wspeed=wspeed,accel=accel)
		
	
	
	def impulse(self,xforce=Vector2(0,0),yforce=Vector2(0,0)):
		if self.right_wall != None:
			self.right_wall = None
			self.addForce(-xforce)
			if isinstance(self.right_wall,RigidBody):
				self.right_wall.addForce(xforce)
		if self.left_wall != None:
			self.left_wall = None
			self.addForce(Vector2(xforce.x,-xforce.y))
			if isinstance(self.left_wall,RigidBody):
				self.left_wall.addForce(Vector2(-xforce.x,xforce.y))
		if self.floor != None and self.right_wall == None and self.left_wall == None:
			self.floor = None
			self.addForce(-yforce)
			if isinstance(self.floor,RigidBody):
				self.floor.addForce(yforce)
