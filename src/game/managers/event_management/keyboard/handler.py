from pygame.event import Event 

from .handles.player.router import player_on_keydown, player_on_keyhold
from .handles.window.router import window_on_keydown

class KeyboardEvents:
    def __init__(self, app):
        self.app = app
        self.players = self.app.player_manager.players

    def on_keydown(self, event:Event):
        player_cmds = player_on_keydown(self.players, event)
        window_cmds = window_on_keydown(event)
        
        cmds = [*window_cmds, *player_cmds]
        return cmds

    def on_keyhold(self):
        player_on_keyhold(self.players)