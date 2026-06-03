from .dto.pixel import Pixel

class GameMap:
    def __init__(self, side:int):
        if (side % 2    ) == 0:
            raise ValueError("Map must be a NxN matrix where N is an odd number")
        self.width = side
        self.height = side

        self.pixels: list[list[Pixel]] = [[Pixel() for _ in range(self.height)] for _ in range(self.width)]
        self.set_limit_walls()
        self.set_obstacles()

    def set_limit_walls(self):
        for i in range(self.width):
            self.pixels[i][0].obstructed = True
            self.pixels[i][self.height-1].obstructed = True
        for i in range(self.height):
            self.pixels[0][i].obstructed = True
            self.pixels[self.width-1][i].obstructed = True

    def set_obstacles(self):
        for i in range(self.width - 2):
            for j in range(self.height - 2):
                if (j % 2) and (i % 2):
                    self.pixels[i+1][j+1].obstructed = True

    def is_valid_pixel(self, x:int, y:int):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_pixel(self, x:int,y:int):
        if self.is_valid_pixel(x,y):
            return self.pixels[x][y]
    
    def obstruct_pixel(self, x:int, y:int):
        if self.is_valid_pixel(x,y):
            self.pixels[x][y].obstructed = True
    def desobstruct_pixel(self, x:int, y:int):
        if self.is_valid_pixel(x,y):
            self.pixels[x][y].obstructed = False

    def occupy_pixel(self, x:int, y:int):
        self.pixels[x][y].occupied = True
    def deoccupy_pixel(self, x:int, y:int):
        self.pixels[x][y].occupied = False
