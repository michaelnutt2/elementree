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


def find_bounds(point_cloud: np.ndarray) -> (float, float, float, float, float, float):
    """
    Accepts a point cloud as a ndarray and finds the max x, y, z values
    to format as bounds for the point cloud
    :param point_cloud:
    :return: Tuple of max/min bounds (x_max, x_min, y_max, y_min, z_max, z_min)
    """
    x_max, y_max, z_max, _ = np.max(point_cloud, axis=0)
    x_min, y_min, z_min, _ = np.min(point_cloud, axis=0)
    return x_max, x_min, y_max, y_min, z_max, z_min


def scale_to_range(
        to_max: np.float32,
        to_min: np.float32,
        array: np.ndarray) -> np.ndarray:
    """
    TODO
    :param to_max:
    :param to_min:
    :param array:
    :return:
    """
    from_min = np.min(array)
    from_max = np.max(array)

    scale_factor = scaling_factor(
        from_min=from_min,
        from_max=from_max,
        to_max=to_max,
        to_min=to_min
    )
    for i in range(len(array)):
        array[i] = int(scale_factor * (array[i] - from_min))
    return array


def scaling_factor(
        from_max: np.float32,
        from_min: np.float32,
        to_max: np.float32,
        to_min: np.float32
) -> np.float32:
    """
    Finds the scaling factor for moving values from one range to another
    :param from_max: previous max value
    :param from_min: previous min value
    :param to_max: new max value
    :param to_min: new min value
    :return:
    """
    return round((to_max - to_min) / ((from_max - from_min) + to_min), 4)
