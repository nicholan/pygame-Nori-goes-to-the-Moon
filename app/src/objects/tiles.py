from collections import defaultdict
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.type = type

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class MapLevel():
    """
    This class is used for creating platforms that will be checked for player collision.
    """
    level = 0
    transitioning = False # Level transition lock

    def __init__(self, map_dict, images_dict, difficulty):
        self.difficulty = difficulty
        self.map_level = 0
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.images_dict = images_dict
        self.level_dict = defaultdict(list)
        self.create_level_dict(map_dict)
    

    def draw_map(self, surface):
        """Draw tiles on screen according to current MapLevel.level"""
        for tile in self.level_dict[str(MapLevel.level)]:
            tile.draw(surface)


    def create_level_dict(self, map_dict):
        """
        Create level dictionary from parsed csv lists.
        """
        for level, map in map_dict.items():
            tiles = self.load_tiles(map)
            self.level_dict[level] = tiles


    def load_tiles(self, map):
        """
        Create Tiles from parsed csv lists.
        """
        tiles = []
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    tiles.append(Tile(self.images_dict['platform' + str(self.difficulty)], x * self.tile_size, y * self.tile_size, 'solid'))
                    

                elif tile == '2':
                    tiles.append(Tile(self.images_dict['blank'], x * self.tile_size, y * self.tile_size, 'solid'))
                x += 1
            # Move to the next row
            y += 1
        # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
    

    def update_level(self):
        """
        Call load_tiles() again if player passes top or bottom of screen.
        """
        if self.map_level != MapLevel.level:
            if MapLevel.level < 0: # Prevent game crashing if player somehow spawns/falls below map 0.
                MapLevel.level = 0
            elif MapLevel.level > 32:
                MapLevel.level = 32
            else:
                self.map_level = MapLevel.level
    
    @classmethod
    def increase_level(cls):
        """Called when player crosses top of the screen"""
        cls.level += 1

    
    @classmethod
    def decrease_level(cls):
        """Called when player crosses bottom of the screen"""
        cls.level -= 1


