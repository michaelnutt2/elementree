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

import numpy as np

from elementree import utils
from cfg import *
from elementree.lidar.octree.OctreeNode import OctreeNode





class Octree:
    """Creates octree data structure from input point cloud"""
    def __init__(self, point_cloud: np.ndarray, bounds: (int, int, int, int, int, int)):
        self._points = point_cloud
        self._bounds = bounds
        self._k = 0
        self._max = None
        self._min = None
        self._x_scale_factor = None
        self._y_scale_factor = None
        self._z_scale_factor = None
        self._location = None
        self._parent_occupancy = 0
        self._parent = None
        self._children = None
        self._octant = None
        self._level = None

    def setup(self, levels: int, scale: bool = True):
        if scale:
            self._max = (2 ** self._k) - 1
            self._min = np.float32(0)
            self._scale_to_range()


    def build_tree(self):
        octants: list(int) = [

        ]
        ...

    def _scale_to_range(self):
        x, y, z, r = np.hsplit(self._points, 4)

        x, self._x_scale_factor = utils.scale_to_range(self._max, self._min, x)
        y, self._y_scale_factor = utils.scale_to_range(self._max, self._min, y)
        z, self._z_scale_factor = utils.scale_to_range(self._max, self._min, z)

        self._points = np.hstack((x, y, z, r))

    @property
    def scaling_factor(self):
        return self._x_scale_factor, self._y_scale_factor, self._z_scale_factor

    def _build_tree(self) -> None:

        bounds = utils.find_bounds(self._points)
        a = (bounds[X_MAX], bounds[Y_MAX], bounds[Z_MAX])
        c = (bounds[X_MIN], bounds[Y_MIN], bounds[Z_MIN])
        x_c, y_c, z_c = (
            utils.find_center_point(bounds[X_MAX], bounds[X_MIN]),
            utils.find_center_point(bounds[Y_MAX], bounds[Y_MIN]),
            utils.find_center_point(bounds[Z_MAX], bounds[Z_MIN])
        )
        b = (x_c, y_c, z_c)

        for point in self._points:
            if point[X] >= a[X]:
                if point[Y] >= a[Y]:
                    if point[Z] >= a[Z]:
                        node = OctreeNode(5, b, 1)
                    else:
                        node = OctreeNode(2, b, 1)

    def _create_node(self):
        ...

    # @property
    # def parent_occupancy(self):
    #     return self._parent_occupancy
    #
    # @parent_occupancy.setter
    # def parent_occupancy(self, value):
    #     self._parent_occupancy = value
    #
    # @property
    # def parent(self):
    #     return self._parent
    #
    # @property
    # def location(self) -> (int, int, int):
    #     return self._location
    #
    # @property
    # def level(self) -> int:
    #     return self._level
    #
    # @property
    # def octant(self) -> int:
    #     return self._octant
    #
    # @property
    # def children(self):
    #     return self._children