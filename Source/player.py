import pygame
from pygame.locals import *
from settings import *


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacles):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/player_right.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.display_surface = pygame.display.get_surface()
		
		self.pos_offset = [0, 0]
		self.speed = 7
		self.obstacles = obstacles

	def get_mvmt(self):
		#if no movement key is pressed, there should be no offset
		self.pos_offset = [0, 0]
		keys = pygame.key.get_pressed()

		#check for horizontal movement
		if keys[pygame.K_LEFT]:
			self.pos_offset[0] = -1
		if keys[pygame.K_RIGHT]:
			self.pos_offset[0] += 1
		#check for vertical movement
		if keys[pygame.K_UP]:
			self.pos_offset[1] = -1
		if keys[pygame.K_DOWN]:
			self.pos_offset[1] += 1

	def check_collision(self):
		test_player = Rect(self.rect[:])	#makes shallow copy

		#check if horizontal movement will cause collision
		test_player[0] += (self.pos_offset[0] * self.speed)
		for obstacle in self.obstacles:
				if pygame.Rect.colliderect(obstacle.rect, test_player):
					self.pos_offset[0] = 0
					test_player[0] = self.rect[0]
		#check if vertical movement will cause collision
		test_player[1] += (self.pos_offset[1] * self.speed)
		for obstacle in self.obstacles:
				if pygame.Rect.colliderect(obstacle.rect, test_player):
					self.pos_offset[1] = 0

	
	def move_player(self):
		self.rect[0] += (self.pos_offset[0] * self.speed)
		self.rect[1] += (self.pos_offset[1] * self.speed)

	def update(self):
		self.get_mvmt()
		self.check_collision()
		self.move_player()