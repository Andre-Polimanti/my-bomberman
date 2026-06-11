import random
from pygame import time as t

from entities.player import Player

VISION_RANGE = 4
FLEE_STEPS = 6
FLEE_CHANCE = 0.8
WALK_CHANCE = 0.5
WALK_AHEAD_CHANCE = 0.4

# MOVE_DELAY = 10
# LOOK_DELAY = 25

MOVE_DELAY = 150
LOOK_DELAY = 50

class Bot(Player):
    def __init__(self, map, position, team, name):
        super().__init__(map, position, team, name)
        self.flee_steps = FLEE_STEPS
        
        self.move_delay = MOVE_DELAY
        self.face_delay = LOOK_DELAY # Controls the flow of info caught by the bot
        
        self.state = "WANDERING"
        self.next_action_time = t.get_ticks()
        
        self.directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        self.scan_index = 0
        self.fires = set()

        self.logical_dir = self.facing_dir # The bot will access its surrounding pixels and process them without graphically turning to them
        random.shuffle(self.directions) # So the bot wont read direction on the same order

    def get_target_position(self):
        target_x = self.position[0] + self.logical_dir[0]
        target_y = self.position[1] + self.logical_dir[1]

        return (target_x, target_y)

    def life_and_death(self, fires):
        self.fires = fires or set()
        super().life_and_death(fires) 

    def get_valid_target(self):
        target_pos = super().get_valid_target()
        # So the bot wont enter the fire
        if target_pos and target_pos in self.fires:
            return None 
        return target_pos
        
    def _player_for_bombing(self, players):
        # If there is a player in the same axys as the pixel the bot is processing, we need this pixel to bomb the player
        pos = self.position
        target_pos = (pos[0] + self.logical_dir[0], pos[1] + self.logical_dir[1])

        for p in players:
            if p == self or not p.is_alive:
                continue

            dx = p.position[0] - target_pos[0]
            dy = p.position[1] - target_pos[1]

            if (dy == 0 and abs(dx) <= VISION_RANGE) or \
               (dx == 0 and abs(dy) <= VISION_RANGE):
                self.face_to_dir(*self.logical_dir)
                return True
        return False

    def _try_walk_facing(self, now):
        # To keep the bots from going and coming, we set a certain chance that they keep the current dirrection while walking
        fx, fy = self.facing_dir
        fpos = (self.position[0] + fx, self.position[1] + fy)
        fpixel = self.map.get_pixel(fpos[0], fpos[1])

        if fpixel.obstructed or fpixel.occupied or fpos in self.fires:
            return False

        if random.random() >= WALK_AHEAD_CHANCE:
            return False

        self.logical_dir = self.facing_dir
        self.walk()
        self.next_action_time = now + self.move_delay
        return True

    def update(self, players):
        if self.stunned:
            return None

        now = t.get_ticks()

        if now < self.next_action_time:
            return None
        # Applying delay

        dx, dy = self.directions[self.scan_index] # Gets direction in shuffled list by index

        if self.logical_dir != (dx, dy): # If the direction is diferent from the the one the bot holding for processing, it must be updated.
            self.logical_dir = (dx, dy)
            self.next_action_time = now + self.face_delay
            return None
            # After the pixel for processing is updated, the dellay is applied.
            # This branch will not be accessed in the next iteraction, and the state machine will be operated.

        dir = dx,dy

        return self.state_machine(dir, players, now) # Must be returned, so that the bombing can go up to the actual game as an event

    def state_machine(self, direction, players, time):
        target_pos = self.get_valid_target()
        dx, dy = direction

        match self.state:
            case "WANDERING":
                if target_pos and self._player_for_bombing(players):
                    self.state = "FLEEING"
                    self.flee_steps = 6
                    self.next_action_time = time + self.move_delay

                    self.face_to_dir(dx, dy)
                    self._flee_from(target_pos)

                    return {"type": "PLAY", "action": "BOMBING", "player": self, "pos": target_pos}

                presence_pos = self._detect_presence()
                if presence_pos and random.random() < FLEE_CHANCE:
                    self.state = "FLEEING"
                    self.flee_steps = 6
                    self.next_action_time = time + self.move_delay
                    self._flee_from(presence_pos)
                    return None

                if self._try_walk_facing(time):
                    return None

                if target_pos and random.random() < WALK_CHANCE:
                        self.face_to_dir(dx, dy)
                        self.walk()
                        self.next_action_time = time + self.move_delay
                        self._restart_scan()
                        return None

                self._advance_scan()

            case "FLEEING":
                if target_pos:
                    self.face_to_dir(dx, dy) 
                    self.walk()
                    
                    self.next_action_time = time + self.move_delay
                    self.flee_steps -= 1
                    
                    if self.flee_steps <= 0:
                        self.state = "WANDERING"
                        self._restart_scan() 
                    return None
                    
                self._advance_scan()
            
    def _advance_scan(self):
        self.scan_index += 1
        if self.scan_index >= len(self.directions):
            self._restart_scan()
        return None

    def _restart_scan(self):
        # If the bot didn't make a decision it must rescan it's surroundings until it does something
        self.scan_index = 0
        random.shuffle(self.directions)
    
    def _detect_presence(self):
        # If there is a player or bomb in the same axis the bot is, it may have to run
        px, py = self.position

        for dx, dy in self.directions:
            for step in range(1, VISION_RANGE + 1):
                x, y = px + dx * step, py + dy * step
                pixel = self.map.get_pixel(x, y)

                if pixel.obstructed:
                    break
                if pixel.occupied:
                    return (x, y)
        return None
    
    def _flee_from(self, danger_pos):
        # If the bot places a bomb or detects a presence and decides to flee, if possible from the starting pixel, it leaves the mutual axis, if not it just runs in the other direction
        # (May result in trapping)
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