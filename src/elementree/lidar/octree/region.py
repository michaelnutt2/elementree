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
        self.x_max = bounds[cfg.X_MAX]
        self.x_min = bounds[cfg.X_MIN]
        self.y_max = bounds[cfg.Y_MAX]
        self.y_min = bounds[cfg.Y_MIN]
        self.z_max = bounds[cfg.Z_MAX]
        self.z_min = bounds[cfg.Z_MIN]

    def within_bounds(self, point: (int, int, int)) -> bool:
        x, y, z = point[cfg.x], point[cfg.y], point[cfg.z]
        if (self.x_max > x >= self.x_min and
                self.y_max > y >= self.y_min and
                self.z_max > z >= self.z_min):
            return True
        return False
