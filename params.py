import math
from typing import Tuple


class Colors:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    YELLOW = 255, 255, 0
    ROBOT = BLUE
    LIDAR_MEASUREMENT = GREEN


class SimParams:
    MAP: str = 'map_1.png'
    INITIAL_POSE: Tuple[int, int, float] = 400, 250, 0.0
    LIDAR_ANGLE: float = 2 * math.pi
    LIDAR_RANGE: int = 250
    LIDAR_RESOLUTION: int = 50
    LIDAR_ANGLE_SIGMA: float = 0.01
    LIDA_DISTANCE_SIGMA: float = 0.01
    SHOW_LIDAR_MEASUREMENTS = True


class PltParams:
    X_AMPLITUDE = 700
    Y_AMPLITUDE = 400
