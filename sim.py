import os
import pygame as pg
import numpy as np
import math
from typing import Tuple, List
from params import SimParams, Colors
from interface import Interface


class Sim:
    def __init__(self, robot_interface: Interface) -> None:
        self._robot_interface = robot_interface
        self._robot_pose = SimParams.INITIAL_POSE
        pg.init()
        map_path = os.path.join(os.path.dirname(__file__), 'maps', SimParams.MAP)
        self._map = pg.image.load(map_path)
        self._width, self._height = self._map.get_size()
        self._screen = pg.display.set_mode((self._width, self._height))
        self._redraw()

    def start(self) -> int:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
            self._update_robot_pose()
            point_cloud = self._do_lidar_scan()
            self._robot_interface.set_point_cloud(point_cloud)
            self._redraw(point_cloud)

    def _update_robot_pose(self) -> None:
        self._robot_pose = self._robot_pose[0] + 1, self._robot_pose[1], self._robot_pose[2]

    def _do_lidar_scan(self) -> List[Tuple[float, float]]:
        point_cloud = []
        lidar_scan_start_angle = (
            self._robot_pose[2]
            if SimParams.LIDAR_ANGLE == 2 * math.pi  # 360 degree sensor
            else self._robot_pose[2] - SimParams.LIDAR_ANGLE / 2
        )
        for angle in np.linspace(lidar_scan_start_angle, lidar_scan_start_angle + SimParams.LIDAR_ANGLE, SimParams.LIDAR_RESOLUTION, False):
            for distance in range(0, SimParams.LIDAR_RANGE):
                possible_obstacle_x = int(self._robot_pose[0] + math.cos(angle) * distance)
                possible_obstacle_y = int(self._robot_pose[1] + math.sin(angle) * distance)
                if 0 <= possible_obstacle_x < self._width and 0 <= possible_obstacle_y < self._height:
                    color = self._screen.get_at((possible_obstacle_x, possible_obstacle_y))
                    if (color[0], color[1], color[2]) == Colors.BLACK:
                        angle, distance = Sim._add_noise([angle, distance], [SimParams.LIDAR_ANGLE_SIGMA, SimParams.LIDA_DISTANCE_SIGMA])
                        point_cloud.append((angle, distance))
                        break
        return point_cloud

    def _redraw(self, point_cloud: List[Tuple[float, float]] = []) -> None:
        self._screen.blit(self._map, (0, 0))
        pg.draw.circle(self._screen, Colors.ROBOT, (self._robot_pose[0], self._robot_pose[1]), 5.0)
        if SimParams.SHOW_LIDAR_MEASUREMENTS:
            for point in point_cloud:
                pg.draw.circle(self._screen, Colors.LIDAR_MEASUREMENT, (
                    int(self._robot_pose[0] + math.cos(point[0]) * point[1]),
                    int(self._robot_pose[1] + math.sin(point[0]) * point[1])
                ), 5.0)
            pg.display.flip()

    def _add_noise(exact_values: List[float], sigmas: List[float]) -> List[float]:
        assert len(exact_values) == len(sigmas)
        mean = np.array(exact_values)
        cov = np.diag(np.array(sigmas) ** 2)
        return np.random.multivariate_normal(mean, cov).tolist()
