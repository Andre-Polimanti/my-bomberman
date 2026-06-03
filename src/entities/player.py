from core.map import GameMap

from .bomb import Bomb

class Player:
    def __init__(self, map:GameMap, position:tuple[int,int], team:int):
        self.map:GameMap = map

        self.position = position
        self.team = team

        self.lives: bool = True
        self.hp:int = 5

        self.spawn()
        self.face_to_dir(0,1)

    def spawn(self):
        (x, y) = self.position
        if self.map.is_valid_pixel(x,y):
            # self.map.obstruct_pixel(x,y)
            pass

    def face_to_dir(self, x:int,y:int):
        self.facing_dir = (x,y)

    def get_target_postion(self):
        target_x = self.position[0] + self.facing_dir[0]
        target_y = self.position[1] + self.facing_dir[1]

        return target_x,target_y

    def walk_to_dir(self):
        target_pos = self.get_target_postion()

        target_px = self.map.get_pixel(target_pos)

        if target_px.obstructed == True:
            return
        else:
            # self.map.obstruct_pixel(target_pos)
            # self.map.desobstruct_pixel(self.position)
            self.position = target_pos
            
    def get_damaged(self):
        current_px = self.map.get_pixel(self.position)
        if current_px.burning == True:
            self.hp -= 1

        if self.hp == 0: self.lives = False

    def place_bomb(self):
        target_pos = self.get_target_postion()
        target_px = self.map.get_pixel(target_pos[0], target_pos[1])

        if target_px.obstructed or target_px.burning:
            return None
        else:
            return Bomb(self, target_pos, 5, 1)