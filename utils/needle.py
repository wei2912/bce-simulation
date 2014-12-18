"""
Simulation of Buffon's Needle Problem.
"""

import math

def predict_prob(length=1.0, gap_width=1.0):
    """
    Predicts the probability that the needle will hit
    one of the two parallel lines.

    length and gap_width can be scalars or arrays.
    """
    l = length
    D = gap_width

    if l <= D:
        return (
            (2 * l) /
            (math.pi * D)
        )
    else:
        return (
            (2 / math.pi) *
            (
                -math.sqrt(
                    (l / D) ** 2 - 1
                ) +
                l / D +
                math.acos(D / l)
            )
        )
