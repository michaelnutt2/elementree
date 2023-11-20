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

import numpy as np

from elementree import utils
import cfg

from elementree.lidar.octree.region import Region


class Octree:
    """Creates octree data structure from input point cloud"""

    def __init__(self, point_cloud: np.ndarray, bounds: Region):
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
        self._children: list[Union['Octree', None]] = [
            None, None, None, None, None, None, None, None
        ]
        self._octant = None
        self._level = None

    def setup(self, levels: int, scale: bool = True):
        if scale:
            self._max = (2 ** self._k) - 1
            self._min = np.float32(0)
            self._scale_to_range()

    def build_tree(self):
        a = (
            self._bounds[cfg.X_MIN],
            self._bounds[cfg.Y_MIN],
            self._bounds[cfg.Z_MIN]
        )
        c = (
            self._bounds[cfg.X_MAX],
            self._bounds[cfg.Y_MAX],
            self._bounds[cfg.Z_MAX]
        )
        b = (
            utils.find_center_point(a[cfg.X], c[cfg.X]),
            utils.find_center_point(a[cfg.Y], c[cfg.Y]),
            utils.find_center_point(a[cfg.Z], c[cfg.Z])
        )
        octant_regions: list['Region'] = [
            Region((c[cfg.X], c[cfg.Y], c[cfg.Z], b[cfg.X], b[cfg.Y], b[cfg.Z])),
            Region((b[cfg.X], c[cfg.Y], c[cfg.Z], a[cfg.X], b[cfg.Y], b[cfg.Z])),
            Region((b[cfg.X], b[cfg.Y], c[cfg.Z], a[cfg.X], a[cfg.Y], b[cfg.Z])),
            Region((c[cfg.X], b[cfg.Y], c[cfg.Z], b[cfg.X], a[cfg.Y], b[cfg.Z])),
            Region((c[cfg.X], b[cfg.Y], b[cfg.Z], b[cfg.X], a[cfg.Y], a[cfg.Z])),
            Region((b[cfg.X], b[cfg.Y], b[cfg.Z], a[cfg.X], a[cfg.Y], a[cfg.Z])),
            Region((b[cfg.X], c[cfg.Y], b[cfg.Z], a[cfg.X], b[cfg.Y], a[cfg.Z])),
            Region((c[cfg.X], c[cfg.Y], b[cfg.Z], b[cfg.X], b[cfg.Y], a[cfg.Z]))
        ]

        octants: list[(int, int, int)] = [
            [None], [None], [None], [None], [None], [None], [None], [None]
        ]

        for point in self._points:
            for i in range(8):
                if octant_regions[i].within_bounds(point):
                    octants[i].append(point)

        for i, octant in enumerate(octants):
            child = None
            # TODO: Fix this so that leaf nodes are correctly entered instead of
            #   recursing forever
            if octant:
                child = Octree(octant, octant_regions[i])
            self._children[i] = child

    def _scale_to_range(self):
        x, y, z, r = np.hsplit(self._points, 4)

        x, self._x_scale_factor = utils.scale_to_range(self._max, self._min, x)
        y, self._y_scale_factor = utils.scale_to_range(self._max, self._min, y)
        z, self._z_scale_factor = utils.scale_to_range(self._max, self._min, z)

        self._points = np.hstack((x, y, z, r))

    @property
    def scaling_factor(self):
        return self._x_scale_factor, self._y_scale_factor, self._z_scale_factor

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
