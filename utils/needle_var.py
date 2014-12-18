"""
Simulation of a variation of Buffon's Needle Problem.
"""

import math

import numpy as np
import numexpr as ne

DEFAULT_TRIALS=10000000

def run_trials(length=1.0, gap_width=1.0, trials=DEFAULT_TRIALS):
    """
    Runs the simulation a specified number of times.
    """
    angles = np.random.random(size=trials)
    y = np.random.random(size=trials)

    clauses = [
        'D - y*D < l/2 * sin(x * pi)',
        'y*D < l/2 * sin(x * pi)'
    ]

    return ne.evaluate(
        'sum(where (%s, 1, 0))' %
            ' & '.join(['(%s)' % i for i in clauses]),
        local_dict={
            'l': length,
            'D': gap_width,
            'x': angles,
            'y': y
        },
        global_dict={
            'pi': math.pi
        }
    )

def predict_prob(length=1.0, gap_width=1.0):
    """
    Predicts the probability that the needle will hit
    one of the two parallel lines.

    length and gap_width can be scalars or arrays.
    """
    L = length
    D = gap_width

    if L > 2 * D:
        return (
            (D * (
                math.pi + 2 * math.asin(D / L) -
                4 * math.asin(2 * D / L)
            ) +
            2 * (
                math.sqrt(L * L - D * D) -
                math.sqrt(L * L - 4 * D * D)
            )) /
            (math.pi * D)
        )
    elif L > D:
        return (
            (
                2 * math.sqrt(L * L - D * D) +
                D * (2 * math.asin(D / L) - math.pi)
            ) / (math.pi * D)
        )
    else:
        return float('NaN')
