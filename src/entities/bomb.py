from pygame import time as t
from core.map import GameMap

class Bomb:
    def __init__(self, bomber, position:tuple[int,int], explosion_site:int, damage:int):
        self.map: GameMap = bomber.map
        self.team:int = bomber.team
        self.position:tuple[int,int] = position

        self.explosion_site:int = explosion_site
        self.damage:int = damage

        self.creation_time = t.get_ticks()
        self.last_update_time = self.creation_time

        self.occupy_position()
        self.get_expansion_ranges()

    def occupy_position(self):
        self.state = "TICKING"

        self.current_radius = 1
        self.map.obstruct_pixel(self.position[0], self.position[1])

    def desoccupy_position(self):
        self.map.desobstruct_pixel(self.position[0], self.position[1])
    
    def explode(self):
        if self.current_radius > max(self.ranges):
            self.state = "LINGERING"
            return

        x, y = self.position
        r = self.current_radius
        
        self.map.lit_pixel(x, y)
        
        if r <= self.ranges[0]: self.map.lit_pixel(x + r, y)
        if r <= self.ranges[1]: self.map.lit_pixel(x, y + r)
        if r <= self.ranges[2]: self.map.lit_pixel(x - r, y)
        if r <= self.ranges[3]: self.map.lit_pixel(x, y - r)
        
        self.current_radius += 1

    def clear_fire(self):
        x, y = self.position
        self.map.unlit_pixel(x, y)
        
        for r in range(1, self.ranges[0] + 1): self.map.unlit_pixel(x + r, y)
        for r in range(1, self.ranges[1] + 1): self.map.unlit_pixel(x, y + r)
        for r in range(1, self.ranges[2] + 1): self.map.unlit_pixel(x - r, y)
        for r in range(1, self.ranges[3] + 1): self.map.unlit_pixel(x, y - r)

    def get_expansion_ranges(self):
        self.ranges = [self.explosion_site, self.explosion_site, self.explosion_site, self.explosion_site]

        to_go = [(1,0), (0,1), (-1,0), (0,-1)]

        for i, (dx,dy)in enumerate(to_go):
            for j in range(1, self.explosion_site + 1):
                x = self.position[0] + (dx*j)
                y = self.position[1] + (dy*j)

                pixel = self.map.get_pixel(x,y)

                if pixel == None or pixel.obstructed:
                    self.ranges[i] = j - 1
                    break

    def life_and_death(self):
        now = t.get_ticks()

        if ( self.state == "TICKING" ) and ( (now - self.creation_time) >= 2000 ):
                self.desoccupy_position()

                self.state = "EXPLODING"
                self.last_update_time = now 

        elif self.state == "EXPLODING":
            if now - self.last_update_time >= 50:
                self.explode()
                self.last_update_time = now 

            if now - self.last_update_time >= 50:
                if self.current_radius < self.explosion_site:
                    x, y = self.position
                    r = self.current_radius
                    
                    self.map.lit_pixel(x + r, y)
                    self.map.lit_pixel(x - r, y)
                    self.map.lit_pixel(x, y + r)
                    self.map.lit_pixel(x, y - r)
                    
                    self.current_radius += 1
                    self.last_update_time = now
                else:
                    self.state = "LINGERING"
                    self.last_update_time = now

        elif self.state == "LINGERING":
            if now - self.last_update_time >= 1000:
                self.clear_fire()
                self.state = "DEAD"

        elif self.state == "DEAD":
            pass