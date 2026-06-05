import pygame

TYPE = "GAME_COMMAND"

def on_keydown(event):
    if event.key == pygame.K_r:
        return{"type": TYPE, "action": "RESTART"}
    else:
        pass