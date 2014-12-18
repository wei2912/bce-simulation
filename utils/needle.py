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
    L = length
    D = gap_width

    if L <= D:
        return (
            (2 * L) /
            (math.pi * D)
        )
    else:
        return (
            (2 / math.pi) *
            (
                -math.sqrt(
                    (L / D) ** 2 - 1
                ) +
                L / D +
                math.acos(D / L)
            )
        )
