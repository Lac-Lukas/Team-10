import pygame, sys
from settings import * 
from button import Button
from level import Level
import _pickle as cPickle

class mainmenu:
	def __init__(self, SCREEN):
		
		self.level = Level()
		self.menuIsOn = True
		self.BG = pygame.image.load("../graphics/background_upscaled.png")
		self.currentState = 0
        # pygame.init()
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #creates display surface and a clock
        # pygame.display.set_caption('RPG')
        # self.clock = pygame.time.Clock()
        # self.level = Level()
	def run(self, SCREEN, CLOCK, MENUTEXT):
		while self.menuIsOn == True:
			SCREEN.blit(self.BG, (0, 0))
			MENU_MOUSE_POS = pygame.mouse.get_pos()

			MENU_TEXT = pygame.font.Font(UI_FONT, 100).render(MENUTEXT, True, "#b68f40")
			MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))



			NEW_GAME_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 250), 
								text_input="NEW GAME", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			RESUME_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 250), 
								text_input="RESUME", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")			
			LOAD_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 400), 
								text_input="LOAD GAME", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			OPTIONS_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 400), 
								text_input="OPTIONS", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			# SAVE_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(1200, 250), 
			# 					text_input="SAVE GAME", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			QUIT_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 550), 
								text_input="QUIT", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")


			# SAVE_1 = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 250), 
			# 					text_input="SAVE 1", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			# SAVE_2 = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 400), 
			# 					text_input="SAVE 2", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			# SAVE_3 = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 550), 
			# 					text_input="SAVE 3", font=pygame.font.Font(UI_FONT, 50), base_color="#d7fcd4", hovering_color="White")
			

			if (MENUTEXT == "Try again?"):
				self.BG = pygame.image.load("../graphics/lose_background.png")
				for button in [NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
					button.imageActive = True
					button.changeColor(MENU_MOUSE_POS)
					button.update(SCREEN)				
			elif (MENUTEXT == "You win!!!"):
				self.BG = pygame.image.load("../graphics/win_background.png")
				for button in [NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
					button.imageActive = True
					button.changeColor(MENU_MOUSE_POS)
					button.update(SCREEN)
			elif (MENUTEXT == "Paused"):
				self.BG = pygame.image.load("../graphics/win_background.png")
				for button in [RESUME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
					button.imageActive = True
					button.changeColor(MENU_MOUSE_POS)
					button.update(SCREEN)
			# elif (MENUTEXT == "SELECT A SAVE SLOT"):
			# 	self.BG = pygame.image.load("../graphics/win_background.png")
			# 	self.currentState = 1
			# 	for button in [SAVE_1, SAVE_2, SAVE_3]:
			# 		button.imageActive = True
			# 		button.changeColor(MENU_MOUSE_POS)
			# 		button.update(SCREEN)	
			# elif (MENUTEXT == "LOAD SAVE FILE"):
			# 	self.BG = pygame.image.load("../graphics/win_background.png")
			# 	self.currentState = 2
			# 	for button in [SAVE_1, SAVE_2, SAVE_3]:
			# 		button.imageActive = True
			# 		button.changeColor(MENU_MOUSE_POS)
			# 		button.update(SCREEN)											
			else:
				self.BG = pygame.image.load("../graphics/background_upscaled.png")
				for button in [NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
					button.imageActive = True
					button.changeColor(MENU_MOUSE_POS)
					button.update(SCREEN)				



			SCREEN.blit(MENU_TEXT, MENU_RECT)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if NEW_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.rungame(SCREEN, CLOCK)
					if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.rungame(SCREEN, CLOCK)
					# if LOAD_BUTTON.checkForInput(MENU_MOUSE_POS):
					# 	print("loading save")
					# 	self.run(SCREEN, CLOCK, "LOAD SAVE FILE")	
					if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
						print("options")
						self.rungame(SCREEN, CLOCK)
						
					# if SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
					# 	print("saving save")
					# 	self.run(SCREEN, CLOCK, "SELECT A SAVE SLOT")
						

					# if (SAVE_1.checkForInput(MENU_MOUSE_POS) and self.currentState == 1):
					# 	self.currentState = 0
					# 	print("saving save 1")
					# 	with open('../Saves/save1.sav', 'wb') as outp:
					# 		cPickle.dump(self.level.player, outp)					
					# 	self.rungame(SCREEN, CLOCK)	
						
					# if (SAVE_2.checkForInput(MENU_MOUSE_POS) and self.currentState == 1):
					# 	self.currentState = 0
					# 	print("saving save 2")
					# 	with open('../Saves/save2.sav', 'wb') as outp:
					# 		cPickle.dump(self.level, outp)							
					# 	self.rungame(SCREEN, CLOCK)
						
					# if (SAVE_3.checkForInput(MENU_MOUSE_POS) and self.currentState == 1):
					# 	self.currentState = 0	
					# 	print("saving save 3")
					# 	with open('../Saves/save3.sav', 'wb') as outp:
					# 		cPickle.dump(self.level, outp)							
					# 	self.rungame(SCREEN, CLOCK)
						

					# if (SAVE_1.checkForInput(MENU_MOUSE_POS) and self.currentState == 2):
					# 	self.currentState = 0
					# 	print("loading save 1")
					# 	self.rungame(SCREEN, CLOCK)
						
					# if (SAVE_2.checkForInput(MENU_MOUSE_POS) and self.currentState == 2):
					# 	self.currentState = 0
					# 	print("loading save 2")
					# 	self.rungame(SCREEN, CLOCK)
						
					# if (SAVE_3.checkForInput(MENU_MOUSE_POS) and self.currentState == 2):
					# 	self.currentState = 0
					# 	print("loading save 3")
					# 	self.rungame(SCREEN, CLOCK)	
						

					if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
						pygame.quit()
						sys.exit()

			pygame.display.update()

	def rungame(self, SCREEN, CLOCK):
		print("starting game")
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						print("pausing")	
						self.run(SCREEN, CLOCK, "Paused")	
					if event.key == pygame.K_h:
						self.level.player.use_health_potion()	
				if self.level.game_lose == True:
					print("it's all over")	
					self.level.reset()						
					self.run(SCREEN, CLOCK, "Try again?")
				if self.level.game_win == True:
					print("you win!")	
					self.level.reset()						
					self.run(SCREEN, CLOCK, "You win!!!")										
			SCREEN.fill('black')
			self.level.run()
			pygame.display.update()
			CLOCK.tick(FPS)