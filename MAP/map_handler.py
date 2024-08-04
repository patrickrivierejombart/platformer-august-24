"""
file: map_handler.py
synopsis: Handles all map related tasks (Map load, TODO)
"""


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
            with open(os.path.join(os.path.dirname(__file__), 'level_saves', level.level_name), 'r') as level_file:
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
    MAPPING_FILE = 'mapping.yml'

    def __init__(self) -> None:
        self.level_map = LevelMap(level=Level1())
        self.__load_mapping()
    
    def __load_mapping(self):
        import os
        import yaml
        self.mapping = None
        print(self.MAPPING_FILE)
        with open(os.path.join(os.path.dirname(__file__), 'level_saves', self.MAPPING_FILE), 'r') as mapping_file:
            try:
                self.mapping = yaml.safe_load(mapping_file)
            except Exception:
                raise MapHandlerException(f'Mapping file {self.MAPPING_FILE} is either missing or corrupt.')
    
    def __getitem__(self, __name):
        try:
            assert __name in self.mapping
            return self.mapping[__name]
        except AssertionError:
            raise MapHandlerException(f'Symbol {__name} can not be found in mapping {self.MAPPING_FILE}.')

    def load_level(self, level: Level):
        self.level_map = LevelMap(level=level)
