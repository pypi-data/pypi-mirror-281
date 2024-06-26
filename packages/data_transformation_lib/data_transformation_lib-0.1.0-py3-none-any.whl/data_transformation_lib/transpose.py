from typing import List

def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Transpose a 2D matrix.

    :param input_matrix: A list of lists of real numbers.
    :return: Transposed matrix.
    :raises ValueError: If input_matrix is not a non-empty 2D list.
    """
    if not input_matrix or not all(isinstance(row, list) and row for row in input_matrix):
        raise ValueError("Input must be a non-empty 2D list")

    return [list(row) for row in zip(*input_matrix)]
