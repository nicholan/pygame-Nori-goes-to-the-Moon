import pygame
from pathlib import Path

class Game():
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("My Game")

            self.surface = pygame.Surface((640, 360))
            self.rect = self.surface.get_rect()

            self.width, self.height = 960, 540
            self.screen = pygame.display.set_mode((self.width,self.height))
            self.clock = pygame.time.Clock()

            self.delta = 0
            self.fps = 60
            self.keys = pygame.key.get_pressed()
            self.font = pygame.font.SysFont(None, 48)

            self.running, self.playing = True, True

            self.state_stack = []
            
            self.load_assets()
            self.load_states()

        def run(self):
            while self.playing:
                self.check_events()
                self.update()
                self.render()

                # Time updater
                self.now = pygame.time.get_ticks()
                self.delta = self.clock.tick(self.fps) * 0.001 * self.fps

        def check_events(self):
            self.keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                self.state_stack[-1].on_event(event)

                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    
        def update(self):
            self.state_stack[-1].update(self.delta)

        def render(self):
            # Render current state to the screen
            self.state_stack[-1].render(self.surface)
            self.screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (0,0))

            pygame.display.flip()


        def draw_text(self, surface, text, color, x, y):
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to assets folders.
            SRC_DIR = Path(__file__).parent / "src"
            self.ASSETS_DIR = SRC_DIR / "assets"
            self.IMAGES = self.ASSETS_DIR / "images"

        def load_states(self):
            from src.states.title import TitleScreen
            from src.states.gameplay import GamePlay
            from src.states.menu import MenuScreen
            from src.states.inventory import InventoryScreen

            self.state_dict = {
                'Title': TitleScreen,
                'Gameplay': GamePlay,
                'Menu': MenuScreen,
                'Inventory': InventoryScreen,
            }

            # Set starting state ('Title')
            self.title_screen = self.state_dict['Title'](self)
            self.state_stack.append(self.title_screen)


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.run()
    pygame.quit()
