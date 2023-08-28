import pygame
from settings import *
from button import Button

class UI:
	def __init__(self):

		# general
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup
		self.health_bar_rect = pygame.Rect(10,10, 300, 20)
		self.energy_bar_rect = pygame.Rect(10,34, 150, 20)

		#convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)


	def show_bar(self,current,max_amount,bg_rect,color):
		# draw bg
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width
		# drawing the bar
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface, BAR_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp):
		text_surf = self.font.render("XP: " + str(int(exp)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface, BAR_BORDER_COLOR,text_rect.inflate(20,20),3)

	def show_gold(self, gold):
		text_surf = self.font.render("Gold: " + str(int(gold)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 100
		text_rect = text_surf.get_rect(topright = (x, y))

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface, BAR_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.display_surface, BAR_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf,weapon_rect)

	def healthSymbolOverlay(self):
		bg_rect = pygame.Rect(310, 5, 32, 32)
		image = pygame.image.load('../graphics/UISymbols/HealthUIBlack.png')
		image_rect = image.get_rect(center = bg_rect.center)
		self.display_surface.blit(image, image_rect)

	def staminaSymbolOverlay(self):
		bg_rect = pygame.Rect(160, 29, 32, 32)
		image = pygame.image.load('../graphics/UISymbols/stamina.png')
		image_rect = image.get_rect(center = bg_rect.center)
		self.display_surface.blit(image, image_rect)

	def healthPotionOverlay(self, health_potion_count):
		bg_rect = pygame.Rect(10, 590, 38, 38)
		image = pygame.image.load('../graphics/UISymbols/Healthpotion.png')
		image_rect = image.get_rect(center = bg_rect.center)
		self.display_surface.blit(image, image_rect)

		text = self.font.render(health_potion_count, True, "#d7fcd4")
		#self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		#self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.display_surface.blit(text, image_rect)

	def display(self,player):
		self.show_bar(player.currentHealth, player.maxStats['maxHealth'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.currentEnergy, player.maxStats['maxEnergy'],self.energy_bar_rect,ENERGY_COLOR)

		self.show_exp(player.exp)
		self.show_gold(player.gold)

		self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
		self.healthSymbolOverlay()
		self.staminaSymbolOverlay()
		self.healthPotionOverlay(player.health_potion_count)
		# self.selection_box(80,635) # magic