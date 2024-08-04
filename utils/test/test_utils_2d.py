import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.utils_2d import acceleration, Force


if __name__ == '__main__':
    acc = acceleration(mass=2, forces=[Force(1,0), Force(-99,-1)])
    print(acc.vector)
