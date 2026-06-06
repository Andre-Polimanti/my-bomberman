from entities.player import Player

class PlayerManager:
    def __init__(self):
        self.players:list[Player] = []
        self.the_living:list[Player] = []

        self.winner = None

    def create_player(self, map, position:tuple[int,int], team:int, name:str):
        player = Player(map, position, team, name)

        self.players.append(player)
        self.the_living.append(player)

        return player
        
    def manage_players(self, fires):
        for player in self.players:
            player.life_and_death(fires)
            if player.lives == False:
                self._kill_zombie_player(player)

    def get_player_on_pixel(self, x:int, y:int):
        for player in self.players:
            if (x,y) == player.position:
                return player
        return None
    
    def get_player_cords(self):
        cords = []
        for player in self.players:
            cords.append(player.position)
        return cords

    def _kill_zombie_player(self, player):
        if player in self.the_living:
            self.the_living.remove(player)
            self._check_for_winner()

    def _check_for_winner(self):
        if len(self.the_living) == 1:
            self.winner = self.the_living[0]