import random
from pygame import time as t

class Bot:
    def __init__(self, player, bomb_manager=None, player_manager=None):
        self.player = player
        self.bomb_manager = bomb_manager
        self.player_manager = player_manager 
        
        self.last_move_time = t.get_ticks()
        self.move_delay = 500
        
        self.last_bomb_time = t.get_ticks()
        self.bomb_delay = 3000
        
        self.current_dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def update(self):
        if self.player.stunned or not self.player.is_alive:
            return

        now = t.get_ticks()
        
        if now - self.last_move_time >= self.move_delay:
            in_danger = False
            danger_axis = None

            if self.bomb_manager:
                for bomb in self.bomb_manager.active_bombs:
                    bx, by = bomb.position
                    px, py = self.player.position
                    
                    if px == bx:
                        in_danger = True
                        danger_axis = 'X'
                        break
                    elif py == by:
                        in_danger = True
                        danger_axis = 'Y'
                        break

            turned_corner = False

            if in_danger:
                escape_directions = []
                if danger_axis == 'X':
                    escape_directions = [(1, 0), (-1, 0)]
                elif danger_axis == 'Y':
                    escape_directions = [(0, 1), (0, -1)]

                random.shuffle(escape_directions)

                for dx, dy in escape_directions:
                    self.player.face_to_dir(dx, dy)
                    if self.player.get_valid_target():
                        self.current_dir = (dx, dy)
                        self.player.walk()
                        turned_corner = True
                        break

            if not turned_corner:
                self.player.face_to_dir(*self.current_dir)
                if self.player.get_valid_target():
                    self.player.walk()
                else:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(directions)
                    for dx, dy in directions:
                        self.player.face_to_dir(dx, dy)
                        if self.player.get_valid_target():
                            self.current_dir = (dx, dy)
                            self.player.walk()
                            break
            
            self.last_move_time = now

        if self.bomb_manager and (now - self.last_bomb_time >= self.bomb_delay):
            dropped_bomb = False
            dist_limit = 4 

            if self.player_manager:
                for other_player in self.player_manager.the_living:
                    if other_player.team in [1, 2]: 
                        dist_x = abs(self.player.position[0] - other_player.position[0])
                        dist_y = abs(self.player.position[1] - other_player.position[1])
                        distance = dist_x + dist_y
                        
                        if distance <= dist_limit:
                            self.bomb_manager.create_bomb(self.player, self.player.position, 5)
                            self.last_bomb_time = now
                            dropped_bomb = True
                            break 

            if not dropped_bomb and random.random() < 0.2:
                self.bomb_manager.create_bomb(self.player, self.player.position, 5) 
                self.last_bomb_time = now