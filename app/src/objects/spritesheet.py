import pygame
from math import floor
import copy

## Spritesheet and SpriteStripAnim from https://www.pygame.org/wiki/Spritesheet

class Spritesheet:
    def __init__(self, filename):
        self.sheet = filename
            
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None, reverse=False, scale=None):
        "Loads image from x,y,x+offset,y+offset"

        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        if reverse:
            image = pygame.transform.flip(image, True, False)

        if scale:
            if scale == 2:
                new = pygame.Rect(0,0,rect.width*2,rect.height*2)
                image = pygame.transform.scale2x(image, pygame.Surface(new.size))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
            else:
                new = pygame.Rect(0,0,rect.width*scale,rect.height*scale)
                image = pygame.transform.scale(image, (new.width, new.height))
                image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None, reverse=False, scale=None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey, reverse, scale) for rect in rects]
        
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None, reverse=False, scale=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey, reverse, scale)


class SpriteStripAnim:
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1, reverse=False, scale=None):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        # For copying
        self.filename = filename
        self.rect = rect
        self.count = count
        self.colorkey = colorkey
        self.loop = loop

        ss = Spritesheet(filename)
        self.images = ss.load_strip(rect, count, colorkey, reverse, scale)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self

    def copy(self):
        copyobj = SpriteStripAnim(self.filename, self.rect, self.count, colorkey=self.colorkey, loop=self.loop)
        return copyobj

