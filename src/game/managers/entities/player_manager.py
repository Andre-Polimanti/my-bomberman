from entities.player import Player

class PlayerManager:
    def __init__(self):
        self.players:list[Player] = []

    def create_player(self, map, position:tuple[int,int], team:int, name:str):
        player = Player(map, position, team, name)
        self.players.append(player)
        
    def get_player_on_pixel(self, x:int, y:int):
        for player in self.players:
            if (x,y) == player.position:
                return Player
        return None
    
    def get_player_cords(self):
        cords = []
        for player in self.players:
            cords.append(player.position)

        return cords