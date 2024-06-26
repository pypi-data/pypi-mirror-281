from typing import List, Union
import numpy as np

def window1d(input_array: Union[List[float], np.ndarray], size: int, shift: int = 1, stride: int = 1) -> List[Union[List[float], np.ndarray]]:
    """
    Generate time series windows.

    :param input_array: A list or 1D Numpy array of real numbers.
    :param size: Size (length) of the window.
    :param shift: Step size between different windows.
    :param stride: Step size within each window.
    :return: List of lists or 1D Numpy arrays of real numbers.
    :raises ValueError: If parameters are invalid.
    """
    if size <= 0 or shift <= 0 or stride <= 0:
        raise ValueError("Size, shift, and stride must be positive integers")
    if isinstance(input_array, list):
        input_array = np.array(input_array)
    if input_array.ndim != 1:
        raise ValueError("Input must be a 1D array or list")

    n = len(input_array)
    windows = []

    for i in range(0, n - size + 1, shift):
        window = input_array[i:i + size:stride]
        windows.append(window.tolist())

    return windows
