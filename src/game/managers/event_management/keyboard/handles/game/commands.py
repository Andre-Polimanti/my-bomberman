import pygame

def on_keydown(event):
    if event.key == pygame.K_r:
        return{"type": "GAME_COMMAND", "action": "RESTART"}
    else:
        pass