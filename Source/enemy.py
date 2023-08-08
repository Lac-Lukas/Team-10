import pygame
from pygame.locals import *
from settings import *

NORMALIZED_MVMT = 0.707107

class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacles, player):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/Player/Color1/Outline/PNGSheets/idle/right_0.png')
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-25)

		#load animation frames
		self.idle_r = self.load_frames('../graphics/Enemies/Minotaur/idle/', 4)
		self.running_r = self.load_frames('../graphics/Enemies/Minotaur/running/', 7)
		self.death_r = self.load_frames('../graphics/Enemies/Minotaur/death/', 5)
		self.attack_r = self.load_frames('../graphics/Enemies/Minotaur/attack/', 8)

		#movement variables
		self.speed = 3
		self.pos_offset = [0, 0]
		self.player_pos = player.rect
		self.obstacles = obstacles

		#animation variables
		self.direction = "right"
		self.frame_counter = 0
		self.animation_cooldown = 60
		self.time_of_last_animation_frame = pygame.time.get_ticks()
		self.idle_frame_counter = 0
		self.running_frame_counter = 0
		self.death_frame_counter = 0
		self.attack_frame_counter = 0

		#combat variables
		self.health = 3
		self.attack_dmg = 10
		self.aggro_dist = 300
		self.attack_dist = 100
		self.attacking = False
		self.attack_cooldown = 600
		self.attack_time = 0
		self.player_obj = player

		#indication when enemy can be deleted
		self.has_death_animation_played = False

	def load_frames(self, path, max_frame_num):
		return [pygame.transform.scale_by(pygame.image.load(path + 'right_' + str(x) + '.png'), 2) for x in range(max_frame_num + 1)]

	def update(self):
		if self.player_obj.is_alive() and self.is_alive():
			self.pos_offset = [0, 0]
			if self.within_range(self.aggro_dist):
				self.move_towards_player()
				self.check_collision()
				self.move()
			if self.within_range(self.attack_dist):
				current_time = pygame.time.get_ticks()
				if not self.attacking and (current_time - self.attack_time > self.attack_cooldown):
					self.attack_time = current_time
					self.attack_frame_counter = 0
					self.attacking = True
		if self.is_alive():
			self.animate()
		else:
			self.death()

	def is_alive(self):
		return self.health > 0

	def move_towards_player(self):
		self.hitbox = self.rect.inflate(0,-25)
		player_pos_x, player_pos_y = self.player_pos[0], self.player_pos[1]

		if abs(self.rect[0] - player_pos_x) > self.speed:
			if self.rect[0] < player_pos_x:
				self.pos_offset[0] = 1
				self.direction = "right"
			elif self.rect[0] > player_pos_x:
				self.pos_offset[0] = -1
				self.direction = "left"
		if abs(self.rect[1] - player_pos_y) > self.speed:
			if self.rect[1] < player_pos_y:
				self.pos_offset[1] = 1
			elif self.rect[1] > player_pos_y:
				self.pos_offset[1] = -1
	
	def check_collision(self):
		test_enemy = Rect(self.hitbox[:])

		#check if horizontal movement will cause collision
		test_enemy[0] += (self.pos_offset[0] * self.speed)
		for obstacle in self.obstacles:
				if pygame.Rect.colliderect(obstacle.rect, test_enemy):
					self.pos_offset[0] = 0
					test_enemy[0] = self.hitbox[0]
		#check if vertical movement will cause collision
		test_enemy[1] += (self.pos_offset[1] * self.speed)
		for obstacle in self.obstacles:
				if pygame.Rect.colliderect(obstacle.rect, test_enemy):
					self.pos_offset[1] = 0

	def animate(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.time_of_last_animation_frame) > self.animation_cooldown:
			if self.attacking:
				self.attack_animation()

			else:
				#character is moving left/right
				if self.pos_offset[0] or self.pos_offset[1]:
					self.image = pygame.transform.flip(self.running_r[self.running_frame_counter], self.direction == 'left', False)
					self.running_frame_counter = (self.running_frame_counter + 1) % 8
					
				#character is idle
				else:
					self.image = pygame.transform.flip(self.idle_r[self.idle_frame_counter], self.direction == 'left', False)
					self.idle_frame_counter = (self.idle_frame_counter + 1) % 5
				# self.frame_counter += 1
				# self.frame_counter %= 10	#there are 10 animation frames

			#update time of last time animation frame was played
			self.time_of_last_animation_frame = current_time

	def move(self):
		if self.pos_offset[0] and self.pos_offset[1]:
			self.pos_offset = [self.pos_offset[0] / abs(self.pos_offset[0]) * NORMALIZED_MVMT, self.pos_offset[1] / abs(self.pos_offset[1]) * NORMALIZED_MVMT]

		self.rect[0] += round(self.pos_offset[0] * self.speed)
		self.rect[1] += round(self.pos_offset[1] * self.speed)

	def take_damage(self, damage):
		was_alive = (self.health >= 1)
		self.health -= damage

		if self.health <= 0  and was_alive:
			self.frame_counter = 0
	
	def attack_animation(self):
		self.image = pygame.transform.flip(self.attack_r[self.attack_frame_counter], self.direction == 'left', False)
		self.attack_frame_counter += 1

		if self.attack_frame_counter == 1:
			self.attack()
		
		if self.attack_frame_counter == 8:
			self.attacking = False
			self.attack_frame_counter = 0

	def attack(self):
		self.player_obj.take_damage(self.attack_dmg)

	def within_range(self, max_distance):
		player_pos_x, player_pos_y = self.player_pos[0], self.player_pos[1]
		return  (((self.hitbox[0] - player_pos_x)**2) + ((self.hitbox[1] - player_pos_y)**2)) ** 0.5 <= max_distance
	
	def death(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.time_of_last_animation_frame) > self.animation_cooldown and (self.death_frame_counter < 5):
			self.time_of_last_animation_frame = current_time
			self.image = pygame.transform.flip(self.death_r[self.death_frame_counter], self.direction == 'left', False)
			self.death_frame_counter += 1
		
		if self.death_frame_counter > 5:
			self.has_death_animation_played = True