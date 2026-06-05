import pygame

def on_keydown(event):
    if event.key == pygame.K_ESCAPE:
        return {"action": "CLOSE_WINDOW"}
    if event.key == pygame.K_r:
        return{"action": "RESTART"}
    else:
        pass