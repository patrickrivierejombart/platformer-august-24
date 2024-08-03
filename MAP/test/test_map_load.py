import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from MAP.map_handler import MapHandler, Level1


if __name__ == '__main__':
    map_handler = MapHandler()
    map_handler.load_level(level=Level1())
    print(map_handler.level_map.map)
