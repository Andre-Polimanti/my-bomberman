from game.app import App

# def main():
#     side = 19
#     map = GameMap(side)
#     x, y = (side) // 2, 1
#     player = Player(map, [x,y], 1)
#     player.place_bomb()
#     map.print_map([x,y])
# main()

def main():
    app = App()
    app.on_execute()
main()