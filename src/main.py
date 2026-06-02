from core.map import GameMap
from entities.player import Player

def main():
    side = 19
    map = GameMap(side)
    x = (side) // 2
    y = 1
    player = Player(map, [x,y], 1)

    player.place_bomb()

    map.print_map([x,y])

main()