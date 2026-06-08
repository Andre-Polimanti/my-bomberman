from pygame import time as t

from core.map import GameMap

class Player:
    def __init__(self, map:GameMap, position:tuple[int,int], team:int, name:str):
        self.name = name
        self.team = team

        self.map:GameMap = map
        self.spawn(position)

        self.face_to_dir(0,1)
        self.set_color()

        self.is_alive: bool = True
        self.hp:int = 5

    def spawn(self, position):
        x,y = position
        if self.map.is_valid_pixel(x,y):
            self.position = position
            self.map.occupy_pixel(x,y)
            pass

        self.stun_end_time: int = 0
        self.stunned = False

    def face_to_dir(self, x:int,y:int):
        self.facing_dir = (x,y)

    def get_target_position(self):
        target_x = self.position[0] + self.facing_dir[0]
        target_y = self.position[1] + self.facing_dir[1]

        return (target_x,target_y)
    
    def get_valid_target(self):
        if self.stunned:
            return
        
        target_pos = self.get_target_position()
        target_px = self.map.get_pixel(target_pos[0], target_pos[1])

        if target_px.obstructed or target_px.occupied:
            return None
        else:
            return target_pos

    def walk(self):
        px = self.get_valid_target()

        if px:
            self.map.occupy_pixel(px[0], px[1])
            self.map.deoccupy_pixel(self.position[0], self.position[1])

            self.position = px

    def set_color(self):
        match self.team:
            case 1:
                self.color = (0,0,255)
            case 2:
                self.color = (255,0,0)
            case 3:
                self.color = (255,255,0)
            case 4:
                self.color = (0,255,255)
            case _:
                self.color = (159,159,159)

    def _manage_stun(self):
        if self.stunned and t.get_ticks() >= self.stun_end_time:
            self.stunned = False

    def get_damage(self, damage:int = 1, stun_duration:int = 1400):
        if self.stunned:
            return
        
        self.hp -= damage
        
        if self.hp <= 0: 
            self._die()

        self.stunned = True
        self.stun_end_time = t.get_ticks() + stun_duration
    
    def _die(self):
        self.is_alive = False
        self.map.deoccupy_pixel(self.position[0], self.position[1])

    def life_and_death(self, fires):
        self._manage_stun()
        if fires:
            if self.position in fires:
                self.get_damage(1)