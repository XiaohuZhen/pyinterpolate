import numpy as np
from tqdm import tqdm
from scipy.spatial.distance import cdist


def calc_point_to_point_distance(points_a, points_b=None):
    """Function calculates distances between all points in the given array.

    INPUT:
    :param points_a: (numpy array) or Python list of lists of coordinates,
    :param points_b: default (None) if None then distances between all points grouped in matrix points_a are
        calculated. If points_b is provided it must be the same type as point_b.

    OUTPUT:
    :return distances: numpy array of distances between all coordinates."""

    if points_b is None:
        distances = cdist(points_a, points_a, 'euclidean')
    else:
        distances = cdist(points_a, points_b, 'euclidean')
    return distances


def _calculate_block_to_block_distance(area_block_1, area_block_2):
    """
        Function calculates distance between two blocks based on how they are divided (into a population blocks)
        :param area_block_1: set of coordinates of each population block in the form:
        [
            [coordinate x 0, coordinate y 0, value 0],
            [...],
            [coordinate x n, coordinate y n, value n]
        ]
        :param area_block_2: the same set of coordinates as area_block_1
        :return distance: function return weighted block to block distance

        Equation: Dist(v_a, v_b) = 1 / (SUM_to(Pa), SUM_to(Pb) n(u_s) * n(u_si)) *
        * SUM_to(Pa), SUM_to(Pb) n(u_s) * n(u_si) ||u_s - u_si||
        where:
        Pa and Pb: number of points u_s and u_si used to discretize the two units v_a and v_b
        n(u_s) - population size in the cell u_s
    """

    if type(area_block_1) is list:
        area_block_1 = np.array(area_block_1)
    if type(area_block_2) is list:
        area_block_2 = np.array(area_block_2)

    a_shape = area_block_1.shape[0]
    b_shape = area_block_2.shape[0]
    ax = area_block_1[:, 0].reshape(1, a_shape)
    bx = area_block_2[:, 0].reshape(b_shape, 1)
    dx = ax - bx
    ay = area_block_1[:, 1].reshape(1, a_shape)
    by = area_block_2[:, 1].reshape(b_shape, 1)
    dy = ay - by
    aval = area_block_1[:, -1].reshape(1, a_shape)
    bval = area_block_2[:, -1].reshape(b_shape, 1)
    w = aval * bval

    dist = np.sqrt(dx ** 2 + dy ** 2)

    wdist = dist * w
    distances_sum = np.sum(wdist) / np.sum(w)
    return distances_sum


def calc_block_to_block_distance(areas):
    """Function calculates distances between blocks based on the population points within the block.

    INPUT:
    :param areas: numpy array or Python list of lists of areal id's and coordinates per each id:
    [
        [area_id_1,
        [[coor_x1, coor_y1, val1],
          [coor_x2, coor_y2, val2],
          [coor_x999, coor_y999, val999]]
        ],

        [next area...]
    ]

    OUTPUT:
    :return areal_distances: tuple with matrix with areal distances (0) and ids of each row of distances (1):

    (
        [[dist(id0:id0), dist(id0:id1), ..., dist(id0:id999)],
        ...,
        [dist(id999:id0), dist(id999:id1), ..., dist(id999:id999)]],

        [id0, id1, ..., id999]
    )

    """

    dist_array = np.zeros(shape=(len(areas), len(areas)))
    idx = 0
    id_row = []

    for area in areas:
        other_idx = idx
        for other_area in areas[idx:]:
            if idx == other_idx:
                val = 0
            else:
                try:
                    a1 = area[1]
                    a2 = other_area[1]
                except IndexError:
                    a1 = area[0][1]
                    a2 = other_area[0][1]
                val = _calculate_block_to_block_distance(a1, a2)
            dist_array[other_idx, idx] = val
            dist_array[idx:, other_idx] = val
            other_idx = other_idx + 1
        id_row.append(area[0])
        idx = idx + 1
    return dist_array, id_row
