import pygame 
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from ui import UI
from support import *

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

		# add a ui
		self.ui = UI()

	def create_map(self):
		layouts = {
				 'boundary': import_csv_layout('../Levels/Level_0/Level_0_Boundary Layer.csv'),
				 'Props': import_csv_layout('../Levels/Level_0/Level_0_Props.csv'),
		}
		graphics = {
				 'Props': import_folder('../graphics/Tilesets/Objects/Props')
		}
		for style, layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites], 'invisible')
						if style == 'Props':
							surf = graphics['Props'][int(col)]
							Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'Props',surf)
						#create objects
				# if col == 'x':
				# 	Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
				# if col == 'p':
				# 	self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites, self.enemy_sprites)
				# if col == 'e':
				# 	Enemy((x,y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.player)
				# 	self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
		self.player = Player((2500,1500),[self.visible_sprites], self.obstacle_sprites, self.enemy_sprites)
		Enemy("Skeleton", (3000,1500), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.player)
		Enemy("Minotaur", (3000,1200), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.player)
		Enemy("Flying Eye", (3000,1000), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.player)
		Enemy("Mushroom", (2700,800), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.player)

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player, self.enemy_sprites)
		self.visible_sprites.update()
		#self.remove_eliminated_enemies(self.enemy_sprites)
		self.ui.display(self.player)

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

		#floor creation
		self.floor_surface = pygame.image.load('../Levels/Level_0/Ground.png').convert()
		self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

	def custom_draw(self,player, enemy_sprites): #logic for the camera, overlaps sprites in the Y direction
		#center player in window
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		#drawing floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface, floor_offset_pos)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.center - self.offset
			x_pos = offset_pos[0] - (sprite.image.get_width() / 2)
			y_pos = offset_pos[1] - (sprite.image.get_height() / 2)
			self.display_surface.blit(sprite.image, (x_pos, y_pos))

			#draw health bar if sprite is an enemy
			if sprite in enemy_sprites:
				if sprite.type == "Minotaur":
					sprite_offset_x = 15
					sprite_offset_y = 10
				elif sprite.type == "Skeleton":
					sprite_offset_x = 85
					sprite_offset_y = 75
				elif sprite.type == "Flying Eye":
					sprite_offset_x = 80
					sprite_offset_y = 100
				elif sprite.type == "Mushroom":
					sprite_offset_x = 75
					sprite_offset_y = 100

				sprite.health_bar_rect = pygame.Rect((x_pos + sprite_offset_x, y_pos + sprite_offset_y), (150, 20))
				sprite.show_bar(sprite.health_bar_rect, HEALTH_COLOR)