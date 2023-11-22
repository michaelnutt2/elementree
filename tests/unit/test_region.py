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

import unittest


class RegionTest(unittest.TestCase):
    def setUp(self):
        from elementree.lidar.octree.Region import Region
        self.region = Region(x_max=5, x_min=-5, y_max=5, y_min=-5, z_max=5, z_min=-5)

    def test_region_is_within_bounds(self):
        within_bounds = self.region.within_bounds(point=(4, 2, 1))
        self.assertTrue(within_bounds)

    def test_region_is_not_within_bounds(self):
        within_bounds = self.region.within_bounds(point=(14, 2, 1))
        self.assertFalse(within_bounds)


if __name__ == '__main__':
    unittest.main()
