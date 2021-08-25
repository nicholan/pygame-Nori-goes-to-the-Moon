from pygame.constants import MOUSEBUTTONDOWN, MOUSEWHEEL
from .state import State
import pygame

class Title(State):
    """
    Title screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta):
        pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                self.exit_state()

            elif event.key == pygame.K_p:
                new_state = Title(self.game)
                new_state.enter_state()

    def render(self, surface):
        surface.fill(pygame.Color("grey50"))
        self.game.draw_text(surface, f"Game States TITLE {len(self.game.state_stack)}", (0,0,0), 320, 180)