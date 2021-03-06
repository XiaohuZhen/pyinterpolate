import numpy as np


def select_values_in_range(data, lag, step_size):
    """Function selects set of values which are greater than (lag - step size) and
    lesser than (lag + step size)."""

    step_size = step_size / 2

    # Check if numpy array is given
    if type(data) != np.ndarray:
        data = np.array(data)

    greater_than = lag - step_size
    less_equal_than = lag + step_size

    # Check conditions
    condition_matrix = np.logical_and(
            np.greater(data, greater_than),
            np.less_equal(data, less_equal_than))

    # Find positions
    position_matrix = np.where(condition_matrix)
    return position_matrix
