import os
import pygame
import csv

def draw_text(surface, text, color, x, y):
            font = pygame.font.SysFont('arial', 13)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

def load_images(directory, colorkey=(0,0,0), accept=(".png", ".jpg", ".bmp")):
    """
    Load all graphics, convert images accordingly, set colorkey / alpha.
    """
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics

    
def load_maps(directory, accept=(".csv")):
    """
    Create dictionary of parsed map csv files.
    """
    maps = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if ext.lower() in accept:
            map = []
            with open(os.path.join(directory, file)) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    map.append(list(row))
            maps[name]=map
    return maps


def load_sfx(directory, accept=(".ogg")):
    """
    Create dictionary of sound effects.
    """
    sfx_dict = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if ext.lower() in accept:
            sfx = pygame.mixer.Sound(os.path.join(directory, file))
            sfx_dict[name]=sfx
    return sfx_dict


