
import pygame
import json
from pathlib import Path
import os
from pygame.constants import NOFRAME 

class Settings():
    """Class to store game settings. Settings can be changed from ingame settings state."""
    def __init__(self, game_rect):
        """
        Class to manage display scaling, game difficulty, music playing, screen frame, mouse scaling.
        """
        self.resolution = [(int(240*x*0.5), int(320*x*0.5)) for x in range(2, 14)] # Create tuples of different resolutions.
        self.rect = game_rect

        try: # Check if config exists, else go with default settings.
            os.path.join(Path(__file__).parent, 'config.json')
            self.load_settings()
        except:
            self.frame = True
            self.load_screen()
            self.load_difficulty()
            self.change_music_volume()

    def load_screen(self, num=4):
        """
        Rezize display size, available sizes in self.resolution list.
        """
        self.resolution_scale = num
        self.width = self.resolution[self.resolution_scale][0]
        self.height = self.resolution[self.resolution_scale][1]
        self.set_scaling()
        self.on_off_frame()

    def load_difficulty(self, num=1):
        self.difficulty = num # 0 easy, 1 normal, 2 hard, 3 hardest.

    def change_music_volume(self, num=2):
        self.volume = num
        volume_f = self.volume / 10
        pygame.mixer.music.set_volume(volume_f)
    
    def set_scaling(self):
        """Get (display size / surface size) ratio for mouse scaling."""
        ratio_x = (self.width / self.rect.width)
        ratio_y = (self.height / self.rect.height)
        self.ratio = (ratio_x, ratio_y)
    
    def on_off_frame(self):
        if self.frame:
            self.screen = pygame.display.set_mode((self.width, self.height), NOFRAME)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))

    def save_settings(self):
        """
        Save user settings to config.json only when user accesses the settings state in game.
        """
        data = {
                'Screen':[{
                    'Width': self.width,
                    'Height': self.height,
                    'Frame': self.frame,
                    'Scale': self.resolution_scale}],
                'Audio':[{
                    'Music volume': self.volume}],
                'Game':[{
                    'Difficulty': self.difficulty}]
            }

        with open(os.path.join(Path(__file__).parent, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_settings(self):
        """
        Load user's previously created settings.
        """
        with open(os.path.join(Path(__file__).parent, 'config.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['Screen']:
                self.width = i['Width']
                self.height = i['Height']
                self.resolution_scale = i['Scale']
                self.frame = i['Frame']
            for i in data['Audio']:
                self.volume = i['Music volume']
            for i in data['Game']:
                self.difficulty = i['Difficulty']

        self.load_screen(self.resolution_scale)
        self.change_music_volume(self.volume)

