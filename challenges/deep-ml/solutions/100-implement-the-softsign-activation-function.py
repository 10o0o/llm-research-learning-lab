# deepml:problem-id=100
# Deep-ML — Implement the Softsign Activation Function
# Difficulty: easy  |  Category: Deep Learning
# Write your solution below. Use "Deep-ML: Submit Solution" to run it.


def softsign(x: float) -> float:
    """
    Implements the Softsign activation function.

    Args:
        x (float): Input value

    Returns:
        float: The Softsign of the input
    """
    # Your code here

    result = x / (1 + abs(x))
    return round(result, 4)
