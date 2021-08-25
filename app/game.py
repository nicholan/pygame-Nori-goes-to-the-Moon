import pygame
from src.states.title import Title

class Game():
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("My Game")

            self.surface = pygame.Surface((640, 360))
            self.width, self.height = 960, 540
            self.screen = pygame.display.set_mode((self.width,self.height))
            self.clock = pygame.time.Clock()

            self.delta = 0
            self.fps = 60
            self.keys = pygame.key.get_pressed()
            self.font = pygame.font.SysFont(None, 48)

            self.running, self.playing = True, True

            self.state_stack = []

            self.load_assets() # Not implemented
            self.load_states()

        def run(self):
            while self.playing:
                self.check_events()
                self.update()
                self.render()

                # Delta time updater
                self.delta = self.clock.tick(self.fps) * 0.001
                print(len(self.state_stack))

        def check_events(self):
            for event in pygame.event.get():
                self.state_stack[-1].on_event(event)

                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
            pass

        def load_states(self):
            # Starting state
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.run()
    pygame.quit()
