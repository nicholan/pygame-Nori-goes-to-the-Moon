from .state import State
import pygame
from ..objects.button import Button
from ..objects.tiles import MapLevel
from ..objects.backgrounds import Fade

class EndingScreen(State):
    """
    End credits screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)
        self.buttons = [
            Button('Play Again?', 120, 170, game.sfx_dict), 
            Button('Quit', 120, 200, game.sfx_dict),
            ]
        MapLevel.level = 0
        self.fade = pygame.sprite.Group(Fade(fade_color=(255, 255, 255)))

    def update(self):
        self.game.backgrounds.update()
        self.game.backgrounds.moon.update()
        [button.update(self.game.scaled_pos) for button in self.buttons]
        self.fade.update()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_running = False

        if self.buttons[0].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.sfx_dict['chime'].play()
            self.game.backgrounds.bg_image = self.game.images_dict[str(MapLevel.level)]
            new_state = self.game.state_dict['Transition'](self.game, 'Gameplay')
            self.exit_state()
            new_state.enter_state()
        
        elif self.buttons[1].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.running = False
        
    def render(self, surface):
        surface.blit(self.game.images_dict[str(32)], (0, 0))
        for element in self.game.backgrounds.dust[0]:
                element.draw(surface)
        self.game.backgrounds.moon.draw(surface)
        surface.blit(self.game.images_dict['nori2'], (0, 0))
        surface.blit(self.game.images_dict['lv_1_front'], (0, 0))
        [button.draw(surface) for button in self.buttons]
        surface.blit(self.game.images_dict['cat_sleep'], (116, 296))
        self.fade.draw(surface)
        
        