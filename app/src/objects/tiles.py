import pygame, csv, os
from pathlib import Path

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.type = type

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, map_name, images_dict):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.images_dict = images_dict
        self.tiles = self.load_tiles(map_name)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0, 0))

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def load_tiles(self, map):
        tiles = []
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    tiles.append(Tile(self.images_dict['grass'], x * self.tile_size, y * self.tile_size, 'solid'))
                    # Move to the next tile in current row
                elif tile == '2':
                    tiles.append(Tile(self.images_dict['box'], x * self.tile_size, y * self.tile_size, 'solid'))
                elif tile == '3':
                    tiles.append(Tile(self.images_dict['water'], x * self.tile_size, y * self.tile_size, 'liquid'))
                x += 1
            # Move to the next row
            y += 1
        # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
