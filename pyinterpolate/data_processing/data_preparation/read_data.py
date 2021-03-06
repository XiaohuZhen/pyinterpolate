import numpy as np


def read_point_data(path, data_type):
    """Function reads data and converts it into numpy array.

    :param path: (str) path to the file,
    :param data_type: (str) data type, available types:
        - 'txt' for txt files,

    :return data_arr: (numpy array) numpy array of coordinates and their values."""
    if data_type == 'txt':
        data_arr = np.loadtxt(path, delimiter=',')
        return data_arr
    else:
        raise ValueError('Data type not supported')
