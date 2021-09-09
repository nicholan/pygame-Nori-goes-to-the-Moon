from .state import State
import pygame
from ..objects.button import Button
from ..objects.tiles import MapLevel

class MenuScreen(State):
    """
    Menu screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)
        self.buttons = [
            Button('Continue', 120, 220, game.sfx_dict),
            Button('Settings', 120, 250, game.sfx_dict), 
            Button('Quit', 120, 280, game.sfx_dict),
            ]

    def update(self):
        [button.update(self.game.scaled_pos) for button in self.buttons]

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit_state()

        if self.buttons[0].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.sfx_dict['ground'].play()
            self.exit_state()
        
        if self.buttons[1].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.sfx_dict['ground'].play()
            new_state = self.game.state_dict['Settings'](self.game)
            new_state.enter_state()

        if self.buttons[2].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.running = False
                
    def render(self, surface):
        surface.blit(self.game.images_dict[str(MapLevel.level)], (0, 0))
        [button.draw(surface) for button in self.buttons]