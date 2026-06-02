import time

from core.map import GameMap

class Bomb:
    def __init__(self, bomber, position:tuple[int,int], explosion_site:int, damage:int):
        self.map: GameMap = bomber.map
        self.team:int = bomber.team
        self.position:tuple[int,int] = position

        self.explosion_site = explosion_site

        self.damage:int = damage

        self.birth_and_death()

    def occupy_position(self):
        self.map.obstruct_pixel(self.position[0], self.position[1])

    def desoccupy_position(self):
        self.map.desobstruct_pixel(self.position[0], self.position[1])

    def explode(self):
        self.desoccupy_position()

        x = self.position[0]
        y = self.position[1]

        self.map.lit_pixel(x,y)
        for i in range(1, self.explosion_site):
            time.sleep(0.3)
            self.map.lit_pixel(x+i, y)
            self.map.lit_pixel(x-i, y)
            self.map.lit_pixel(x, y+i)
            self.map.lit_pixel(x, y-i)
        time.sleep(0.5)
        
        self.map.unlit_pixel(x,y)
        for i in range(self.explosion_site):
            self.map.unlit_pixel(x+i, y)
            self.map.unlit_pixel(x-i, y)
            self.map.unlit_pixel(x, y+i)
            self.map.unlit_pixel(x, y-i)

    def birth_and_death(self):
        self.occupy_position()
        time.sleep(2)
        self.explode()