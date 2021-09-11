import pygame
from .tiles import MapLevel
from collections import defaultdict
from random import choice
from .spritesheet import SpriteStripAnim
import random

class Backgrounds:
    """
    Create random moving elements in the background.
    """
    def __init__(self, surface, images_dict):
        self.surface = surface
        self.images_dict = images_dict
        self.bg_image = self.images_dict[str(MapLevel.level)]
        self.planets = defaultdict(list)
        self.dust = defaultdict(list)
        self.asteroids = defaultdict(list)
        self.nebulas = defaultdict(list)

        self.trees = self.images_dict['lv_1_front'] # Level 0 trees.  (+ end screen trees.)
        self.moon = Moon(self.images_dict['moon']) # Level 32 moon. (also title screen, end screen.)

        Asteroid.parse_asteroid_sheet(self.images_dict)
        Planet.parse_planets_sheet(self.images_dict)
        self.init_levels()
        self.init_elements()

    def init_levels(self):
        """
        Create empty lists in the element dicts.
        """
        for i in range(0, 32):
            self.planets[i] = pygame.sprite.Group()
            self.dust[i] = [] # Only one dust img per level.
            self.asteroids[i] = pygame.sprite.Group()
            self.nebulas[i] = [] # Only one nebula img per level.
                
    def init_elements(self):
        self.create_planets()
        self.create_dust(self.images_dict)
        self.create_asteroids()
        self.create_nebulas(self.images_dict)

    def update(self):
        self.create_planets()
        self.create_dust(self.images_dict)
        self.create_asteroids()
        self.create_nebulas(self.images_dict)

        # Move elements in all existing levels even if player is not in the level.
        for _, planets in self.planets.items():
            self.update_all_elements(planets)

        for _, dust in self.dust.items():
            self.update_all_elements(dust)

        for _, asteroid in self.asteroids.items():
            self.update_all_elements(asteroid)
        
        for _, nebula in self.nebulas.items():
            self.update_all_elements(nebula)

        self.moon.update()

        # Clear offscreen elements.
        for _, planets in self.planets.items():
            self.clear_offscreen_elements(planets)
        
        for _, dust in self.dust.items():
            self.clear_offscreen_elements(dust)
        
        for _, asteroid in self.asteroids.items():
            self.clear_offscreen_elements(asteroid)
        
        for _, nebula in self.nebulas.items():
            self.clear_offscreen_elements(nebula)
        
        if MapLevel.level > 0: # Prevent game crashing if level is < 0.
            self.bg_image = self.images_dict[str(MapLevel.level)]


    def create_planets(self):
        for level, planets in self.planets.items():
            if level > 22:
                if len(planets) < 2:
                    new_planet = Planet()
                    self.planets[level].add(new_planet) # Create a new dictionary key if one doesnt already exist.
            elif level > 11:
                if len(planets) < 1:
                    new_planet = Planet()
                    self.planets[level].add(new_planet)

    def create_dust(self, images):
        for level, dust in self.dust.items():
            if len(dust) < 1:
                new_dust = Dust(images, level)
                self.dust[level].append(new_dust)
            elif Dust.wind_direction > 0 and len(dust) == 1:
                if dust[0].rect.left > 0:
                    new_dust = Dust(images, level)
                    self.dust[level].append(new_dust)
            elif Dust.wind_direction < 0 and len(dust) == 1:
                if dust[0].rect.right < 240:
                    new_dust = Dust(images, level)
                    self.dust[level].append(new_dust)
    
    def create_asteroids(self):
        for level, asteroid in self.asteroids.items():
            if level > 23:
                if len(asteroid) < 3:
                    new_asteroid = Asteroid()
                    self.asteroids[level].add(new_asteroid)

            elif level > 19:
                if len(asteroid) < 1:
                    new_asteroid = Asteroid()
                    self.asteroids[level].add(new_asteroid)

    def create_nebulas(self, images):
        for level, nebula in self.nebulas.items():
            if level > 24:
                if len(nebula) < 1:
                    new_nebula = Nebula(images, level)
                    self.nebulas[level].append(new_nebula)

                elif Dust.wind_direction > 0 and len(nebula) == 1:
                    if nebula[0].rect.left > 0:
                        new_nebula = Nebula(images, level)
                        self.nebulas[level].append(new_nebula)
                
                elif Dust.wind_direction < 0 and len(nebula) == 1:
                    if nebula[0].rect.right < 240:
                        new_nebula = Nebula(images, level)
                        self.nebulas[level].append(new_nebula)


    def clear_offscreen_elements(self, element_list):
        for element in element_list:
            if element.speed > 0:
                if element.rect.left > 320:
                    element_list.remove(element)
            
            elif element.speed < 0:
                if element.rect.right < 0:
                    element_list.remove(element)
                    
    def update_all_elements(self, element_list):
        for element in element_list:
            element.update()

    def draw_elements(self):
        """
        Draw elements on the visible level.
        """
        self.surface.blit(self.bg_image, (0, 0))

        if MapLevel.level != 32:
            for element in self.nebulas[MapLevel.level]:
                element.draw(self.surface)
                
            for element in self.planets[MapLevel.level]: 
                element.draw(self.surface)

            for element in self.asteroids[MapLevel.level]:
                element.draw(self.surface)
            
            for element in self.dust[MapLevel.level]:
                element.draw(self.surface)
        else:
            self.moon.draw(self.surface)
        
        if MapLevel.level == 0:
            self.surface.blit(self.trees, (0, 0))



class Planet(pygame.sprite.Sprite):
    """
    Class for creating randomly sized and rotated moving planets.
    """
    planets = []

    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        
        self.images = choice(Planet.planets).copy() #SpriteStripAnim.copy(), create a copy to perform transform operations on.
        scale = random.randint(1, 15) / 10
        flipping = random.randint(0, 3)
        if scale != 1.0:
            rect = pygame.Rect(0, 0, 100*scale, 100*scale)
            self.images.images = [pygame.transform.scale(image, (rect.width, rect.height)) for image in self.images.images]

        if flipping != 0:
            self.images.images = self.randomize(self.images.images, flipping)

        self.images.frames = random.randint(60, 200)
        self.images.f = self.images.frames
        self.images.iter()

        self.rect = self.images.images[0].get_rect()
        self.y = random.randint(50, 270) # Starting position.

        self.speed_x = choice([round(random.uniform(-.05, -.2), 2), 
                                round(random.uniform(.05, .2), 2)])
        self.speed_y = choice([round(random.uniform(-.001, -.01), 3), 
                                round(random.uniform(.001, .01), 3)])

        self.speed = self.speed_x

        if self.speed > 0: # Element moves to the right, so it should start from left side of screen.
            self.x = 0 - self.rect.width
        else: # Moves left
            self.x = 240
    
    def animate(self):
        self.image = self.images.next()

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.y = self.y
        self.rect.x = self.x
        self.animate()
    
    def randomize(self, images, flipping):
        """Random vertical and horizontal image flipping."""
        if flipping == 1:
            img_list = [pygame.transform.flip(image, True, False) for image in images]
        elif flipping == 2:
            img_list = [pygame.transform.flip(image, False, True) for image in images]
        elif flipping == 3:
            img_list = [pygame.transform.flip(image, True, True) for image in images]
        return img_list

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    @classmethod
    def parse_planets_sheet(cls, images_dict):
        """Parse planet spritesheet during the loading state."""
        planet_sheet = images_dict['planets']
        rect = planet_sheet.get_rect() # get the size of the sheet

        for x in range(int(rect.height / 100)):
            new_planet = SpriteStripAnim(planet_sheet, (0, x*100, 100, 100), 90, colorkey=(0, 0, 0), loop=True, frames=60)
            Planet.planets.append(new_planet)



class Dust(pygame.sprite.Sprite):
    """
    Moving space dust, randomized images.
    """
    clouds = ['cloud' + str(x) for x in range(28)]
    wind_direction = choice([-1, 1])
    first_load_counter = 0 # First time game is loaded elements spawn at middle of the screen, instead of outside the screen.

    def __init__(self, image, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = image[Dust.clouds[0]] # Placeholder.
        
        if level == 0:
            # Base level.
            self.image = choice([image[Dust.clouds[0]], image[Dust.clouds[1]]])
            self.image = choice([self.image, pygame.transform.flip(self.image, True, False)])

        elif level in (range(1, 6)):
            x = random.randint(3,6)
            self.image = image[Dust.clouds[x]] # White clouds.
            self.image = self.randomize(self.image)
        
        elif level in (range(6, 11)):
            x = random.randint(7,9)
            self.image = image[Dust.clouds[x]] # Blue clouds.
            self.image = self.randomize(self.image)
        
        elif level in (range(11, 15)):
            x = random.randint(10,14)
            self.image = image[Dust.clouds[x]] # Yellow clouds.
            self.image = self.randomize(self.image)
        
        elif level in (range(15, 20)):
            x = random.randint(15,18)
            self.image = image[Dust.clouds[x]] # Pink clouds.
            self.image = self.randomize(self.image)

        elif level in (range(20, 28)):
            x = random.randint(20,22)
            self.image = image[Dust.clouds[x]] # Purple clouds.
            self.image = self.randomize(self.image)

        elif level in (range(28, 32)):
            x = random.randint(23,27)
            self.image = image[Dust.clouds[x]] # Red/fire clouds.
            self.image = self.randomize(self.image)

        self.rect = self.image.get_rect()

        if level == 0:
            self.rect.y = 320 - self.rect.height # Clouds start at bottom of screen.

        self.set_speed()
        self.set_position()
        
    def set_position(self):
        """Set cloud starting positions."""
        if Dust.wind_direction > 0: # Elements moving to the right, so they should start from left side of screen.
            if Dust.first_load_counter < 31: # First round of elements spawn middle of the screen.
                self.x = 0 
                Dust.first_load_counter += 1
            else:
                self.x = 0 - self.rect.width

        else: # Start right.
            if Dust.first_load_counter < 31:
                self.x = 0 
                Dust.first_load_counter += 1
            else:
                self.x = 0 + 320

    def set_speed(self):
        if Dust.wind_direction > 0:
            self.speed = round(random.uniform(.08, .2), 2) # Moving right.
        else:
            self.speed = round(random.uniform(-.08, -.2), 2) # Moving left.

    def randomize(self, image):
        """Random vertical and horizontal image flipping."""
        img = choice([image, 
        pygame.transform.flip(image, True, False), 
        pygame.transform.flip(image, False, True), 
        pygame.transform.flip(image, True, True)])
        return img

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Nebula(pygame.sprite.Sprite):

    nebulas = ['nebula' + str(x) for x in range(8)]

    def __init__(self, image, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = image[Nebula.nebulas[0]] # Placeholder.

        if level in (range(24, 28)):
            x = random.randint(0, 2)
            self.image = image[Nebula.nebulas[x]] # Choose random purple nebula.
            self.image = self.randomize(self.image)
            
        elif level in (range(28, 32)):
            x = random.randint(3, 6)
            self.image = image[Nebula.nebulas[x]] # Choose random fire nebula.
            self.image = self.randomize(self.image)

        self.rect = self.image.get_rect()
        self.set_speed()

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def set_speed(self):
        if Dust.wind_direction > 0:
            self.speed = round(random.uniform(.03, .09), 2) # Moving right.
            self.x = 0 - self.rect.width
        else:
            self.speed = round(random.uniform(-.03, -.09), 2) # Moving left.
            self.x = 240

    def randomize(self, image):
        """Random vertical and horizontal image flipping."""
        img = choice([image, 
        pygame.transform.flip(image, True, False), 
        pygame.transform.flip(image, False, True), 
        pygame.transform.flip(image, True, True)])
        return img

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Asteroid(pygame.sprite.Sprite):

    asteroids = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = choice(Asteroid.asteroids).copy() #SpriteStripAnim.copy(), create a copy to perform transform operations on.
        scale = random.randint(2, 13) / 10
        flipping = random.randint(0, 3)

        if scale != 1.0:
            rect = pygame.Rect(0, 0, 100*scale, 100*scale)
            self.images.images = [pygame.transform.scale(image, (rect.width, rect.height)) for image in self.images.images]

        if flipping != 0:
            self.images.images = self.randomize(self.images.images, flipping)

        self.images.frames = random.randint(60, 200)
        self.images.f = self.images.frames
        self.images.iter()

        self.rect = self.images.images[0].get_rect()
        self.speed_x = choice([round(random.uniform(-.05, -.2), 2), 
                                round(random.uniform(.05, .2), 2)])

        self.speed_y = choice([round(random.uniform(-.05, -.1), 2), 
                                round(random.uniform(.05, .1), 2)])

        self.y = random.randint(75, 250) # Starting position on y-axis.
        self.speed = self.speed_x

        if self.speed_x > 0: # Element moves to the right, so it should start from left side of screen.
            self.x = 0 - self.rect.width
        else: # Moves left
            self.x = 240

    def animate(self):
        self.image = self.images.next()

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.y = self.y
        self.rect.x = self.x
        self.animate()

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def randomize(self, images, flipping):
        """Random vertical and horizontal image flipping."""
        if flipping == 1:
            img_list = [pygame.transform.flip(image, True, False) for image in images]
        elif flipping == 2:
            img_list = [pygame.transform.flip(image, False, True) for image in images]
        elif flipping == 3:
            img_list = [pygame.transform.flip(image, True, True) for image in images]
        return img_list

    @classmethod
    def parse_asteroid_sheet(cls, images_dict):
        """Parse asteroid spritesheet during the loading state."""
        asteroid_sheet = images_dict['asteroids']
        rect = asteroid_sheet.get_rect() # get the size of the sheet

        for x in range(int(rect.height / 100)):
            new_asteroid = SpriteStripAnim(asteroid_sheet, (0, x*100, 100, 100), 90, colorkey=(0, 0, 0), loop=True, frames=60)
            Asteroid.asteroids.append(new_asteroid)


class Moon(pygame.sprite.Sprite):
    """Class to handle the Moon seperate from other screen elements."""
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.images = SpriteStripAnim(image, (0,0,100,100), 90, colorkey=(0, 0, 0), loop=True, frames=60)
        self.rect = self.images.images[0].get_rect()
        self.rect.y = 25
        self.rect.x = 120
        self.images.iter()

    def animate(self):
        self.image = self.images.next()

    def update(self):
        self.animate()
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Fade(pygame.sprite.Sprite):
    """
    Screen fade for between game state transitions.
    """
    def __init__(self, fade_color=(0,0,0), fade_in=True):
        super().__init__()
        self.rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.fade_in = fade_in
        self.color = fade_color
        if self.fade_in:
            self.alpha = 255
            self.opacity = -1
        else:
            self.alpha = 0
            self.opacity = 1


    def update(self):
        self.image.fill((self.color[0], self.color[1], self.color[2], self.alpha))
        self.alpha += self.opacity
        if self.alpha >= 255:
            self.alpha = 255

        elif self.alpha <= 0:
            self.alpha = 0
        else:
            self.alpha += self.opacity


