import pygame 
from settings import *
from tile import Tile
from player import Player
from ui import UI
from support import *

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

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
							""" if col == 'x':
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == 'p':
					self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites) """
		self.player = Player((2500,1500),[self.visible_sprites], self.obstacle_sprites)	

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.ui.display(self.player)

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

	def custom_draw(self,player): #logic for the camera, overlaps sprites in the Y direction
		#get offsets
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		#drawing floor

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface, floor_offset_pos)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.center - self.offset
			self.display_surface.blit(sprite.image, (offset_pos[0] - (sprite.image.get_width() / 2), offset_pos[1] - (sprite.image.get_height() / 2)))