from .state import State
import pygame
from ..objects.player import Player
from ..objects.tiles import TileMap
import os

class GamePlay(State):
    """
    Main gameplay state.
    """
    def __init__(self, game):
        State.__init__(self, game)
        self.player = Player(self.game.rect.center, self.game.images_dict['player'])
        self.map = TileMap(self.game.maps_dict['first'], self.game.images_dict)

    def update(self, delta):
        self.player.update(self.game.keys, delta, self.map.tiles)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                new_state = self.game.state_dict['Menu'](self.game)
                new_state.enter_state()
            
            elif event.key == pygame.K_TAB:
                new_state = self.game.state_dict['Inventory'](self.game)
                new_state.enter_state()

            elif event.key == pygame.K_SPACE:
                    self.player.jump()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.player.is_jumping:
                    self.player.velocity.y *= .25
                    self.player.is_jumping = False

    def render(self, surface):
        surface.fill(pygame.Color("gray90"))
        self.game.draw_text(surface, f"State GAMEPLAY {len(self.game.state_stack)}", (0,0,0), 136, 256)
        self.player.draw(surface)
        self.map.draw_map(surface)
        self.map.load_map()
        
