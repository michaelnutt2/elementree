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
from collections import deque
from typing import Union

import numpy as np

from elementree import utils
from elementree.lidar.octree import cfg

from elementree.lidar.octree.Region import Region


class Octree:
    """
    Octree data structure. Constructor takes in a np ndarray or list of 3 int
    tuples as the point cloud and a Region object that defines the area of the
    points. If the points need to be scaled, call setup(levels) with number of
    levels of the tree
    """

    def __init__(
            self,
            point_cloud: Union[np.ndarray, list[(int, int, int)]],
            bounds: Region,
            _level: int = 0
    ):
        self._points: list[(int, int, int)]
        if type(point_cloud) is np.ndarray:
            self._points = point_cloud.tolist()
        else:
            self._points = point_cloud
        self._bounds: Region = bounds
        self._k: int = 0
        self._max: Union[np.float32, None] = None
        self._min: Union[np.float32, None] = None
        self._x_scale_factor: int
        self._y_scale_factor: int
        self._z_scale_factor: int
        self._location: (int, int, int) = None
        self._occupancy: np.uint8 = np.uint8(0)
        self._children: list[Union['Octree', None]] = [
            None, None, None, None, None, None, None, None
        ]
        self._octant: int = -1
        self._level: int = _level

    def setup(self, levels):
        self._max = (2 ** levels) - 1
        self._min = np.float32(0)
        self._bounds = Region(x_max=self._max, y_max=self._max, z_max=self._max,
                              x_min=0, y_min=0, z_min=0)
        self._scale_to_range()

    def build_tree(self):
        """
        Build the octree out of the points in self._points. Creates a new octree
        object at each node while there are points available to sort.
        """
        # Checks if this is a leaf node to break out of the recursion.
        # if type(self._points) is np.ndarray:
        #     self._points = self._points.tolist()

        if len(self._points) <= 1:
            return

        # a, b, and c used to define the octant regions of the space
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
        self.location = b
        octant_regions: list['Region'] = [
            Region(
                x_min=b[cfg.X], y_min=b[cfg.Y], z_min=b[cfg.Z],
                x_max=c[cfg.X], y_max=c[cfg.Y], z_max=c[cfg.Z]
            ),
            Region(
                x_min=a[cfg.X], y_min=b[cfg.Y], z_min=b[cfg.Z],
                x_max=b[cfg.X], y_max=c[cfg.Y], z_max=c[cfg.Z]
            ),
            Region(
                x_min=a[cfg.X], y_min=a[cfg.Y], z_min=b[cfg.Z],
                x_max=b[cfg.X], y_max=b[cfg.Y], z_max=c[cfg.Z]
            ),
            Region(
                x_min=b[cfg.X], y_min=a[cfg.Y], z_min=b[cfg.Z],
                x_max=c[cfg.X], y_max=b[cfg.Y], z_max=c[cfg.Z]
            ),
            Region(
                x_min=b[cfg.X], y_min=a[cfg.Y], z_min=a[cfg.Z],
                x_max=c[cfg.X], y_max=b[cfg.Y], z_max=b[cfg.Z],
            ),
            Region(
                x_min=a[cfg.X], y_min=a[cfg.Y], z_min=a[cfg.Z],
                x_max=b[cfg.X], y_max=b[cfg.Y], z_max=b[cfg.Z]
            ),
            Region(
                x_min=a[cfg.X], y_min=b[cfg.Y], z_min=a[cfg.Z],
                x_max=b[cfg.X], y_max=c[cfg.Y], z_max=b[cfg.Z],
            ),
            Region(
                x_min=b[cfg.X], y_min=b[cfg.Y], z_min=a[cfg.Z],
                x_max=c[cfg.X], y_max=c[cfg.Y], z_max=b[cfg.Z]
            )
        ]

        # populating a list of octants that will hold the points as they are
        # sorted
        octants: list[list[(int, int, int)]] = [
            [], [], [], [], [], [], [], []
        ]

        # iterates through each point and octant region to see if the point
        # fits in that region bucket
        for point in self._points:
            for i in range(8):
                if octant_regions[i].within_bounds(point):
                    octants[i].append(point)

        # creates new children nodes for each octant that is not empty
        for i, octant in enumerate(octants):
            if len(octant) != 0:
                self.children[i] = self._create_node(octant, octant_regions[i])
                self.children[i].octant = i
                self.occupancy += 2 ** i

    def _create_node(
            self,
            octant: list[(int, int, int)],
            region: 'Region'
    ) -> Union['Octree', None]:
        if len(octant) == 0:
            return None

        ret = Octree(point_cloud=octant, bounds=region, _level=self._level+1)
        return ret

    def _scale_to_range(self):
        points = np.array(self._points)
        x, y, z, r = np.hsplit(points, 4)

        x, self._x_scale_factor = utils.scale_to_range(self._max, self._min, x)
        y, self._y_scale_factor = utils.scale_to_range(self._max, self._min, y)
        z, self._z_scale_factor = utils.scale_to_range(self._max, self._min, z)

        points = np.hstack((x, y, z, r))
        self._points = points.tolist()


    def bft(self) -> list[np.uint8]:
        occupancy: list[np.uint8] = []
        nodes = deque([self])
        while len(nodes) > 0:
            node = nodes.popleft()
            for i in range(8):
                child = node.children[i]
                if child:
                    nodes.append(child)
            occupancy.append(node.occupancy)
        return occupancy

    def dft(self) -> list[np.uint8]:
        ...

    @property
    def scaling_factor(self):
        return self._x_scale_factor, self._y_scale_factor, self._z_scale_factor

    @property
    def bounds(self):
        return self._bounds

    @property
    def occupancy(self):
        return self._occupancy

    @occupancy.setter
    def occupancy(self, value):
        if value > 255:
            value = 255
        self._occupancy = value

    @property
    def location(self) -> (int, int, int):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def level(self) -> int:
        return self._level

    @property
    def octant(self) -> int:
        return self._octant

    @octant.setter
    def octant(self, value):
        self._octant = value

    @property
    def children(self) -> list[Union['Octree', None]]:
        return self._children

    @children.setter
    def children(self, value: Union['Octree', None]):
        self._children = value
