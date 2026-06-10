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

        self.fires = set()

        self.logical_dir = self.facing_dir
        random.shuffle(self.directions)

    def get_target_position(self):
        target_x = self.position[0] + self.logical_dir[0]
        target_y = self.position[1] + self.logical_dir[1]
        return (target_x, target_y)

    def life_and_death(self, fires):
        self.fires = fires or set()
        super().life_and_death(fires)

    def get_valid_target(self):
        target_pos = super().get_valid_target()
        if target_pos and target_pos in self.fires:
            return None
        return target_pos

    def _restart_scan(self):
        self.scan_index = 0
        random.shuffle(self.directions)
        
    def _spray(self, players):
        pos = self.position
        target_pos = (pos[0] + self.logical_dir[0], pos[1] + self.logical_dir[1])

        for p in players:
            if p == self or not p.is_alive:
                continue

            dx = p.position[0] - target_pos[0]
            dy = p.position[1] - target_pos[1]

            if (dy == 0 and abs(dx) <= self.view_range) or \
               (dx == 0 and abs(dy) <= self.view_range):
                self.face_to_dir(*self.logical_dir)
                return True
        return False

    def _detect_presence(self):
        px, py = self.position

        for dx, dy in self.directions:
            for step in range(1, self.view_range + 1):
                x, y = px + dx * step, py + dy * step
                pixel = self.map.get_pixel(x, y)

                if pixel is None or pixel.obstructed:
                    break
                if pixel.occupied:
                    return (x, y)
        return None

    def _try_walk_facing(self, now):
        fx, fy = self.facing_dir
        fpos = (self.position[0] + fx, self.position[1] + fy)
        fpixel = self.map.get_pixel(fpos[0], fpos[1])

        if fpixel is None or fpixel.obstructed or fpixel.occupied or fpos in self.fires:
            return False

        if random.random() >= 0.4:
            return False

        self.logical_dir = self.facing_dir
        self.walk()
        self.next_action_time = now + self.move_delay
        return True

    def _flee_from(self, danger_pos):
        px, py = self.position
        safe_dirs = []
        other_dirs = []

        for d in self.directions:
            nx, ny = px + d[0], py + d[1]
            if nx != danger_pos[0] and ny != danger_pos[1]:
                safe_dirs.append(d)
            else:
                other_dirs.append(d)

        random.shuffle(safe_dirs)
        random.shuffle(other_dirs)
        self.directions = safe_dirs + other_dirs
        self.scan_index = 0

    def update(self, players):
        if not self.is_alive or self.stunned:
            return None

        now = t.get_ticks()

        if now < self.next_action_time:
            return None

        dx, dy = self.directions[self.scan_index]

        if self.logical_dir != (dx, dy):
            self.logical_dir = (dx, dy)
            self.next_action_time = now + self.face_delay
            return None

        target_pos = self.get_valid_target()

        match self.state:
            case "WANDERING":
                if target_pos and self._spray(players):
                    self.state = "FLEEING"
                    self.flee_steps = 6
                    self.next_action_time = now + self.move_delay

                    self.face_to_dir(dx, dy)
                    self._flee_from(target_pos)

                    return {"type": "PLAY", "action": "BOMBING", "player": self, "pos": target_pos}

                presence_pos = self._detect_presence()
                if presence_pos and random.random() < 0.8:
                    self.state = "FLEEING"
                    self.flee_steps = 6
                    self.next_action_time = now + self.move_delay
                    self._flee_from(presence_pos)
                    return None

                if self._try_walk_facing(now):
                    return None

                if target_pos:
                    if random.random() < 0.5:
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