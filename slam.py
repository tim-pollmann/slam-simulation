from interface import Interface
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import math
from params import PltParams, Colors
from typing import Any


class Slam:
    def __init__(self, interface: Interface) -> None:
        self._interface = interface
        self._robot_pose = 0, 0, 0.0
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot()
        self._robot_color = tuple(proportion / 255 for proportion in Colors.ROBOT)
        self._lidar_measurement_color = tuple(proportion / 255 for proportion in Colors.LIDAR_MEASUREMENT)

    def start(self) -> None:
        _ = anim.FuncAnimation(self._fig, self._update)
        plt.show()

    def _update(self, _: Any) -> None:
        pointcloud_x, pointcloud_y = [], []
        for point in self._interface.point_cloud:
            x = self._robot_pose[0] + math.cos(point[0]) * point[1]
            y = self._robot_pose[1] + math.sin(point[0]) * point[1]
            pointcloud_x.append(x)
            pointcloud_y.append(y)
        self._ax.clear()
        self._ax.set_xlim([- PltParams.X_AMPLITUDE, PltParams.X_AMPLITUDE])
        self._ax.set_ylim([PltParams.Y_AMPLITUDE, - PltParams.Y_AMPLITUDE])
        self._ax.scatter(pointcloud_x, pointcloud_y, color=self._lidar_measurement_color)
        self._ax.scatter(0.0, 0.0, color=self._robot_color)
