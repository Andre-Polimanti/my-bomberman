import pygame

TYPE = "WINDOW_COMMAND"

def on_keydown(event):
    if event.key == pygame.K_ESCAPE:
        return {"type": TYPE, "action": "CLOSE"}
    if event.key == pygame.K_m:
        return {"type": TYPE, "action": "MINIMIZE"}
    else:
        pass