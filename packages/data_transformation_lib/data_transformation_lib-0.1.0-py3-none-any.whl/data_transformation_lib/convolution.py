from typing import Union
import numpy as np

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Perform 2D cross-correlation on the input matrix with the given kernel.

    :param input_matrix: 2D Numpy array of real numbers.
    :param kernel: 2D Numpy array of real numbers.
    :param stride: Step size.
    :return: 2D Numpy array of real numbers.
    :raises ValueError: If parameters are invalid.
    """
    if stride <= 0:
        raise ValueError("Stride must be a positive integer")
    if input_matrix.ndim != 2 or kernel.ndim != 2:
        raise ValueError("Input and kernel must be 2D arrays")

    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    output = np.zeros((output_height, output_width))

    for i in range(0, output_height):
        for j in range(0, output_width):
            region = input_matrix[i*stride:i*stride+kernel_height, j*stride:j*stride+kernel_width]
            output[i, j] = np.sum(region * kernel)

    return output
