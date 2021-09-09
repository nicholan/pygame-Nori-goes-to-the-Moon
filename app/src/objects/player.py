import pygame
from .tiles import MapLevel
from .spritesheet import SpriteStripAnim


class Player:
    """
    Class for player controlled character.
    """
    def __init__(self, pos, image, sfx_dict):
        self.images = [
            SpriteStripAnim(image, (0,0,16,13), 4, colorkey=(0, 0, 0), loop=True, frames=5), # IDLE RIGHT[0]
            SpriteStripAnim(image, (0,13,16,13), 8, colorkey=(0,0,0), loop=True, frames=5), # RIGHT [1]
            SpriteStripAnim(image, (0,13,16,13), 8, colorkey=(0,0,0), loop=True, frames=5, reverse=True), # LEFT [2] (is right reversed.)
            SpriteStripAnim(image, (0,26,16,13), 2, colorkey=(0,0,0), loop=True, frames=10), # JUMP RIGHT [3]
            SpriteStripAnim(image, (0,26,16,13), 2, colorkey=(0,0,0), loop=True, frames=10, reverse=True), #JUMP LEFT [4] (reversed)
            SpriteStripAnim(image, (0,0,16,13), 4, colorkey=(0, 0, 0), loop=True, frames=5, reverse=True) # IDLE LEFT [5] (reversed)
        ]

        for _ in self.images:
            _.iter()

        self.sfx_dict = sfx_dict
        self.rect = self.images[0].images[0].get_rect()
        self.is_jumping = False
        self.is_grounded = False
        self.facing_right = True
        self.gravity = .35
        self.friction = -.12
        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)


    def animate(self):
        """
        Sprite animations.
        """
        if self.is_jumping:
            if self.velocity.x > 0: # Jumping right.
                self.image = self.images[3].next()
            else:
                self.image = self.images[4].next()
        else:
            if self.velocity.x > 0: # Moving right.
                self.image = self.images[1].next()
            elif self.velocity.x < 0:
                self.image = self.images[2].next()
            elif self.is_jumping == False and self.facing_right:
                self.image = self.images[0].next()
            elif self.is_jumping == False and not self.facing_right:
                self.image = self.images[5].next()


    def update(self, keys, delta, tiles, surface_rect):
        """
        Update must accept a new argument delta (time delta between frames).
        Adjustments to position must be multiplied by this delta.
        Set the rect to true_pos once adjusted (automatically converts to int).
        """
        self.animate()
        self.horizontal_movement(keys, delta)
        self.check_collisions_x(tiles)
        self.vertical_movement(delta)
        self.check_collisions_y(tiles)
        self.check_edges(surface_rect)
        self.check_exit(surface_rect)
        

    def horizontal_movement(self, keys, delta):
        """
        Player movement on the x-axis.
        """
        self.acceleration.x = 0
        if keys[pygame.K_a]:
            self.facing_right = False
            self.acceleration.x -= .3
        elif keys[pygame.K_d]:
            self.acceleration.x += .3
            self.facing_right = True

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * delta
        self.cap_velocity(4)
        self.position.x += self.velocity.x * delta + (self.acceleration.x * .5) * (delta * delta)
        self.rect.x = self.position.x

    def vertical_movement(self, delta):
        """
        Player movement on the y-axis.
        """
        if self.velocity.y != 0.0:
            self.is_jumping = True

        self.velocity.y += self.acceleration.y * delta
        if self.velocity.y > 9: 
            self.velocity.y = 9
        self.position.y += self.velocity.y * delta + (self.acceleration.y * .5) * (delta * delta)
        self.rect.bottom = self.position.y

    def cap_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: 
            self.velocity.x = 0 

    def jump(self):
        """
        Player jumping.
        """
        if self.is_grounded:
            self.sfx_dict['jump'].play()
            self.is_jumping = True
            self.velocity.y -= 7
            self.is_grounded = False

    def get_hits(self, tiles):
        """
        Get a list of player-tile collisions.
        """
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles):
        """
        Check player-tile collisions on the x-axis, left and right of tiles.
        """
        collisions = self.get_hits(tiles)
        for tile in collisions: 
            if self.velocity.x > 0: # Hit tile from left.
                self.velocity.x = 0
                self.position.x = tile.rect.left - self.rect.width
                self.rect.x = self.position.x

            elif self.velocity.x < 0: # Hit tile from right.
                self.velocity.x = 0
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def check_collisions_y(self, tiles):
        """
        Check player-tile collisions on the y-axis, top and bottom of tiles.
        """
        self.rect.bottom += 1 # +1 to make sure jump is more reliable.
        collisions = self.get_hits(tiles)
        
        for tile in collisions:
            if self.velocity.y > 0: # Hit tile from the top.
                if self.is_jumping and MapLevel.level == 0 and self.rect.y > 280: # Play sfx if player hits the ground.
                    self.sfx_dict['ground'].play()

                self.is_grounded = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y

            elif self.velocity.y < 0: # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.height
                self.rect.bottom = self.position.y

    def check_edges(self, surface_rect):
        """
        Prevent player from moving outside left and right screen boundaries.
        """
        if self.rect.x < 0:
            self.position.x = 0
            self.rect.x = self.position.x
        elif self.rect.x > (surface_rect.width - self.rect.width):
            self.position.x = surface_rect.width - self.rect.width
            self.rect.x = self.position.x

    def check_exit(self, surface_rect):
        if not MapLevel.transitioning:
            if self.position.y < surface_rect.top: # Hit top edge on screen
                self.position.y = surface_rect.bottom # Reposition player to the bottom of the screen
                self.rect.y = self.position.y
                MapLevel.increase_level()

            elif self.position.y > surface_rect.bottom: # Hit bottom edge on screen
                self.position.y = surface_rect.top # Reposition player to the top of the screen
                self.rect.y = self.position.y
                MapLevel.decrease_level()
            MapLevel.transitioning = True

    def draw(self, surface):
        """
        Draw player to the screen.
        """
        surface.blit(self.image, self.rect)