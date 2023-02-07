import pygame

from . import settings

class Tile: 
    def __init__(self, x, y, texture_name): 
        self.x = x
        self.y = y
        self.texture_name = texture_name

    def render(self, surface):
        surface.blit(
            settings.TEXTURES[self.texture_name],
            (self.x, self.y)
        )


class TileMap:
    def __init__(self, num_tiles,  tile_texture_names):
        self.tiles = []

        rows = num_tiles // 16
        cols = num_tiles // 16
        tile_counter = 0

        for i in range(rows):
            for j in range(cols):
                self.tiles.append(
                    Tile(
                        j * settings.TILE_SIZE,
                        i * settings.TILE_SIZE,
                        tile_texture_names[tile_counter]
                    )
                )
                tile_counter += 1
            
    def render(self, surface):
        for tile in self.tiles:
            tile.render(surface)

