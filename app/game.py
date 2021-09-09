import pygame
from pathlib import Path
from settings import Settings
from tools import load_images, load_maps, load_sfx

class Game():
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Nori")

            self.surface = pygame.Surface((240, 320), flags=pygame.SRCALPHA)
            self.rect = self.surface.get_rect()
            self.settings = Settings(self.rect)

            self.clock = pygame.time.Clock()

            self.delta = 0
            self.fps = 60
            self.keys = pygame.key.get_pressed()

            self.running = True
            self.state_stack = []

            self.get_scaled_mouse_pos()
            self.load_directories()
            self.load_assets()
            self.create_gameplay()
            self.load_states()

        def run(self):
            """
            Main game loop.
            """
            while self.running:
                self.check_events()
                self.update()
                self.render()
                self.delta = self.clock.tick(self.fps) * 0.001 * self.fps

        def check_events(self):      
            self.keys = pygame.key.get_pressed()
            self.get_scaled_mouse_pos()

            for event in pygame.event.get():    
                self.state_stack[-1].on_event(event)

                if event.type == pygame.QUIT:
                    self.running = False

        def update(self):
            self.state_stack[-1].update()

        def render(self):
            # Render current state to the screen
            self.state_stack[-1].render(self.surface)
            self.settings.screen.blit(pygame.transform.scale(self.surface, (self.settings.width, self.settings.height)), (0,0))
            pygame.display.flip()
        
        def get_scaled_mouse_pos(self):
            """
            Scale mouse positioning with display size.
            """
            mouse_pos = list(pygame.mouse.get_pos())
            self.scaled_pos = (mouse_pos[0] / self.settings.ratio[0], mouse_pos[1] / self.settings.ratio[1])

        def load_directories(self):
            """
            Create pointers to assets folders.
            """
            self.SRC_DIR = Path(__file__).parent / "src"
            self.ASSETS_DIR = self.SRC_DIR / "assets"
            self.IMAGES = self.ASSETS_DIR / "images" 
            self.MAPS = self.ASSETS_DIR / "maps"
            self.SFX = self.ASSETS_DIR / "sfx"
            self.MUSIC = self.ASSETS_DIR / "music"

        def load_assets(self):
            """
            Create asset dictionaries.
            """
            self.images_dict = load_images(self.IMAGES)
            self.maps_dict = load_maps(self.MAPS)
            self.sfx_dict = load_sfx(self.SFX)

        def create_gameplay(self):
            """
            Initialize game backgrounds, tilemaps, player.
            """
            from src.objects.backgrounds import Backgrounds
            from src.objects.tiles import MapLevel
            from src.objects.player import Player

            self.tiles = MapLevel(self.maps_dict, self.images_dict, self.settings.difficulty)
            self.backgrounds = Backgrounds(self.surface, self.images_dict)
            self.player = Player((120,304), self.images_dict['player_sheet'], self.sfx_dict)

        def load_states(self):
            """
            Create game states dictionary.
            """
            from src.states.title import TitleScreen
            from src.states.gameplay import GamePlay
            from src.states.menu import MenuScreen
            from src.states.settings import SettingsScreen
            from src.states.ending import EndingScreen
            from src.states.transition import TransitionScreen

            self.state_dict = {
                'Title': TitleScreen,
                'Gameplay': GamePlay,
                'Menu': MenuScreen,
                'Settings': SettingsScreen,
                'Transition': TransitionScreen,
                'Ending': EndingScreen
            }

            # Set starting state ('Title')
            self.title_screen = self.state_dict['Title'](self)
            self.state_stack.append(self.title_screen)




