from ......configs.player_controls import *
from .commands import on_keydown, on_keyhold

def player_on_keydown(players, event):
    actions = []

    act = on_keydown(players[0], p1_controls, event)
    if act: actions.append(act)
    act = on_keydown(players[1], p2_controls, event)
    if act: actions.append(act)

    return actions

def player_on_keyhold(players):
    on_keyhold(players[0], p1_controls)
    on_keyhold(players[1], p2_controls)
