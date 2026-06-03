from core.map import GameMap

from .bomb import Bomb

class Player:
    def __init__(self, map:GameMap, position:tuple[int,int], team:int, name:str):
        self.name = name
        self.team = team

        self.map:GameMap = map
        self.spawn(position)

        self.face_to_dir(0,1)
        self.set_color()

        self.lives: bool = True
        self.hp:int = 5

    def spawn(self, position):
        x,y = position
        if self.map.is_valid_pixel(x,y):
            self.position = position
            self.map.occupy_pixel(x,y)
            pass

    def face_to_dir(self, x:int,y:int):
        self.facing_dir = (x,y)

    def get_target_postion(self):
        target_x = self.position[0] + self.facing_dir[0]
        target_y = self.position[1] + self.facing_dir[1]

        return (target_x,target_y)

    def walk_to_dir(self):
        target_pos = self.get_target_postion()

        target_px = self.map.get_pixel(target_pos[0], target_pos[1])

        if target_px.obstructed or target_px.occupied:
            return
        else:
            self.map.occupy_pixel(target_pos[0], target_pos[1])
            self.map.deoccupy_pixel(self.position[0], self.position[1])
            self.position = target_pos
            
    def get_damage(self, damage:int):
        self.hp -= damage
        print("Damaged!")

        if self.hp == 0: self.lives = False

    def place_bomb(self):
        target_pos = self.get_target_postion()
        target_px = self.map.get_pixel(target_pos[0], target_pos[1])

        if target_px.obstructed or target_px.occupied:
            return None
        else:
            return Bomb(self, target_pos, 5, 1)
        
    def set_color(self):
        if self.team == 1:
            self.color = (0,0,255)
        elif self.team == 2:
            self.color = (255,0,0)
        else:
            print("Invalid team!")