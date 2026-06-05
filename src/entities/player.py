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
    
    def get_valid_target(self):
        target_pos = self.get_target_postion()
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
            
    def get_damage(self, damage:int):
        self.hp -= damage
        print("Damaged!")

        if self.hp == 0: self.lives = False
        
    def set_color(self):
        if self.team == 1:
            self.color = (0,0,255)
        elif self.team == 2:
            self.color = (255,0,0)
        else:
            print("Invalid team!")