import pygame
import json

NEIGHBOR_OFFSETS = [
    (-4, -4), (-3, -4), (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4), (3, -4), (4, -4), (5, -4),
    (-4, -3), (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3), (5, -3),
    (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), (5, -2),
    (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1),
    (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
    (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
    (-4, 3), (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
    (-4, 4), (-3, 4), (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
    (-4, 5), (-3, 5), (-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)
    ]


class CollisionMap:
    def __init__(self, tile_size=8):
        self.ground = {}
        self.wall = {}
        self.ceiling = {}
        self.jump_through = {}
        self.tile_size = tile_size
    
    def tiles_around(self, pos):
        tiles = {'ground': [], 'wall': [], 'ceiling': [], 'jump_through': []}
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.ground:
                tiles['ground'].append(self.ground[check_loc])
            elif check_loc in self.wall:
                tiles['wall'].append(self.wall[check_loc])
            elif check_loc in self.ceiling:
                tiles['ceiling'].append(self.ceiling[check_loc])
            elif check_loc in self.jump_through:
                tiles['jump_through'].append(self.jump_through[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        tiles = self.tiles_around(pos)
        rects = {
            'ground': [pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)
                        for tile in tiles['ground']
            ],
            'wall': [pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)
                     for tile in tiles['wall']
            ],
            'ceiling': [pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)
                     for tile in tiles['ceiling']
            ],
            'jump_through': [pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)
                     for tile in tiles['jump_through']
            ]
        }
        return rects

    def all_collisions(self):
        rects = {'ground': [], 'wall': [], 'ceiling': [], 'jump_through': []}
        for collision_item in self.ground.values():
            rects['ground'].append(pygame.Rect(collision_item['pos'][0] * self.tile_size, collision_item['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        for collision_item in self.wall.values():
            rects['wall'].append(pygame.Rect(collision_item['pos'][0] * self.tile_size, collision_item['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        for collision_item in self.ceiling.values():
            rects['ceiling'].append(pygame.Rect(collision_item['pos'][0] * self.tile_size, collision_item['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        for collision_item in self.jump_through.values():
            rects['jump_through'].append(pygame.Rect(collision_item['pos'][0] * self.tile_size, collision_item['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.ground = map_data['ground']
        self.wall = map_data['wall']
        self.ceiling = map_data['ceiling']
        self.jump_through = map_data['jump_through']
        self.tile_size = map_data['tile_size']
