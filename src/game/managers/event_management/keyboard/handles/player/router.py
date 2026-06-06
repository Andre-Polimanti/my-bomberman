from ......configs.player_controls import *
from .commands import on_keydown, on_keyhold

def player_on_keydown(players, event):
    actions = []

    for player, controls in zip(players, player_controls):
        act = on_keydown(player, controls, event)
        if act: 
            actions.append(act)
    return actions

def player_on_keyhold(players):
    for player, controls in zip(players, player_controls):
        on_keyhold(player, controls)
