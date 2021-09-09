import pygame

class Button:
    def __init__(self, msg, x, y, sfx_dict):    
        """Create clickable buttons, hovering over changes text color."""
        self.msg = msg
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('David', 19)
        self.x, self.y = x, y
        self.text_surface = self.font.render(self.msg, True, self.text_color)
        self.rect = self.text_surface.get_rect()
        self.rect.center = (self.x, self.y)
        self.sfx_dict = sfx_dict
        self.sfx_play = True


    def draw(self, surface):
        surface.blit(self.text_surface, self.rect)
    
    def update(self, mouse_pos):
        """Takes scaled mouse position as arg."""
        if self.hover(mouse_pos):
            self.text_color = 'orange'
            self.text_surface = self.font.render(self.msg, True, self.text_color)
            if self.sfx_play:
                self.sfx_dict['m_over'].play()
                self.sfx_play = False

        else:
            self.text_color = (255, 255, 255)
            self.text_surface = self.font.render(self.msg, True, self.text_color)
            self.sfx_play = True

    def hover(self, mouse_pos):
        """Check if cursor is over the button."""
        return True if self.rect.collidepoint(mouse_pos) else False