import pygame

from core.map import GameMap

from entities.player import Player
from entities.bomb import Bomb

class App:
    def __init__(self):
        self._running = False
        self._display_surf = None
        
        self.map = GameMap(15)
        
        self.BLOCK_SIZE = 40 
        self.width = self.map.width * self.BLOCK_SIZE
        self.height = self.map.height * self.BLOCK_SIZE

        self.size = self.width, self.height

        self.active_bombs:list[Bomb] = []
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        self._running = True

        self.player_1:Player = Player(self.map, (self.map.width//2, 2), 1)
        self.player_2:Player = Player(self.map, (self.map.width//2, self.map.height-2), 2)

        kaboom = self.player_1.place_bomb()
        if kaboom:
            self.active_bombs.append(kaboom)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
    def on_loop(self):
        self.manage_bombs()
        pass
        
    def on_render(self):
        self._display_surf.fill((0, 0, 0))

        for x in range(self.map.width):
            for y in range(self.map.height):
                pixel = self.map.get_pixel(x, y)
                rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                
                if pixel.obstructed:
                    color = (128, 128, 128)
                elif pixel.burning:
                    color = (255, 69, 0)
                else:
                    color = (34, 139, 34)

                if (x,y) == self.player_1.position:
                    color = (0,0,255)
                elif (x,y) == self.player_2.position:
                    color = (255,0,0)
                
                pygame.draw.rect(self._display_surf, color, rect)                
                pygame.draw.rect(self._display_surf, (20, 20, 20), rect, 1)

        pygame.display.flip()
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        clock = pygame.time.Clock()
 
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            clock.tick(60)
            
        self.on_cleanup()

    def manage_bombs(self):
        for bomb in self.active_bombs:
            bomb.life_and_death()
            
        for bomb in self.active_bombs:
            if bomb.state == "DEAD":
                self.active_bombs.remove(bomb)

        