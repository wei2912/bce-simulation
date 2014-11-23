"""
Simulation of Buffon's Needle Experiment.
"""

import math

import numexpr as ne

def predict_prob(length, gap_width):
    """
    Predicts the probability that the needle will hit
    one of the two parallel lines.

    length and gap_width can be scalars or arrays.
    """
    clauses = [
        "l <= D", "(2 * l) / (pi * D)",
        "(2 / pi) * (-sqrt((l / D)**2 - 1) + l/D + arccos(D / l))",
    ]

    return ne.evaluate(
        'where(%s, %s, %s)' % tuple(clauses),
        local_dict={
            'l': length,
            'D': gap_width
        },
        global_dict={
            'pi': math.pi
        }
    )
