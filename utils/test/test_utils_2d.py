import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.utils_2d import acceleration, Force, position, Position, Speed


if __name__ == '__main__':
    pos_x0 = Position(10, 10)
    jump_vector_list = [
        Force(0, 0),
        Force(0, -0.5),
        Force(0, -0.7),
        Force(0, -0.87),
        Force(0, -1),
        Force(0, -0.87),
        Force(0, -0.7),
        Force(0, -0.5),
        Force(0, 0),
        Force(0, 0.5),
        Force(0, 0.7),
        Force(0, 0.87),
        Force(0, 1),
        Force(0, 0.87),
        Force(0, 0.7),
        Force(0, 0.5),
        Force(0, 0)
    ]
    for jump_vector in jump_vector_list:
        pos_x0.update_force(force_list=[jump_vector])
        pos_x0.update_speed(speed_list=[Speed(1, 0)])
        pos_x0.increment_position(dt = 1)
        print(pos_x0.vector)
