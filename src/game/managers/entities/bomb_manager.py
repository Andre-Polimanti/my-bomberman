from entities.bomb import Bomb

class BombManager:
    def __init__(self):
        self.active_bombs:list[Bomb] = []

    def create_bomb(self, player):
        bomb = player.place_bomb() 
        if bomb:
            self.active_bombs.append(bomb)

    def get_all_fire_coords(self):
        all_fire = set()
        for bomb in self.active_bombs:
            all_fire.update(bomb.fire_coords)
        return all_fire
    
    def manage_bombs(self):
        for bomb in self.active_bombs:
            bomb.life_and_death()
            
        for bomb in self.active_bombs:
            if bomb.state == "DEAD":
                self.active_bombs.remove(bomb)
    
    def get_bomb_cords(self):
        cords = []
        for bomb in self.active_bombs:
            cords.append(bomb.position)
        return cords
    
    def get_bomb_by_cord(self, x:int, y:int):
        for bomb in self.active_bombs:
            if bomb.position == (x,y):
                return bomb
        return None