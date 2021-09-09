from .state import State
import pygame
from tools import draw_text
from ..objects.tiles import MapLevel
from ..objects.backgrounds import Fade

class GamePlay(State):
    """
    Main gameplay state.
    """
    def __init__(self, game):
        State.__init__(self, game)
        self.fade = pygame.sprite.Group(Fade())

    def update(self):
        self.fade.update()
        self.game.tiles.update_level()
        self.game.backgrounds.update()
        self.game.player.update(self.game.keys, self.game.delta, self.game.tiles.level_dict[str(MapLevel.level)], self.game.rect)
        self.track_statistics()
        MapLevel.transitioning = False
        self.check_ending()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                new_state = self.game.state_dict['Menu'](self.game)
                new_state.enter_state()

            elif event.key == pygame.K_SPACE:
                    self.game.player.jump()
        
    def render(self, surface):
        self.game.backgrounds.draw_elements()
        self.game.player.draw(surface)
        self.game.tiles.draw_map(surface)
        if self.game.settings.stats:
            draw_text(surface, f"{MapLevel.level}", (255,255,255), 230, 310) 
            draw_text(surface, f"{self.meters / 10}", (255,255,255), 30, 310)
        self.fade.draw(surface)
    
    def check_ending(self):
        """
        Check whether player reaches the last level and jumps to the moon.
        Transition to ending state. Resets player positioning.
        """
        if MapLevel.level == 32 and self.game.player.rect.colliderect(self.game.backgrounds.moon.rect):
            self.game.sfx_dict['chime2'].play()
            self.game.player.__init__((120, 304), self.game.images_dict['player_sheet'], self.game.sfx_dict)
            new_state = self.game.state_dict['Transition'](self.game, 'Ending', fade_color=(255, 255, 255))
            self.exit_state()
            new_state.enter_state()
        
    def track_statistics(self):
        self.meters = MapLevel.level * 320 - self.game.player.rect.y + 291


            
        
        
