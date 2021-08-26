import os
import sys
import pygame


class Player:
    """
    Class for player controlled character.
    """
    
    def __init__(self, pos, speed, assets):
        
        self.assets = assets
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=pos)
        self.true_pos = list(self.rect.center) # Exact float position.
        self.speed = speed # Speed in pixels per second.
        self.MOVEMENT = {
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_w: (0, 0), # (0, -1) No moving up y.
            pygame.K_s: (0, 0), # (0, 1) No moving down y.
            }

        
        self.is_jumping = False
        self.is_grounded = False
        self.gravity, self.friction = .35, -.12
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)


    def make_image(self):
        """
        Load player image.
        """
        image = pygame.image.load(os.path.join(self.assets, 'player_r.png')).convert_alpha()
        return image
    
    def jump(self):
        if self.is_grounded:
            self.is_jumping = True
            self.velocity.y -= 8
            self.is_grounded = False


    def update(self, keys, screen_rect, delta):
        """
        Update must accept a new argument delta (time delta between frames).
        Adjustments to position must be multiplied by this delta.
        Set the rect to true_pos once adjusted (automatically converts to int).
        """
        self.horizontal_movement(keys, screen_rect,delta)
        self.vertical_movement(delta)
        


    def horizontal_movement(self, keys, screen_rect, delta):
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
        self.velocity.y += self.acceleration.y * delta
        if self.velocity.y > 7: 
            self.velocity.y = 7
        self.position.y += self.velocity.y * delta + (self.acceleration.y * .5) * (delta * delta)

        if self.position.y >= 320:
            self.is_grounded = True
            self.velocity.y = 0
            self.position.y = 320
        self.rect.bottom = self.position.y

    def cap_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0 



    def clamp(self, screen_rect):
        """
        Clamp the rect to the screen if needed and reset true_pos to the
        rect position so they don't lose sync.
        """
        if not screen_rect.contains(self.rect):
            self.rect.clamp_ip(screen_rect)
            self.true_pos = list(self.rect.center)

    def draw(self, surface):
        """
        Draw player to the screen.
        """
        surface.blit(self.image, self.rect)