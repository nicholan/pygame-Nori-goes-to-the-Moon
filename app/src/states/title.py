from .state import State
import pygame

class TitleScreen(State):
    """
    Title screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta):
        pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            new_state = self.game.state_dict['Gameplay'](self.game)
            self.exit_state()
            new_state.enter_state()
                
    def render(self, surface):
        surface.fill(pygame.Color("grey50"))
        self.game.draw_text(surface, f"State TITLE {len(self.game.state_stack)}", (0,0,0), 320, 180)