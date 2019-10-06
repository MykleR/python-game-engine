#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.object import Object



class PhysicMaterial:
	def __init__(self,friction=0.2,bounce=0,
			left=True,right=True,up=True,down=True):
		self.friction = friction
		self.bounce = bounce
		
		self.left = left
		self.right = right
		self.up = up
		self.down = down
							
			


class Collider(Object):
	def __init__(self,x,y,w,h,physics=None,scene=None,
			material=PhysicMaterial(),offset=(0,0)):
		Object.__init__(self,x,y,w,h,scene=scene)
		
		self.offset = offset
		self.hit_rect = Rect(0,0,w+offset[0],h+offset[1])
		self.hit_rect.center = self.pos
		self.physics = physics
		self.physics_material = material
		
		self.floor = None
		self.right_wall = None
		self.left_wall = None
		self.roof = None
		self.hits = []
	
	def group_collision(self,group):
		hits = pygame.sprite.spritecollide(self, group, False,self.collide_hit_rect)
		if self in hits:
			hits.remove(self)
		return hits
	
	def update_rect(self):
		self.update_hit_rect()
		self.rect.center = self.hit_rect.center
	
	def update_hit_rect(self,direction=Vector2(1,1)):
		if direction.x: self.hit_rect.centerx = self.pos.x
		if direction.y: self.hit_rect.centery = self.pos.y
	
	def collide_hit_rect(self,one, two):
		return one.hit_rect.colliderect(two.hit_rect)






class RigidBody(Collider):
	def __init__(self,x,y,w,h,maxforce,physics,material=PhysicMaterial(),
			mass=1.5,kinematic=False,freezeX=False,freezeY=False,scene=None):
		
		Collider.__init__(self,x,y,w,h,physics,material=material,scene=scene)
		
		self.mass = mass
		self.kinematic = kinematic
		self.freezeX = freezeX
		self.freezeY = freezeY
		self.maxforce = maxforce
		
		self.velocity = Vector2(0,0)
		self.physics = physics
	
	
	def addForce(self,direction=Vector2(0,0)):
		self.velocity += direction/self.mass
	
	def impulse(self,xforce=Vector2(0,0),yforce=Vector2(0,0)):
		if self.right_wall!=None:
			self.right_wall = None
			self.addForce(-xforce)
			if isinstance(self.right_wall,RigidBody):
				self.right_wall.addForce(xforce)
		if self.left_wall !=None:
			self.left_wall = None
			self.addForce(xforce)
			if isinstance(self.left_wall,RigidBody):
				self.left_wall.addForce(-xforce)
		if self.roof != None:
			self.roof = None
			self.addForce(yforce)
			if isinstance(self.roof,RigidBody):
				self.roof.addForce(-yforce)
		if self.floor != None:
			self.floor = None
			self.addForce(-yforce)
			if isinstance(self.floor,RigidBody):
				self.floor.addForce(yforce)
	
	def gravity(self):
		if not self.kinematic:
			self.velocity.x += self.physics.gravity.x*self.physics.delta
			self.velocity.y += self.physics.gravity.y*self.physics.delta
	
	def velocity_fix(self):
		if self.velocity.x>self.maxforce:    self.velocity.x=self.maxforce
		elif self.velocity.x<-self.maxforce: self.velocity.x=-self.maxforce
		if self.velocity.y>self.maxforce:    self.velocity.y=self.maxforce
		elif self.velocity.y<-self.maxforce: self.velocity.y=-self.maxforce
		
	
	def move(self):
		if not self.freezeX:
			self.pos.x += self.velocity.x * self.physics.delta
		if not self.freezeY:
			self.pos.y += self.velocity.y * self.physics.delta
	
	def bounce(self,hit,d=(0,0),ex=True):
		if d[0]:
			self.velocity.x = (-hit.physics_material.bounce-self.physics_material.bounce)*self.velocity.x/self.mass
		if d[1]:
			self.velocity.y = (-hit.physics_material.bounce-self.physics_material.bounce)*self.velocity.y/self.mass
		if isinstance(hit,RigidBody) and ex:
			hit.bounce(self,d=d,ex=False)
			
	def stop(self,hit,left=0,right=0,top=0,bottom=0):
		if left:
			self.pos.x = hit.rect.right + self.rect.width / 2
		if right:
			self.pos.x = hit.rect.left - self.rect.width / 2
		if top:
			self.pos.y = hit.rect.bottom + self.rect.height / 2
		if bottom:
			self.pos.y = hit.rect.top - self.rect.height / 2
	
	def onCollisionLeft(self,hit):
		self.stop(hit,left=1)
		self.left_wall = hit
		self.bounce(hit,d=(1,0))
	def onCollisionRight(self,hit):
		self.stop(hit,right=1)
		self.right_wall = hit
		self.bounce(hit,d=(1,0))
	def onCollisionTop(self,hit):
		self.stop(hit,top=1)
		self.roof = hit
		self.bounce(hit,d=(0,1))
	def onCollisionBottom(self,hit):
		self.stop(hit,bottom=1)
		self.floor = hit
		self.bounce(hit,d=(0,1))
	
	def onCollisionLeftExit(self):
		self.left_wall = None
	def onCollisionRightExit(self):
		self.right_wall = None
	def onCollisionTopExit(self):
		self.roof = None
	def onCollisionBottomExit(self):
		self.floor = None
	
	def onCollisionExit(self):
		self.floor = None
		self.right_wall = None
		self.left_wall = None
		self.roof = None
	def onCollisionEnter(self):pass
	
	def collision(self,hits,direction=Vector2(1,1)):
		for hit in hits:
			if hit != self:
				self.onCollisionEnter()
				if direction.x:
					if hit.rect.centerx >= self.hit_rect.centerx and hit.physics_material.left and self.velocity.x>0:
						self.onCollisionRight(hit)
					else:
						self.onCollisionRightExit()
					if hit.rect.centerx <= self.hit_rect.centerx and hit.physics_material.right and self.velocity.x<0:
						self.onCollisionLeft(hit)
					else:
						self.onCollisionLeftExit()
				if direction.y:
					if hit.rect.centery >= self.hit_rect.centery and hit.physics_material.up and self.velocity.y>0:
						self.onCollisionBottom(hit)
					else:
						self.onCollisionBottomExit()
					if hit.rect.centery <= self.hit_rect.centery and hit.physics_material.down and self.velocity.y<0:
						self.onCollisionTop(hit)
					else:
						self.onCollisionTopExit()
	
	
	def friction(self):
		if self.floor:
			self.velocity.x += -self.velocity.x*self.floor.physics_material.friction
		if self.roof:
			self.velocity.x += -self.velocity.x*self.roof.physics_material.friction
		if self.right_wall:
			self.velocity.y += -self.velocity.y*self.right_wall.physics_material.friction
		if self.left_wall:
			self.velocity.y += -self.velocity.y*self.left_wall.physics_material.friction
	
	
	def physics_update(self,delta=0):
		if self.velocity.x >= 0:
			self.onCollisionLeftExit()
		if self.velocity.x <= 0:
			self.onCollisionRightExit()
		if self.velocity.y > self.physics.gravity.y/10:
			self.onCollisionTopExit()
		if self.velocity.y < -self.physics.gravity.y/10:
			self.onCollisionBottomExit()
		
		self.gravity()
		self.friction()
		self.velocity_fix()
		self.move()
		
		




class KinematicBody(Collider):
	def __init__(self,x,y,w,h,physics,scene=None,
			material=PhysicMaterial(),freezeX=None,freezeY=None):
		
		Collider.__init__(self,x,y,w,h,material=material,scene=scene)
		
		self.freezeX = freezeX
		self.freezeY = freezeY
		
		self.velocity = Vector2(0,0)
		
	
	def move(self,delta=0):
		if not self.freezeX:
			if self.physics!=None:
				self.pos.x += self.velocity.x * self.physics.delta
			else:
				self.pos.x += self.velocity.x * delta
		if not self.freezeY:
			if self.physics!=None:
				self.pos.y += self.velocity.y * self.physics.delta
			else:
				self.pos.y += self.velocity.y * delta
	
	
	def physics_update(self,delta=0):
		self.move(delta)
	
	def stop(self,hit,left=0,right=0,top=0,bottom=0):
		if left:
			self.pos.x = hit.rect.right + self.rect.width / 2
		if right:
			self.pos.x = hit.rect.left - self.rect.width / 2
		if top:
			self.pos.y = hit.rect.bottom + self.rect.height / 2
		if bottom:
			self.pos.y = hit.rect.top - self.rect.height / 2
	
	def onCollisionBottom(self,hit):
		self.stop(hit,bottom=1)
		self.velocity.y = 0
	def onCollisionLeft(self,hit):
		self.stop(hit,left=1)
		self.velocity.x = 0
	def onCollisionRight(self,hit):
		self.stop(hit,right=1)
		self.velocity.x = 0
	def onCollisionTop(self,hit):
		self.stop(hit,top=1)
		self.velocity.y = 0
	
	def onCollisionLeftExit(self):pass
	def onCollisionRightExit(self):pass
	def onCollisionTopExit(self):pass
	def onCollisionBottomExit(self):pass
	
	def onCollisionExit(self):pass
	def onCollisionEnter(self):pass
	
	def collision(self,hits,direction=Vector2(1,1)):
		for hit in hits:
			if hit != self:
				self.onCollisionEnter()
				if direction.x:
					if hit.rect.centerx > self.hit_rect.centerx:
						if hit.physics_material.left and self.velocity.x>0:
							self.onCollisionRight(hit)
					else:
						self.onCollisionRightExit()
					if hit.rect.centerx < self.hit_rect.centerx:
						if hit.physics_material.right and self.velocity.x<0:
							self.onCollisionLeft(hit)
					else:
						self.onCollisionLeftExit()
				if direction.y:
					if hit.rect.centery > self.hit_rect.centery:
						if hit.physics_material.up and self.velocity.y>0:
							self.onCollisionBottom(hit)
					else:
						self.onCollisionBottomExit()
					if hit.rect.centery < self.hit_rect.centery:
						if hit.physics_material.down and self.velocity.y<0:
							self.onCollisionTop(hit)
					else:
						self.onCollisionTopExit()


		





class Physics(threading.Thread):
	def __init__(self,cps=60,gravity=Vector2(0,98),timefactor=5):
		threading.Thread.__init__(self)
		self.alive = threading.Event()
		self.alive.set()
	
		self.gravity = gravity
		self.cps = cps
		self.timefactor = timefactor
		
		self.rigid_bodies = []
		self.kinematic_bodies = []
		self.colliders = pygame.sprite.Group()
		self.static_colliders = pygame.sprite.Group()
		self.clock = None
		self.delta = 0
		self.current_cps = 0
		
	def addBodies(self,objs):
		for obj in objs:
			self.addBody(obj)
	
	def addColliders(self,objs):
		for obj in objs:
			self.addCollider(obj)
	
	def addBody(self,obj):
		if isinstance(obj,RigidBody):
			self.rigid_bodies.append(obj)
			#~ print("added [{}] in rigidbodies list".format(obj)) 
		if isinstance(obj,KinematicBody):
			self.kinematic_bodies.append(obj)
	
	def addCollider(self,obj):
		if isinstance(obj,Collider):
			if obj not in self.colliders:
				self.colliders.add(obj)
				if not isinstance(obj,RigidBody):
					self.static_colliders.add(obj)
				#~ print("added [{}] in colliders list".format(obj))
	
	def clear(self):
		self.rigid_bodies = []
		self.colliders = pygame.sprite.Group()
		self.static_colliders = pygame.sprite.Group()
	
	def removeBody(self,obj):
		if obj in self.rigid_bodies:
			self.rigid_bodies.remove(obj)
		if obj in self.kinematic_bodies:
			self.kinematic_bodies.remove(obj)
	
	def removeCollider(self,obj):
		if obj in self.colliders:
			self.colliders.remove(obj)
	
	def run(self):
		self.alive.wait()
		self.clock = pygame.time.Clock()
		lastdelta = time.time()
		
		while self.alive.isSet():
			if self.delta != 0:
				for kb in self.kinematic_bodies:
					kb.physics_update(delta=self.delta)
					if kb in self.colliders:
						kb.update_hit_rect(Vector2(1,0))
						kb.collision(kb.group_collision(self.colliders),direction=Vector2(1,0))
						kb.update_rect()
						kb.collision(kb.group_collision(self.colliders),direction=Vector2(0,1))
					kb.update_rect()
				for rb in self.rigid_bodies:
					rb.physics_update()
					if rb in self.colliders:
						if rb.group_collision(self.colliders) == []:rb.onCollisionExit()
						rb.update_hit_rect(Vector2(1,0))
						rb.collision(rb.group_collision(self.colliders),direction=Vector2(1,0))
						rb.update_rect()
						rb.collision(rb.group_collision(self.colliders),direction=Vector2(0,1))
					rb.update_rect()
			
			self.clock.tick(self.cps)
			self.current_cps = self.clock.get_fps()
			self.delta = (time.time() - lastdelta)*self.timefactor
			lastdelta = time.time()
		
		
	def stop(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)
