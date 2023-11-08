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


class OctreeNode:
    def __init__(
            self,
            parent_occupancy: np.uint8 = 0,
            parent: 'OctreeNode' = None
    ):
        self._parent_occupancy = parent_occupancy
        self._parent = parent
        ...

    @property
    def parent_occupancy(self):
        return self._parent_occupancy

    @property
    def parent(self):
        return self._parent
