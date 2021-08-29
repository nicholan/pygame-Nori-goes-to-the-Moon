from .state import State
import pygame

class MenuScreen(State):
    """
    Menu screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta):
        pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit_state()
                
    def render(self, surface):
        surface.fill(pygame.Color("yellow"))
        self.game.draw_text(surface, f"State MENU {len(self.game.state_stack)}", (0,0,0), 136, 256)