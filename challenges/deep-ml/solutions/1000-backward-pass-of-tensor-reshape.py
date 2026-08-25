# deepml:problem-id=1000
# Deep-ML — Backward Pass of Tensor Reshape
# Difficulty: easy  |  Category: Deep Learning
# Write your solution below. Use "Deep-ML: Submit Solution" to run it.

import numpy as np


def reshape_backward(grad_output: np.ndarray, original_shape: tuple) -> np.ndarray:
    """
    Backward pass for a reshape/view operation.

    Args:
        grad_output: numpy array, gradient w.r.t. the reshape output.
        original_shape: tuple of ints, shape of the input to the forward reshape.

    Returns:
        numpy array of shape `original_shape` containing the gradient
        w.r.t. the input tensor.
    """

    if grad_output.size != np.prod(original_shape):
        raise ValueError("grad_output의 원소 수와 original_shape의 원소 수가 다릅니다.")

    return np.reshape(grad_output, original_shape)
