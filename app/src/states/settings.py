import pygame
from .state import State
from ..objects.button import Button
from ..objects.tiles import MapLevel

class SettingsScreen(State):
    """
    Settings screen state.
    """

    def __init__(self, game):
        State.__init__(self, game)
        self.diff_list = ['Easy', 'Normal', 'Hard', 'Hardest']
        self.btn_messages()
        self.buttons = [
            Button(self.reso_msg, 120, 100, self.game.sfx_dict),
            Button(self.diff_msg, 120, 130, self.game.sfx_dict),
            Button(self.music_msg, 120, 160, self.game.sfx_dict), 
            Button(self.frame_msg, 120, 190, self.game.sfx_dict),
            Button(self.stats_msg, 120, 220, self.game.sfx_dict),
            Button('Back', 120, 280, self.game.sfx_dict),
            ]

    def update(self):
        self.btn_messages()
        self.update_messages()
        [button.update(self.game.scaled_pos) for button in self.buttons]


    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit_state()
            self.game.settings.save_settings()
            self.game.sfx_dict['ground'].play()

        elif self.buttons[0].hover(self.game.scaled_pos):
            if event.type == pygame.MOUSEBUTTONUP:
                self.change_display_scaling(event.button)
                self.game.sfx_dict['ground'].play()

        elif self.buttons[1].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.change_difficulty()
            self.game.sfx_dict['ground'].play()

        elif self.buttons[2].hover(self.game.scaled_pos):
            if event.type == pygame.MOUSEBUTTONUP:
                self.change_vol(event.button)
                self.game.sfx_dict['ground'].play()

        elif self.buttons[3].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.on_off_frame()
            self.game.sfx_dict['ground'].play()
        
        elif self.buttons[4].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.toggle_stats()
            self.game.sfx_dict['ground'].play()

        elif self.buttons[5].hover(self.game.scaled_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.game.sfx_dict['ground'].play()
            self.game.settings.save_settings()
            self.exit_state()
                
    def render(self, surface):
        surface.blit(self.game.images_dict[str(MapLevel.level)], (0, 0))
        [button.draw(surface) for button in self.buttons]

    def btn_messages(self):
        """
        Update button messages.
        """
        f = lambda arg : 'On' if arg else 'Off'
        self.music_msg = 'Music volume:' + str(int(self.game.settings.volume*10))
        self.diff_msg = 'Difficulty:' + self.diff_list[self.game.settings.difficulty] 
        self.reso_msg = 'Display:' + str(self.game.settings.width) +' * '+ str(self.game.settings.height)
        self.frame_msg = 'Window frame:' + f(self.game.settings.frame)
        self.stats_msg = 'Game stats:' + f(self.game.settings.stats)

    def update_messages(self):
        """
        Update button messages on screen.
        """
        self.buttons[0].msg = self.reso_msg
        self.buttons[1].msg = self.diff_msg
        self.buttons[2].msg = self.music_msg
        self.buttons[3].msg = self.frame_msg
        self.buttons[4].msg = self.stats_msg

    def change_display_scaling(self, mouse_button):
        """
        Left mouse button increases window size, right decreases.
        """
        if mouse_button == 1:
            if self.game.settings.resolution_scale == len(self.game.settings.resolution) - 1:
                self.game.settings.resolution_scale = 0
            else:
                self.game.settings.resolution_scale += 1
        elif mouse_button == 3:
            if self.game.settings.resolution_scale == 0:
                self.game.settings.resolution_scale = len(self.game.settings.resolution) - 1
            else:
                self.game.settings.resolution_scale -= 1

        self.game.settings.load_screen(self.game.settings.resolution_scale) # Update display window with selected scale.
    
    def change_difficulty(self):
        """
        Cycles game difficulty setting.
        """
        if self.game.settings.difficulty == 3:
            self.game.settings.difficulty = 0
        else:
            self.game.settings.difficulty += 1

        self.game.tiles.difficulty = self.game.settings.difficulty
        self.game.tiles.create_level_dict(self.game.maps_dict) # Reload tiles images with corresponding difficulty.

    def change_vol(self, mouse_button):
        """
        Change volume setting.
        """
        if mouse_button == 1:
            if self.game.settings.volume == 10:
                self.game.settings.volume = 10
            else:
                self.game.settings.volume += 1
        elif mouse_button == 3:
            if self.game.settings.volume == 0:
                self.game.settings.volume = 0
            else:
                self.game.settings.volume -= 1
        self.game.settings.change_music_volume(self.game.settings.volume)

    def on_off_frame(self):
        """
        Toggle screen frame.
        """
        if self.game.settings.frame:
            self.game.settings.frame = False
        else:
            self.game.settings.frame = True

        self.game.settings.on_off_frame() # Update display window.


    def toggle_stats(self):
        """
        Toggle stats (level, 'meters') display during gameplay.
        """
        self.game.settings.toggle_stats() # Update display window.
