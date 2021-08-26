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

        
        self.isJump = False
        self.velocity = 8
        self.mass = 1

    def make_image(self):
        """
        Load player image.
        """

        image = pygame.image.load(os.path.join(self.assets, 'player_r.png')).convert_alpha()
        return image
    
    def jump(self, screen_rect, delta):
        """
        Make player jump.
        """
        if self.isJump:
            FORCE = (1 / 2) * self.mass * (self.velocity**2)
            self.true_pos[1] -= FORCE

            self.velocity -= 1
            if self.velocity < 0:
                self.mass = -1

            if self.velocity == -9:
                self.isJump = False
                self.velocity = 8
                self.mass = 1

            self.rect.center = self.true_pos
            self.clamp(screen_rect)


    def update(self, keys, screen_rect, delta):
        """
        Update must accept a new argument delta (time delta between frames).
        Adjustments to position must be multiplied by this delta.
        Set the rect to true_pos once adjusted (automatically converts to int).
        """

        # Test gravity.
        self.true_pos[1] += 1 * self.speed * delta

        for key in self.MOVEMENT:
            if keys[key]:
                self.true_pos[0] += self.MOVEMENT[key][0] * self.speed * delta
                self.true_pos[1] += self.MOVEMENT[key][1] * self.speed * delta
        self.rect.center = self.true_pos
        self.clamp(screen_rect)

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