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


class UtilsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.array = np.array([
            [-5, 2, 3, 5],
            [-5, -1, 4, 5],
            [-4, 3, -1, 6],
            [-4, 4, -5, 2],
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
            [2, -3, 2, 0],
            [3, 0, 1, 0],
            [4, -1, 5, 1],
            [4, -2, 3, 1],
            [5, 0, 2, 2],
            [5, -3, 2, 5]
        ])

    def test_find_bounds(self):
        from elementree.utils import find_bounds
        x_max, x_min, y_max, y_min, z_max, z_min = find_bounds(self.array)
        self.assertEqual(5,  x_max)
        self.assertEqual(-5, x_min)
        self.assertEqual(4, y_max)
        self.assertEqual(-3, y_min)
        self.assertEqual(5, z_max)
        self.assertEqual(-5, z_min)

    def test_scaling_factor_k_equals_16(self):
        from elementree.utils import scaling_factor
        to_max = 2**8 - 1
        to_min = 0
        x = self.array[:, 0]
        from_min = np.min(x)
        from_max = np.max(x)
        y = (scaling_factor(from_max, from_min, to_max, to_min))
        self.assertEqual(25.5, y)

    def test_scale_x_to_range_k_equals_16(self):
        from elementree.utils import scale_to_range
        x = self.array[0]
        scaled_16, _ = scale_to_range(np.float32(65535), np.float32(0.0), x)
        self.assertEqual(0, scaled_16[0])
        self.assertEqual(45874, scaled_16[1])
        self.assertEqual(52428, scaled_16[2])

    def test_scale_x_to_range_k_equals_8(self):
        from elementree.utils import scale_to_range
        x = self.array[0]
        scaled_8, _ = scale_to_range(np.float32(255), np.float32(0.0), x)
        self.assertEqual(0, scaled_8[0])
        self.assertEqual(178, scaled_8[1])
        self.assertEqual(204, scaled_8[2])

    def test_find_center_point(self):
        from elementree.utils import find_center_point
        cp = find_center_point(0, 255)
        self.assertEqual(127, cp)
