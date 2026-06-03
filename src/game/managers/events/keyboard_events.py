import pygame
from pygame.event import Event 


class KeyboardEvents:
    def __init__(self, app):
        self.player_manager = app.player_manager
        self.bomb_manager = app.bomb_manager
        self.move_delay = 150

        self.p1_controls = {
            "keys": {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            },
            "bomb_key": pygame.K_SPACE,
            "last_instr": None,
            "last_time": pygame.time.get_ticks()
        }
    def handle_keydown(self, event: Event):
        players = self.player_manager.players
        if not players: return

        p1 = players[0]
        if event.key in self.p1_controls["keys"]:
            dx, dy = self.p1_controls["keys"][event.key]
            
            p1.face_to_dir(dx, dy)
            
            if self.p1_controls["last_instr"] == event.key:
                target_x = p1.position[0] + dx
                target_y = p1.position[1] + dy

                bomb = self.bomb_manager.get_bomb_by_cord(target_x,target_y)
                if bomb is not None and bomb.state == "TICKING":
                    return
                else:
                    p1.walk_to_dir()
        
            self.p1_controls["last_time"] = pygame.time.get_ticks()
                
        elif event.key == self.p1_controls["bomb_key"]:
            self.bomb_manager.create_bomb(p1)

        self.p1_controls["last_instr"] = event.key

    def handle_holded_keys(self):
        players = self.player_manager.players
        if not players: return

        p1 = players[0]

        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        for key in self.p1_controls["keys"]:
            if keys[key]: 
                if key == self.p1_controls["last_instr"]:
                    if now - self.p1_controls["last_time"] >= self.move_delay:
                        dx, dy = self.p1_controls["keys"][key]

                        target_x = p1.position[0] + dx
                        target_y = p1.position[1] + dy

                        bomb = self.bomb_manager.get_bomb_by_cord(target_x,target_y)
                        if bomb is not None and bomb.state == "TICKING":
                            return
                        else:
                            p1.walk_to_dir()
                        
                        self.p1_controls["last_time"] = now
                        break