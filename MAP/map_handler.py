

class Level:
    @property
    def level_name(self):
        """
        """


class Level1(Level):
    # Return name of the level file loaded
    @property
    def level_name(self):
        return 'starter-village.sav'


class MapHandlerException(Exception):
    pass


class LevelMap:
    """
    Map stored into memory for loaded level
    """
    class LevelLoader:
        """
        """
        def load_save(self, level: Level):
            import os
            map_rows = None
            with open(os.path.join(os.path.dirname(__file__), 'level_saves', level.level_name)) as level_file:
                map_rows = [[symbol for symbol in line.strip('\n').split('|')] for line in level_file]
                try:
                    row_length = len(map_rows[0])
                    assert all(len(row)==row_length for row in map_rows)
                except AssertionError:
                    raise MapHandlerException(f'Save file {level.level_name} is corrupt. Each row must be the same length.')
                except Exception:
                    raise MapHandlerException(f'Save file {level.level_name} is empty.')
            return map_rows
        
    def __init__(self, level: Level):
        self._current_map = None
        self.__load_level_save(level=level)

    def __load_level_save(self, level: Level):
        self._current_map = self.LevelLoader().load_save(level=level)
    
    @property
    def map(self):
        return self._current_map


class MapHandler:
    def __init__(self) -> None:
        self.level_map = LevelMap(level=Level1())

    def load_level(self, level: Level):
        self.level_map = LevelMap(level=level)
    
    symbol_meaning = {
        '#': 'map_block',
        '>': 'level_portal',
        'S': 'shop',
        'N': 'npc_character',
        'L': 'loot_box',
        'C': 'checkpoint',
        ' ': 'empty'
    }
