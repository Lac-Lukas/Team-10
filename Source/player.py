import pygame
from pygame.locals import *
from settings import *

NORMALIZED_MVMT = 0.707107
ATTACK_ENERGY_COST = 5
ROLL_ENERGY_COST = 15

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacles, enemies):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/Player/Color1/Outline/PNGSheets/idle/right_0.png')
		self.image = pygame.transform.scale(self.image, (64,80))

		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-30,-20) #changes sprite's hitbox to allow sprites to overlap a bit

		#load animation frames
		self.running_r = self.load_frames('../graphics/Player/Color1/Outline/PNGSheets/running/', 9)
		self.idle_r = self.load_frames('../graphics/Player/Color1/Outline/PNGSheets/idle/', 9)
		self.attack_r = self.load_frames('../graphics/Player/Color1/Outline/PNGSheets/attack/', 3)
		self.death_r = self.load_frames('../graphics/Player/Color1/Outline/PNGSheets/death/', 9)
		self.roll_r = self.load_frames('../graphics/Player/Color1/Outline/PNGSheets/roll/', 11)

		#Player movement variables
		self.pos_offset = [0, 0]
		self.speed = 7
		self.obstacles = obstacles

		#Player animation variables
		self.direction = "right"
		self.counter = 0	#counter will count up to 9
		self.animation_cooldown = 60
		self.roll_animation_cooldown = 40
		self.time_of_last_animation_frame = pygame.time.get_ticks()

		#Player attack variables
		self.weapon_index = 0 #  zero is sword should change to enum later

		self.can_switch_weapon = True
		self.attack_cooldown = 400
		self.attack_time = 0
		self.attacking = False
		self.attack_direction = "right"
		self.attack_dmg = 0.5
		
		# main stats for player
		self.maxStats = {'maxHealth': 100, 'maxEnergy':80, 'maxAttack': 10, 'maxMagic': 4, 'maxSpeed': 5}
		self.currentHealth = self.maxStats["maxHealth"]
		self.currentEnergy = self.maxStats["maxEnergy"]
		self.curentShield = 50
		self.exp = 0
		self.gold = 0
		self.currentSpeed = 9001

		#combat variables
		self.enemies = enemies
		self.roll_speed = 4
		self.is_rolling = False
		self.roll_time = 0
		self.roll_cooldown = 1000
		self.energy_recovery_rate = 1
	
	def load_frames(self, path, max_frame_num):
		return [pygame.transform.scale_by(pygame.image.load(path + 'right_' + str(x) + '.png'), 2) for x in range(max_frame_num+1)]

	def update(self):
		if self.is_rolling:
			self.hitbox = self.rect.inflate(-30,-20)
			self.check_collision()
			self.roll()
			self.move_player()
		elif self.is_alive():
			self.get_mvmt()
			self.check_collision()
			self.animate()
			self.move_player()
		elif self.counter < 10:	#death animation only has 10 frames
			self.death()

	def is_alive(self):
		return self.currentHealth > 0

	def get_mvmt(self):
		self.hitbox = self.rect.inflate(-30,-20)

		#if no movement key is pressed, there should be no offset
		self.pos_offset = [0, 0]
		keys = pygame.key.get_pressed()
		mouse_buttons = pygame.mouse.get_pressed() #checks for mouse input
		#check if player is rolling
		if keys[pygame.K_SPACE]:
			if self.is_rolling == False and (self.currentEnergy >= ROLL_ENERGY_COST):
				self.currentEnergy -= ROLL_ENERGY_COST
				self.is_rolling = True
				self.speed += self.roll_speed
				self.counter = 0
				self.attacking = False 	#don't want to queue an attack after rolling
		#check for horizontal movement
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.pos_offset[0] = -1
			self.direction = 'left'
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.pos_offset[0] += 1
			self.direction = 'right'
		#check for vertical movement
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.pos_offset[1] = -1
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.pos_offset[1] += 1
		#check if player is attacking
		if mouse_buttons[0]:
			current_time = pygame.time.get_ticks()
			if not self.attacking and (current_time - self.attack_time > self.attack_cooldown) and self.currentEnergy >= ATTACK_ENERGY_COST:
				self.currentEnergy -= ATTACK_ENERGY_COST
				self.counter = 0
				self.attack_time = current_time
				self.attack_direction = self.direction
				self.attacking = True
		if keys[pygame.K_q] and self.can_switch_weapon:
			self.can_switch_weapon = False
			self.weapon_switch_time = pygame.time.get_ticks()
			
			if self.weapon_index < len(list(weapon_data.keys())) - 1:
				self.weapon_index += 1
			else:
				self.weapon_index = 0
					
			self.weapon = list(weapon_data.keys())[self.weapon_index]		

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
			if self.attacking:
				self.attack_animation()

			else:
				#character is moving left/right
				if self.currentEnergy < self.maxStats["maxEnergy"]:
						self.currentEnergy += (self.energy_recovery_rate / 5)

				if self.pos_offset[0] or self.pos_offset[1]:
					self.image = pygame.transform.flip(self.running_r[self.counter], self.direction == 'left', False)
				#character is idle
				else:
					if self.currentEnergy < self.maxStats["maxEnergy"]:
						self.currentEnergy += self.energy_recovery_rate
					self.image = pygame.transform.flip(self.idle_r[self.counter], self.direction == 'left', False)
				self.counter = (self.counter + 1) % 10	#these animations have 10 frames

			#update time of last time animation frame was played
			self.time_of_last_animation_frame = current_time
	
	def attack_animation(self):
		self.image = pygame.transform.flip(self.attack_r[self.counter], self.attack_direction == 'left', False)
		self.counter += 1

		if self.counter == 1 or self.counter == 2:
			self.attack()
		
		if self.counter == 3:
			self.attacking = False
			self.counter = 0

	def attack(self):
		hurtbox = self.hitbox[:]
		hurtbox[2] = 90
		hurtbox[3] = 86
		if self.direction == 'right':
			hurtbox[0] += 45
		else:
			hurtbox[0] -= 95

		for enemy in self.enemies:
				if pygame.Rect.colliderect(enemy.rect, hurtbox):
					enemy.take_damage(self.attack_dmg)

	def take_damage(self, damage):
		if not self.is_rolling:
			self.currentHealth -= damage

		if not self.is_alive():
			self.counter = 0

	def death(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.time_of_last_animation_frame) > self.animation_cooldown:
			self.time_of_last_animation_frame = current_time
			self.image = pygame.transform.flip(self.death_r[self.counter], self.direction == 'left', False)
			self.counter += 1

	def roll(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.time_of_last_animation_frame) > self.roll_animation_cooldown:
			self.time_of_last_animation_frame = current_time
			self.image = pygame.transform.flip(self.roll_r[self.counter], self.direction == 'left', False)
			self.counter += 1
		
		if self.counter > 11:
			self.counter = 0
			self.is_rolling = False
			self.speed -= self.roll_speed