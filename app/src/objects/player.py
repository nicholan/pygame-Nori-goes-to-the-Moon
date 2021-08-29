import os
import pygame


class Player:
    """
    Class for player controlled character.
    """
    def __init__(self, pos, image):
        
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.is_jumping = False
        self.is_grounded = False
        self.gravity = .35
        self.friction = -.12
        self.position = pygame.math.Vector2(100, 100)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)


    def update(self, keys, delta, tiles):
        """
        Update must accept a new argument delta (time delta between frames).
        Adjustments to position must be multiplied by this delta.
        Set the rect to true_pos once adjusted (automatically converts to int).
        """
        self.horizontal_movement(keys, delta)
        self.check_collisions_x(tiles)
        self.vertical_movement(delta)
        self.check_collisions_y(tiles)


    def horizontal_movement(self, keys, delta):
        """
        Player movement on the x-axis.
        """
        self.acceleration.x = 0
        if keys[pygame.K_a]:
            self.acceleration.x -= .3
        elif keys[pygame.K_d]:
            self.acceleration.x += .3

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * delta
        self.cap_velocity(4)
        self.position.x += self.velocity.x * delta + (self.acceleration.x * .5) * (delta * delta)
        self.rect.x = self.position.x

    def vertical_movement(self, delta):
        """
        Player movement on the y-axis.
        """
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
            self.is_jumping = True
            self.velocity.y -= 9
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
            if tile.type == 'solid': # Tile types for different collision properties.
                if self.velocity.x > 0: # Hit tile from left.
                    self.velocity.x = 0
                    self.position.x = tile.rect.left - self.rect.w
                    self.rect.x = self.position.x

                elif self.velocity.x < 0: # Hit tile from right.
                    self.velocity.x = 0
                    self.position.x = tile.rect.right
                    self.rect.x = self.position.x


    def check_collisions_y(self, tiles):
        """
        Check player-tile collisions on the y-axis, top and bottom of tiles.
        """
        self.is_grounded = False
        self.rect.bottom += 1 # +1 to make sure jump is more reliable.

        collisions = self.get_hits(tiles)
        for tile in collisions:
            if tile.type == 'solid':
                if self.velocity.y > 0: # Hit tile from the top.
                    self.is_grounded = True
                    self.is_jumping = False
                    self.velocity.y = 0
                    self.position.y = tile.rect.top
                    self.rect.bottom = self.position.y

                elif self.velocity.y < 0: # Hit tile from the bottom
                    self.velocity.y = 0
                    self.position.y = tile.rect.bottom + self.rect.h
                    self.rect.bottom = self.position.y

    def draw(self, surface):
        """
        Draw player to the screen.
        """
        surface.blit(self.image, self.rect)