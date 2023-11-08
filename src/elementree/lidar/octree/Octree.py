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
import numpy as np

from elementree import utils


class Octree:
    """Creates octree data structure from input point cloud"""

    def __init__(self, point_cloud: np.ndarray, levels: int):
        self._point_cloud = point_cloud
        self._k = levels
        self._max = 2 ** levels - 1
        self._min = np.float32(0)
        self._x_scale_factor = None
        self._y_scale_factor = None
        self._z_scale_factor = None
        self._bounds = None

    def _scale_to_range(self):
        x, y, z, r = np.hsplit(self._point_cloud, 4)
        bounds = utils.find_bounds(self._point_cloud)

        x = utils.scale_to_range(self._max, self._min, x)
        y = utils.scale_to_range(self._max, self._min, y)
        z = utils.scale_to_range(self._max, self._min, z)

        self._point_cloud = np.hstack((x, y, z, r))

    

    @property
    def scaling_factor(self):
        return self._x_scale_factor, self._y_scale_factor, self._z_scale_factor
