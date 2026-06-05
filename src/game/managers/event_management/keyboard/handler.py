from pygame.event import Event 

from ....configs.player_controls import *
from .handles.player import player_on_keydown, player_on_keyhold

class KeyboardEvents:
    def __init__(self, app):
        self.players = app.player_manager.players

        self.move_delay = 150

    def handle_keydown(self, event: Event):
        if not self.players: return

        actions = []
        
        act = player_on_keydown(self.players[0], p1_controls, event)
        if act: actions.append(act)
        act = player_on_keydown(self.players[1], p2_controls, event)
        if act: actions.append(act)

        return actions

    def handle_keyhold(self):
        if not self.players: return

        player_on_keyhold(self.players[0], p1_controls)
        player_on_keyhold(self.players[1], p2_controls)
