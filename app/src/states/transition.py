from .state import State
from ..objects.backgrounds import Fade
import pygame

class TransitionScreen(State):
    """
    End credits screen state.
    """
    def __init__(self, game, next_state, fade_color=(0,0,0)):
        State.__init__(self, game)
        self.next_state = next_state
        self.fade = pygame.sprite.Group(Fade(fade_color=fade_color, fade_in=False)) # Fade out
        self.counter = 0
        
    def update(self):
        self.fade.update()
        self.counter += 7

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pass
                
    def render(self, surface):
        self.fade.draw(surface)
        if self.counter >= 254:
            new_state = self.game.state_dict[self.next_state](self.game)
            self.exit_state()
            new_state.enter_state()