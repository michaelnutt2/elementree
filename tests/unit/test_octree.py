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
        from elementree.lidar.octree import Region as rg
        self.array = np.array([
            [-5, 2, 3, 5],
            [-5, -1, 4, 5],
            [-4, 3, -1, 6],
            [-4, 5, -5, 2],
            [-3, 2, 1, 4],
            [-3, -2, 5, 5],
            [-2, 1, 4, 7],
            [-2, 3, -2, 8],
            [-1, 2, 3, 5],
            [-1, 3, 4, 8],
            [0, -1, 2, 2],
            [0, 3, -4, 5],
            [1, 2, 5, 4],
            [1, 3, -1, 4],
            [2, 4, -1, 0],
            [2, -5, 2, 0],
            [3, 0, 1, 0],
            [4, -1, 5, 1],
            [4, -2, 3, 1],
            [5, 0, 2, 2],
            [5, -3, 2, 5]
        ])
        self.region = rg.Region(x_min=-5, x_max=5, y_min=-5, y_max=5, z_min=-5, z_max=5)
        self.tree = oc.Octree(self.array, self.region)

    def test_scale_to_range(self):
        self.tree.setup(8)
        self.tree._scale_to_range()
        self.assertEqual(0, self.tree._points[0][0])
        self.assertEqual(178, self.tree._points[0][1])
        self.assertEqual(204, self.tree._points[0][2])
        self.assertEqual(0, self.tree._points[1][0])
        self.assertEqual(102, self.tree._points[1][1])
        self.assertEqual(229, self.tree._points[1][2])
        self.assertEqual(25, self.tree._points[2][0])
        self.assertEqual(204, self.tree._points[2][1])
        self.assertEqual(102, self.tree._points[2][2])
        self.assertEqual(25, self.tree._points[3][0])
        self.assertEqual(255, self.tree._points[3][1])
        self.assertEqual(0, self.tree._points[3][2])

    def test_downscale(self):
        from elementree.utils import downscale
        self.tree.setup(8)
        self.tree._scale_to_range()
        x, y, z, _ = self.array[0]
        x = downscale(x, 3)
        y = downscale(y, 3)
        z = downscale(z, 3)
        self.assertEqual(0, x)
        self.assertEqual(176, y)
        self.assertEqual(200, z)

    def test_set_children(self):
        self.tree.children[0] = self.tree
        self.assertEqual(self.tree, self.tree.children[0])

    def test_build_tree(self):
        self.tree.build_tree()

    def test_create_node_intermediate(self):
        octants = [(5, 4, 4), (2, 3, 1)]
        node = self.tree._create_node(octants, self.region)
        self.assertEqual(self.region, node.bounds)
        self.assertEqual(self.tree, node.parent)

    def test_breadth_first_traversal(self):
        self.tree.setup(8)
        self.tree.build_tree()
        occupancy = self.tree.bft()
        test_occupancy = [
            243, 40, 180, 64, 142, 194, 66, 0, 20, 0, 0, 3, 0, 18, 24, 0, 0, 0,
            0, 0, 0, 160, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.assertEqual(test_occupancy, occupancy)

    @unittest.skip("Not Implemented Yet")
    def test_depth_first_traversal(self):
        occupancy = self.tree.dft()
        test_occupancy = [
            243, 40, 0, 20, 0, 0, 180, 0, 0, 3, 0, 0, 0, 64, 18, 0, 0, 142, 24,
            0, 0, 0, 0, 0, 194, 0, 0, 0, 66, 160, 0, 0, 0
        ]
        self.assertEqual(test_occupancy, occupancy)


if __name__ == '__main__':
    unittest.main()
