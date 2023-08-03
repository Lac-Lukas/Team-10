import pygame 
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == 'p':
					self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites, self.enemy_sprites)
				if col == 'e':
					Enemy((x,y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.player)

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.remove_eliminated_enemies(self.enemy_sprites)
	
	def remove_eliminated_enemies(self, enemy_sprites):
		for enemy in enemy_sprites:
			if enemy.health <= 0 and enemy.has_death_animation_played:
				enemy_sprites.remove(enemy)
				self.visible_sprites.remove(enemy)

class YSortCameraGroup (pygame.sprite.Group):
	def __init__(self):

		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self,player): #logic for the camera, overlaps sprites in the Y direction
		#center player in window
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.center - self.offset
			self.display_surface.blit(sprite.image, (offset_pos[0] - (sprite.image.get_width() / 2), offset_pos[1] - (sprite.image.get_height() / 2)))

			#pygame.draw.rect(self.display_surface, 'red', pygame.Rect(offset_pos[0] - (sprite.image.get_width() / 2), offset_pos[1] - (sprite.image.get_height() / 2), 64, 80))
