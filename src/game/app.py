import pygame

from core.map import GameMap
from game.managers.event_management.keyboard.handler import KeyboardEvents

from .managers.entity_management.bomb_manager import BombManager
from .managers.entity_management.player_manager import PlayerManager

class App:
    def __init__(self):
        self._running = False
        self._display_surf = None

        self.map = GameMap(15)
        self.BLOCK_SIZE = 60
        
        self.width = self.map.width * self.BLOCK_SIZE
        self.height = self.map.height * self.BLOCK_SIZE

        self.size = self.width, self.height

    def on_init(self):
        self.setup()
        pygame.init()
        
        pygame.display.set_caption("My Bomberman")
        self._display_surf = pygame.display.set_mode(
            self.size, 
            pygame.DOUBLEBUF
            )
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            actions =  self.keyboard_events.on_keydown(event)
            if actions:
                for act in actions:
                    match act["type"]:
                        case "WINDOW_COMMAND":
                            if act["action"] == "CLOSE":
                                self._running = False
                            if act["action"] == "MINIMIZE":
                                pygame.display.iconify()

                        case "GAME_COMMAND":
                            if act["action"] == "RESTART":
                                self.setup()
                                
                        case "PLAY":
                            if act["action"] == "BOMBING":
                                self.bomb_manager.create_bomb(act["player"], act["pos"])

    def on_loop(self):
        self.bomb_manager.manage_bombs()
        self.keyboard_events.on_keyhold()
        pass
        
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
    
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        active_fires = self.bomb_manager.get_all_fire_coords()

        for x in range(self.map.width):
            for y in range(self.map.height):
                pixel = self.map.get_pixel(x, y)
                rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                
                if pixel.obstructed:
                    color = (128, 128, 128)
                elif (x, y) in active_fires:
                    color = (255, 69, 0)
                else:
                    color = (34, 139, 34)
                
                for player in self.player_manager.players:
                    if (x,y) == player.position:
                        color = player.color
                for bomb in self.bomb_manager.active_bombs:
                    if (x,y) == bomb.position and bomb.state == "TICKING":
                        color = (0,0,0)
                
                pygame.draw.rect(self._display_surf, color, rect)          
                pygame.draw.rect(self._display_surf, (20, 20, 20), rect, 1)

                for player in self.player_manager.players:
                    if (x, y) == player.position:
                        cx = x * self.BLOCK_SIZE + self.BLOCK_SIZE // 2
                        cy = y * self.BLOCK_SIZE + self.BLOCK_SIZE // 2
                        
                        dx, dy = player.facing_dir
                        
                        tip = (cx + dx * 15, cy + dy * 15)
                        
                        left_base = (cx + dy * 8, cy - dx * 8)
                        right_base = (cx - dy * 8, cy + dx * 8)
                        
                        pygame.draw.polygon(self._display_surf, (255, 255, 255), [tip, left_base, right_base])

        pygame.display.flip()

    def setup(self):
        self.map = GameMap(15)

        self.player_manager = PlayerManager()
        self.bomb_manager = BombManager()

        self.create_players()

        self.keyboard_events = KeyboardEvents(self)

    def create_players(self):
        map = self.map

        p1_pos = (map.width//2, 1)
        p2_pos = (map.width//2, map.height-2)

        self.player_manager.create_player(map, p1_pos, 1, "Bluey")
        self.player_manager.create_player(map, p2_pos, 2, "Redy")