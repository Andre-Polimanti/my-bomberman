import random
from pygame import time as t

from entities.player import Player

class Bot(Player):
    def __init__(self, map, position, team, name):
        super().__init__(map, position, team, name)
        self.view_range = 4
        
        self.move_delay = 300 
        self.face_delay = 100
        
        self.state = "WANDERING"
        self.next_action_time = t.get_ticks()
        
        self.directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.scan_index = 0
        self.flee_steps = 0
        
        self.logical_dir = self.facing_dir 
        random.shuffle(self.directions)

    def get_target_position(self):
        target_x = self.position[0] + self.logical_dir[0]
        target_y = self.position[1] + self.logical_dir[1]
        return (target_x, target_y)

    def _restart_scan(self):
        self.scan_index = 0
        random.shuffle(self.directions)
        
    def _spray(self, players):
        pos = self.position
        # Usa logical_dir em vez de facing_dir
        target_pos = (pos[0] + self.logical_dir[0], pos[1] + self.logical_dir[1])

        for p in players:
            if p == self or (p.position[0] == pos[0] or p.position[1] == pos[1]):
                continue
            
            dx = p.position[0] - target_pos[0]
            dy = p.position[1] - target_pos[1]

            if (dy == 0 and abs(dx) <= self.view_range) or \
               (dx == 0 and abs(dy) <= self.view_range):
                self.facing_dir = self.logical_dir
                return True
        return False

    def update(self, players):
        if not self.is_alive or self.stunned:
            return None
            
        now = t.get_ticks()
        
        if now < self.next_action_time:
            return None

        dx, dy = self.directions[self.scan_index]

        # Muda apenas a direção LÓGICA (o bot não vira visualmente ainda)
        if self.logical_dir != (dx, dy):
            self.logical_dir = (dx, dy)
            self.next_action_time = now + self.face_delay
            return None

        # Como sobrescrevemos get_target_position, ele usa a logical_dir aqui
        target_pos = self.get_valid_target()

        match self.state:
            case "WANDERING":
                if target_pos:
                    if self._spray(players):
                        self.state = "FLEEING"
                        self.flee_steps = 6
                        self.next_action_time = now + self.move_delay
                        
                        # ATUALIZA O VISUAL: Vira o rosto para soltar a bomba na direção certa
                        self.face_to_dir(dx, dy) 
                        
                        # Prioriza dar meia-volta
                        oposite_dir = (-dx, -dy)
                        self.directions.remove(oposite_dir)
                        self.directions.insert(0, oposite_dir)
                        self.scan_index = 0 
                        
                        return {"type": "PLAY", "action": "BOMBING", "player": self, "pos": target_pos}

                    if random.random() < 0.5:
                        # ATUALIZA O VISUAL: Vira o rosto para a direção que vai andar
                        self.face_to_dir(dx, dy) 
                        self.walk()
                        
                        self.next_action_time = now + self.move_delay
                        self._restart_scan() 
                        return None
                        
                self.scan_index += 1
                if self.scan_index >= 4:
                    self._restart_scan()
                return None

            case "FLEEING":
                if target_pos:
                    # ATUALIZA O VISUAL: Vira o rosto e corre em linha reta
                    self.face_to_dir(dx, dy) 
                    self.walk()
                    
                    self.next_action_time = now + self.move_delay
                    self.flee_steps -= 1
                    
                    if self.flee_steps <= 0:
                        self.state = "WANDERING"
                        self._restart_scan() 
                    return None
                    
                self.scan_index += 1
                if self.scan_index >= 4:
                    self._restart_scan()
                return None