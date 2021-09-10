from .state import State
from ..objects.button import Button
import pygame
import os

class TitleScreen(State):
    """
    Title screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)
        self.buttons = [
            Button('Play', 120, 220, game.sfx_dict), 
            Button('Settings', 120, 250, game.sfx_dict), 
            Button('Quit', 120, 280, game.sfx_dict),
            ]

        pygame.mixer.music.load(os.path.join(self.game.MUSIC, 'theme.mp3')) # Start theme music at title screen.
        pygame.mixer.music.play(-1) # Loop

    def update(self):
        self.game.backgrounds.moon.update()
        [button.update(self.game.scaled_pos) for button in self.buttons]

    def on_event(self, event):
        if self.game.backgrounds.moon.rect.collidepoint(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.music.load(os.path.join(self.game.MUSIC, 'theme2.mp3'))
            pygame.mixer.music.play(-1)

        elif self.buttons[0].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.sfx_dict['chime'].play()
            new_state = self.game.state_dict['Transition'](self.game, 'Gameplay')
            self.exit_state()
            new_state.enter_state()

        elif self.buttons[1].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.sfx_dict['ground'].play()
            new_state = self.game.state_dict['Settings'](self.game)
            new_state.enter_state()
            
        elif self.buttons[2].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.running = False

    def render(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.game.images_dict[str(32)], (0, 0))
        self.game.backgrounds.moon.draw(surface)
        surface.blit(self.game.images_dict['nori'], (0, 0))
        [button.draw(surface) for button in self.buttons]
        