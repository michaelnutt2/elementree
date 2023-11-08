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
import numpy as np


class OctreeTestCase(unittest.TestCase):
    def setUp(self):
        from elementree.lidar.octree import Octree as oc
        self.array = np.array([
            [1.52, 2.456, 0.516, 5],
            [5.213, 2.16, 1.566, 6],
            [3.15, 4.21, -1.25, 7]
        ])
        self.tree = oc.Octree(self.array, 16)

    def test_scale_to_range(self):
        self.tree._scale_to_range()
        self.assertEqual(0, self.tree._point_cloud[0][0])
        self.assertEqual(9462, self.tree._point_cloud[0][1])
        self.assertEqual(41099, self.tree._point_cloud[0][2])
        self.assertEqual(5, self.tree._point_cloud[0][3])
        self.assertEqual(65535, self.tree._point_cloud[1][0])
        self.assertEqual(0, self.tree._point_cloud[1][1])
        self.assertEqual(65535, self.tree._point_cloud[1][2])
        self.assertEqual(6, self.tree._point_cloud[1][3])
        self.assertEqual(28925, self.tree._point_cloud[2][0])
        self.assertEqual(65535, self.tree._point_cloud[2][1])
        self.assertEqual(0, self.tree._point_cloud[2][2])
        self.assertEqual(7, self.tree._point_cloud[2][3])


if __name__ == '__main__':
    unittest.main()
