import pygame
from pygame.locals import *
from settings import *

NORMALIZED_MVMT = 0.707107

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacles):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/Player/Color1/Outline/PNGSheets/idle/right_0.png')
		self.image = pygame.transform.scale(self.image, (64,80))

		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.inflate(-30,-50) #changes sprite's hitbox to allow sprites to overlap a bit

		#Player movement variables
		self.pos_offset = [0, 0]
		self.speed = 7
		self.obstacles = obstacles

		#Player animation variables
		self.direction = "right"
		self.counter = 0
		self.animation_cooldown = 60
		self.time_of_last_animation_frame = pygame.time.get_ticks()

	def update(self):
		self.get_mvmt()
		self.check_collision()
		self.animate()
		self.move_player()

	def get_mvmt(self):
		self.hitbox = self.rect.inflate(-30,-50)
		#if no movement key is pressed, there should be no offset
		self.pos_offset = [0, 0]
		keys = pygame.key.get_pressed()

		#check for horizontal movement
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.pos_offset[0] = -1
			self.direction = "left"
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.pos_offset[0] += 1
			self.direction = "right"
		#check for vertical movement
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.pos_offset[1] = -1
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.pos_offset[1] += 1

	def check_collision(self):
		test_player = Rect(self.hitbox[:])	#makes shallow copy

		#check if horizontal movement will cause collision
		test_player[0] += (self.pos_offset[0] * self.speed)
		for obstacle in self.obstacles:
				if pygame.Rect.colliderect(obstacle.rect, test_player):
					self.pos_offset[0] = 0
					test_player[0] = self.hitbox[0]
		#check if vertical movement will cause collision
		test_player[1] += (self.pos_offset[1] * self.speed)
		for obstacle in self.obstacles:
				if pygame.Rect.colliderect(obstacle.rect, test_player):
					self.pos_offset[1] = 0

	def move_player(self):
		if self.pos_offset[0] and self.pos_offset[1]:
			self.pos_offset = [self.pos_offset[0] / abs(self.pos_offset[0]) * NORMALIZED_MVMT, self.pos_offset[1] / abs(self.pos_offset[1]) * NORMALIZED_MVMT]

		self.rect[0] += round(self.pos_offset[0] * self.speed)
		self.rect[1] += round(self.pos_offset[1] * self.speed)

	def animate(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.time_of_last_animation_frame) > self.animation_cooldown:
			#character is moving left/right
			if self.pos_offset[0] or self.pos_offset[1]:
				self.image = pygame.transform.scale_by(pygame.image.load('../graphics/Player/Color1/NoOutline/PNGSheets/running/' + self.direction + '_' + str(self.counter) + '.png'), 2)
			#character is idle
			else:
				self.image = pygame.transform.scale_by(pygame.image.load('../graphics/Player/Color1/Outline/PNGSheets/idle/' + self.direction + '_' + str(self.counter) + '.png'), 2)
				
			if self.counter == 9:
					self.counter = 0
			else:
				self.counter += 1

			#update time of last time animation frame was played
			self.time_of_last_animation_frame = current_time