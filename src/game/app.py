import pygame

from core.map import GameMap
from game.managers.event_management.keyboard.handler import KeyboardEvents

from .managers.entity_management.bomb_manager import BombManager
from .managers.entity_management.player_manager import PlayerManager

from game.configs.game_modes import only_bots, single_player, local


BOMB_RANGE = 5

class App:
    def __init__(self):
        self._running = False
        self._display_surf = None

        self.map = GameMap(15)
        self.BLOCK_SIZE = 60
        self.scoreboard = 180
        
        self.width = self.map.width * self.BLOCK_SIZE
        self.height = self.map.height * self.BLOCK_SIZE

        self.size = self.width + self.scoreboard, self.height
        self.fires = None

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("My Bomberman")
        self._display_surf = pygame.display.set_mode(
            self.size, 
            pygame.DOUBLEBUF
            )
        self._running = True

        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 20, bold = True)

        self.sprites = {
            "floor": self._load_sprite("assets/floor.png"),
            "wall": self._load_sprite("assets/wall.png"),
            "bomb": self._load_sprite("assets/bomb.png"),
            "fire": self._load_sprite("assets/fire.png"),
        }

        self.setup()

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
                            if self.champion:
                                if act["action"] == "RESTART":
                                    self.setup()

                        case "PLAY":
                            if self.champion == None:
                                if act["action"] == "BOMBING":
                                    self.bomb_manager.create_bomb(act["player"], act["pos"], BOMB_RANGE)

    def on_loop(self):  
        self.keyboard_events.on_keyhold()

        for player in self.player_manager.players:
            if player.is_alive:
                action = player.update(self.player_manager.players)
                if action and action["type"] == "PLAY" and action["action"] == "BOMBING":
                    self.bomb_manager.create_bomb(action["player"], action["pos"], BOMB_RANGE)

        self.bomb_manager.manage_bombs()

        current_status = self.player_manager.manage_players(self.fires)
        if self.champion is None and current_status is not None:
            self.champion = current_status

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

        self._game_render()
        self._scoreboard_render()

        if self.champion != None:
            self._game_over_render()
        
        pygame.display.flip()

    def _scoreboard_render(self):
        pygame.draw.line(self._display_surf, (255, 255, 255), (self.width,0), (self.width,self.height), 1)

        x = self.width + 10
        y = 15
        padding = 30

        title = self.font.render("Players", True, (160,160,160))
        self._display_surf.blit(title, (x,y))

        for player in self.player_manager.players:
            y += padding

            name_text = player.name
            name_color = player.color if player.is_alive else (100,100,100)

            hp_text = f"{player.hp}" if player.is_alive else "Exploded"
            hp_color = (0,160,0) if player.is_alive else (155,155,31)

            name_render = self.font.render(name_text, True, name_color)
            hp_render = self.font.render(hp_text, True, hp_color)

            self._display_surf.blit(name_render, (x,y))
            y += 20
            self._display_surf.blit(hp_render, (x,y))
        
        y += padding + 10
        pygame.draw.line(self._display_surf, (255, 255, 255), (self.width,y), (self.width+self.scoreboard,y), 1)
    
    def _game_render(self):
        active_fires = self.bomb_manager.get_all_fire_coords()
        self.fires = active_fires

        for x in range(self.map.width):
            for y in range(self.map.height):
                color = None 

                pixel = self.map.get_pixel(x, y)
                rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                
                self._display_surf.blit(self.sprites["floor"], rect)
                
                if pixel.obstructed:
                    self._display_surf.blit(self.sprites["wall"], rect)
                elif (x, y) in active_fires:
                    self._display_surf.blit(self.sprites["fire"], rect)
                    
                for bomb in self.bomb_manager.active_bombs:
                    if (x,y) == bomb.position and bomb.state == "TICKING":
                        self._display_surf.blit(self.sprites["bomb"], rect)

                for player in self.player_manager.players:
                    if player.is_alive and (x, y) == player.position:
                        current_sprite = player.get_current_sprite()
                        self._display_surf.blit(current_sprite, rect)
                
                if color is not None:
                    pygame.draw.rect(self._display_surf, color, rect)          

    def _game_over_render(self):
        pygame.draw.rect(self._display_surf, (0, 0, 0), (0, 0, self.width, self.height))

        game_over_text = "Game Over"

        if self.champion == "DRAW":

            champ_text = "DRAW - All of the living died in the same time."
            champ_color = (180, 180, 180)
        else:
            champ_text = f"The winner is " + self.champion.name
            champ_color = self.champion.color

        retry_text = "Type R to restart the game"

        game_over_render = self.font.render(game_over_text, True, (255,255,255))
        champ_render = self.font.render(champ_text, True, champ_color)
        retry_render = self.font.render(retry_text, True, (127,127,127))

        mid_x = self.width // 2
        mid_y = self.height // 2

        game_over_place = game_over_render.get_rect(center=(mid_x, mid_y-40))
        champ_place = champ_render.get_rect(center=(mid_x, mid_y))
        retry_place = retry_render.get_rect(center=(mid_x, mid_y+30))

        self._display_surf.blit(game_over_render, game_over_place)
        self._display_surf.blit(champ_render, champ_place)
        self._display_surf.blit(retry_render, retry_place)

    def setup(self):
        self.map = GameMap(15)
        self.champion = None

        self.player_manager = PlayerManager()
        self.bomb_manager = BombManager()

        only_bots(self)
        #single_player(self)
        #local(self)

        self.keyboard_events = KeyboardEvents(self)

    def _load_sprite(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (self.BLOCK_SIZE, self.BLOCK_SIZE))