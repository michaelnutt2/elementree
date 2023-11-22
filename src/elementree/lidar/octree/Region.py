# ------------------------------------------------------------------------------
#      ElemenTree - Python library of tree data structures
#      Copyright (C) 2023  Michael Nutt
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------
from typing import Union

from elementree.lidar.octree import cfg


class Region:
    """
    Defines an area.
    """

    def __init__(
            self,
            x_max: int,
            y_max: int,
            z_max: int,
            x_min: int,
            y_min: int,
            z_min: int,
    ):
        if x_max < x_min:
            raise ValueError
        if y_max < y_min:
            raise ValueError
        if z_max < z_min:
            raise ValueError

        self._bounds = {
            'x_max': x_max,
            'x_min': x_min,
            'y_max': y_max,
            'y_min': y_min,
            'z_max': z_max,
            'z_min': z_min
        }

    def within_bounds(self, point: (int, int, int, int)) -> bool:
        x, y, z = point[cfg.X], point[cfg.Y], point[cfg.Z]
        if (self._bounds[cfg.X_MAX] > x >= self._bounds[cfg.X_MIN] and
                self._bounds[cfg.Y_MAX] > y >= self._bounds[cfg.Y_MIN] and
                self._bounds[cfg.Z_MAX] > z >= self._bounds[cfg.Z_MIN]):
            return True
        return False

    def __getitem__(self, item):
        return self._bounds[item]
