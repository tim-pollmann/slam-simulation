from typing import Tuple, List


class Interface:
    def __init__(self) -> None:
        self._point_cloud = []

    @property
    def point_cloud(self) -> List[Tuple[float, float]]:
        return self._point_cloud

    def set_point_cloud(self, point_cloud: List[Tuple[float, float]]) -> None:
        self._point_cloud = point_cloud
