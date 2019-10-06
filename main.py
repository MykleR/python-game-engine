from engine.main import *
from game_classes import Player,Block,TopDownPlayer


class Game(Scene):
	
	def __init__(self,e):
		Scene.__init__(self,e)
		
		self.engine.change_physics(Physics(gravity=Vector2(0,98)))
		
		self.player = Player(350,300,30,50,RED,self.engine.physics,scene=self)
		#LEVEL (ground,platforms...)
		plt = Block(1000,400,200,25,GREY,scene=self,material=PhysicMaterial(down=False,right=False,left=False))
		plt2 = Block(650,300,350,25,GREY,scene=self,material=PhysicMaterial(down=False,right=False,left=False))
		plt3 = Block(300,400,200,25,GREY,scene=self,material=PhysicMaterial(down=False,right=False,left=False))
		wall = Block(0,self.engine.YWIN/2,50,700,GREY,scene=self,material=PhysicMaterial(friction=0.3))
		wall2 = Block(1280,self.engine.YWIN/2,50,700,GREY,scene=self,material=PhysicMaterial(friction=0.3))
		wall3 = Block(150,250,25,300,GREY,scene=self,material=PhysicMaterial(friction=0.3))
		ground = Block(640,700,1280,370,GRASS,scene=self,material=PhysicMaterial(bounce=0.3))
		
		
	def start(self):
		self.add(SKY)
	
	def onEventStay(self,event):
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.engine.load_scene(Menu)
			if event.key == K_b:
				self.engine.drawer.hitbox = not self.engine.drawer.hitbox
	

class Game2(Scene):
	
	def __init__(self,e):
		Scene.__init__(self,e)
		
		self.engine.change_physics(Physics(gravity=Vector2(0,0)))
		
		ground = Block(640,700,1280,370,GRASS,scene=self)
		plt = Block(1000,400,200,25,GREY,scene=self)
		self.player = TopDownPlayer(350,300,30,50,RED,self.engine.physics,scene=self)
	
	def start(self):
		self.add(SKY)
	
	def onUpdateExit(self):
		self.player.pos.x = self.player.pos.x%self.engine.XWIN
	
	def onEventStay(self,event):
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.engine.load_scene(Menu)
			if event.key == K_b:
				self.engine.drawer.hitbox = not self.engine.drawer.hitbox
		



class Menu(Scene):
	
	def __init__(self,e):
		Scene.__init__(self,e)
		
		space = self.engine.applyY(100)
		title_size = self.engine.XWIN/15+self.engine.YWIN/15
		button_text_size = int(self.engine.XWIN/50+self.engine.YWIN/50)
		
		self.text_title = TextSprite(self.engine.XWIN/3,# X coords
			self.engine.applyY(100),					# Y coords
			title_size,									# Size
			WHITE,										# Color
			txt=self.engine.TITLE,scene=self)						# String
		
		self.button_play = Button(self.engine.XWIN/2,self.engine.YWIN/2,# X,Y coords
			self.engine.applyX(250),self.engine.applyY(70),				# Width, Height
			ALPHA,LIGHT_GREY,												# Colors
			TextSprite(self.engine.applyX(100),							# Text
				self.engine.applyY(70)/2,
				button_text_size,
				WHITE,txt="PLAY"),scene=self)
		
		self.button_option = Button(self.engine.XWIN/2,self.engine.YWIN/2+space,# X,Y coords
			self.engine.applyX(250),self.engine.applyY(70),				# Width, Height
			ALPHA,LIGHT_GREY,												# Colors
			TextSprite(self.engine.applyX(80),							# Text
				self.engine.applyY(70)/2,
				button_text_size,
				WHITE,txt="PLAY 2"),scene=self)
		
		self.button_quit = Button(self.engine.XWIN/2,self.engine.YWIN/2+space*2,# X,Y coords
			self.engine.applyX(250),self.engine.applyY(70),				# Width, Height
			ALPHA,LIGHT_GREY,											# Colors
			TextSprite(self.engine.applyX(100),							# Text
				self.engine.applyY(70)/2,
				button_text_size,
				WHITE,txt="QUIT"),scene=self)
		
	
	def onStart(self):
		self.add(SKY)
		
	def onUpdateEnter(self):
		if self.button_play.pressed:
			self.engine.load_scene(Game)
		if self.button_quit.pressed:
			self.engine.stop()
		if self.button_option.pressed:
			self.engine.load_scene(Game2)
	




engine = Engine((1280,720),Menu,title="Super Mario")
engine.start()
	

