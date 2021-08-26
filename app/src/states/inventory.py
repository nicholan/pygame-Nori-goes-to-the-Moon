from .state import State
import pygame

class InventoryScreen(State):
    """
    Menu screen state.
    """
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta):
        pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.exit_state()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit_state()
                
    def render(self, surface):
        surface.fill(pygame.Color("orange"))
        self.game.draw_text(surface, f"State INVENTORY {len(self.game.state_stack)}", (0,0,0), 320, 180)