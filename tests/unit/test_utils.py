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
            [1.52, 2.456, 0.516, 5],
            [5.213, 2.16, 1.566, 6],
            [3.15, 4.21, -1.25, 7]
        ])

    def test_find_bounds(self):
        from elementree.utils import find_bounds
        x_max, x_min, y_max, y_min, z_max, z_min = find_bounds(self.array)
        self.assertEqual(x_max, 5.213)
        self.assertEqual(x_min, 1.52)
        self.assertEqual(y_max, 4.21)
        self.assertEqual(y_min, 2.16)
        self.assertEqual(z_max, 1.566)
        self.assertEqual(z_min, -1.25)

    def test_scaling_factor_k_equals_16(self):
        from elementree.utils import scaling_factor
        to_max = 2**16 - 1
        to_min = 0
        x = self.array[:, 0]
        from_min = np.min(x)
        from_max = np.max(x)
        y = (scaling_factor(from_max, from_min, to_max, to_min))
        self.assertEqual(y, 17745.7352)

    def test_scale_x_to_range_k_equals_16(self):
        from elementree.utils import scale_to_range
        x = self.array[:, 0]
        scaled_16 = scale_to_range(np.float32(65535), np.float32(0.0), x)
        self.assertEqual(scaled_16[0], 0)
        self.assertEqual(scaled_16[1], 65535)
        self.assertEqual(scaled_16[2], 28925)
