import pygame, sys
from settings import * 
from button import Button
from level import Level

class mainmenu:
	def __init__(self, SCREEN):
		self.level = Level()
		self.menuIsOn = True
		self.BG = pygame.image.load("../Levels/Level_0/Ground.png")
        # pygame.init()
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #creates display surface and a clock
        # pygame.display.set_caption('RPG')
        # self.clock = pygame.time.Clock()
        # self.level = Level()
	def run(self, SCREEN, CLOCK):
		while self.menuIsOn == True:
			SCREEN.blit(self.BG, (0, 0))
			MENU_MOUSE_POS = pygame.mouse.get_pos()

			MENU_TEXT = pygame.font.Font(UI_FONT, 100).render("MAIN MENU", True, "#b68f40")
			MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

			PLAY_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 250), 
								text_input="PLAY", font=pygame.font.Font(UI_FONT, 75), base_color="#d7fcd4", hovering_color="White")
			OPTIONS_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 400), 
								text_input="OPTIONS", font=pygame.font.Font(UI_FONT, 75), base_color="#d7fcd4", hovering_color="White")
			QUIT_BUTTON = Button(image=pygame.image.load('../graphics/Play Rect.png'), pos=(640, 550), 
								text_input="QUIT", font=pygame.font.Font(UI_FONT, 75), base_color="#d7fcd4", hovering_color="White")

			SCREEN.blit(MENU_TEXT, MENU_RECT)

			for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
				button.changeColor(MENU_MOUSE_POS)
				button.update(SCREEN)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
						while True:
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit()
									sys.exit()
							SCREEN.fill('black')
							self.level.run()
							pygame.display.update()
							CLOCK.tick(FPS)
						#self.menuIsOn = False
						#self.level.run()
					if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
						options()
					if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
						pygame.quit()
						sys.exit()

			pygame.display.update()