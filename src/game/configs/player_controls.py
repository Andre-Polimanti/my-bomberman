import pygame

p1_controls = {
    "move_keys": {
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0),
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
    },
    "bomb_key": pygame.K_SPACE,
    "last_instr": None,
    "last_time": pygame.time.get_ticks()
}
p2_controls = {
    "move_keys": {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    },
    "bomb_key": pygame.K_KP_ENTER,
    "last_instr": None,
    "last_time": pygame.time.get_ticks()
}
player_controls = [p1_controls, p2_controls]