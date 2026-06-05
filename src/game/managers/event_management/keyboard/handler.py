from pygame.event import Event 

from .handles.window.router import window_on_keydown
from .handles.game.router import game_on_keydown
from .handles.player.router import player_on_keydown, player_on_keyhold

class KeyboardEvents:
    def __init__(self, app):
        self.app = app
        self.players = self.app.player_manager.players

    def on_keydown(self, event:Event):
        window_cmds = window_on_keydown(event)
        game_cmds = game_on_keydown(event)
        player_cmds = player_on_keydown(self.players, event)      

        cmds = [*window_cmds, *game_cmds, *player_cmds]
        return cmds

    def on_keyhold(self):
        player_on_keyhold(self.players)