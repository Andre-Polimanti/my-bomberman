import pygame

def on_keydown(event):
    if event.key == pygame.K_ESCAPE:
        return {"type": "WINDOW_COMMAND", "action": "CLOSE"}
    if event.key == pygame.K_m:
        return {"type": "WINDOW_COMMAND", "action": "MINIMIZE"}
    else:
        pass