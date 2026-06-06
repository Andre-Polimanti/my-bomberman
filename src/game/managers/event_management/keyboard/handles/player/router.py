from ......configs.player_controls import *
from .commands import on_keydown, on_keyhold

def player_on_keydown(players, event):
    actions = []

    for i in range(len(players)):
        act = on_keydown(players[i], player_controls[i], event)
        if act: actions.append(act)

    return actions

def player_on_keyhold(players):
    on_keyhold(players[0], p1_controls)
    on_keyhold(players[1], p2_controls)
