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
import cfg


class Region:
    def __init__(self, bounds: (int, int, int, int, int, int)):
        self._bounds = bounds

    def within_bounds(self, point: (int, int, int)) -> bool:
        x, y, z = point[cfg.X], point[cfg.Y], point[cfg.Z]
        if (self._bounds[cfg.X_MAX] > x >= self._bounds[cfg.X_MIN] and
                self._bounds[cfg.Y_MAX] > y >= self._bounds[cfg.Y_MIN] and
                self._bounds[cfg.Z_MAX] > z >= self._bounds[cfg.Z_MIN]):
            return True
        return False

    def __getitem__(self, item):
        return self._bounds[item]
