import pygame 



from . import settings
from .tilemap import TileMap


class Window:
    def __init__(self, title, state, action):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.WINDOW_HEIGHT)


        )
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.state = state 
        self.action = action 
        self.P = settings.P
        self.finish_state = True
        self.render_robot = True
        num_tiles = len(settings.P)
        tile_texture_names = ["ground" for _ in range(num_tiles)] #lista con la cant de tiles

        for _, action_table in self.P.items():
            for _, possibilities in action_table.items():
                for _, state_to, reward, terminated in possibilities:
                    if terminated:
                        if reward > 0.0:
                            self.finish_state = state_to
                        else:
                            tile_texture_names[state_to] = "ground" #mientras wasted


        #tile_texture_names[self.finish_state] = "ground"
        self.tilemap = TileMap(num_tiles, tile_texture_names)


    def reset(self, state, action):  
        self.state = state
        self.action = action
        self.render_robot = True
        for tile in self.tilemap.tiles:
            if tile.texture_name == "robbot_wasted":
                tile.texture_name = "ground"

    def update(self, state, action, reward, terminated):
        if terminated and reward == 0.0 and state != self.finish_state:
            self.tilemap.tiles[state].texture_name = "robot"
            settings.SOUNDS['win'].play()
        
            
            self.render_robot = False
            settings.SOUNDS['wasted'].play()
            
        self.state = state
        self.action = action
    
    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settings.TEXTURES['battery'],
            (self.tilemap.tiles[self.finish_state].x, self.tilemap.tiles[self.finish_state].y)

        )
        if self.render_robot:
            self.render_surface.blit(
                settings.TEXTURES['robot'][self.action],
                (self.tilemap.tiles[self.state].x, self.tilemap.tiles[self.state].y )
            )

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface, self.screen.get_size() #la escala
            ),
            (0, 0)
        )

        pygame.event.pump() #bloquea eventos keyboard etc
        pygame.display.update()


    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()