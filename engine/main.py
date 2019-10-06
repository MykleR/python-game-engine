#!/usr/local/bin/python
#-*- coding: utf-8 -*-
from engine.engine_lib import *

from engine.__init__ import *


pygame.init()




class Engine(threading.Thread):
	def __init__(self,display,mainscene,
			physics=Physics(),fps=60,flags=0,title="Window"):
		
		threading.Thread.__init__(self)
		
		self.DISPLAY = display
		self.XWIN,self.YWIN = display
		self.FPS = fps
		self.FLAGS = flags
		self.TITLE = title
		
		self.drawer = Drawer(fps)
		self.physics = physics
		self.physics.cps = fps
		self.main_scene = mainscene
		
		self.scene = None
		self.alive = threading.Event()
		
		
	#---EVENTS---
	def onUpdate(self):pass
	def onStart(self):pass
	
	#---TOOLS---
	def applyX(self,x,res=1280):
		return int(self.XWIN/(res/x))
	def applyY(self,y,res=720):
		return int(self.YWIN/(res/y))
	def applyXY(self,x,xres=1280,yres=720):
		return int(self.XWIN*self.YWIN/(xres*yres/x))
	
	def change_physics(self,new):
		self.physics.clear()
		self.physics.stop()
		self.physics = new
		self.physics.start()


	#======== START ========

	def _print_start(self):
		print("-------------------------")
		print(" Welcom on {0}".format(self.TITLE))
		print("-------------------------")

	def _set_display(self):
		self.clock = pygame.time.Clock()
		self.drawer.window = pygame.display.set_mode(self.DISPLAY,self.FLAGS)
		pygame.display.set_caption(self.TITLE)

	#----- START MAIN -----
	def start(self):
		self.onStart()
		self.ready()
		threading.Thread.start(self)
	
	def ready(self):
		try:
			self._print_start()
		
			self._set_display()
			self.drawer.start()
			self.physics.start()
		
			self.load_scene(self.main_scene)
			self.alive.set()
		except:
			print("Something went wrong while initialising Engine")
		
		
	#======== RUN ========
	
	def load_scene(self,scene):
		self.drawer.clear()
		self.physics.clear()
		self.scene = scene(self)
		self.scene.start()
	
	#----- RUN MAIN -----
	def run(self):
		self.alive.wait()
		
		while self.alive.isSet():
			#~ print(int(self.drawer.current_fps),int(self.physics.current_cps))
			self.onUpdate()
			self.scene.run()
			self.clock.tick(self.FPS)
	
	def stop(self,timeout=None):
		self.drawer.stop(timeout)
		self.physics.stop(timeout)
		self.alive.clear()
	
	
