"""
Simulation of Buffon's Coin Experiment.
"""

import numpy as np
import numexpr as ne

from utils import misc

def run_trials(diameter, width, trials=1000000):
    """
    Runs the simulation a specified number of times.
    """
    diameter = misc.validate_diameter(diameter)
    width = misc.validate_width(width)
    trials = misc.validate_trials(trials)

    x = np.random.random(size=trials)
    y = np.random.random(size=trials)

    clauses = [
        '1.0 - x < d / (2 * D)',
        'x < d / (2 * D)',
        '1.0 - y < d / (2 * D)',
        'y < d / (2 * D)'
    ]

    return ne.evaluate(
        'sum(where (%s, 1, 0))' %
            ' | '.join(['(%s)' % i for i in clauses]),
        local_dict={
            'd': diameter,
            'D': width,
            'x': x,
            'y': y
        }
    )

def predict_prob(diameter, width):
    """
    Predicts the probability that the coin will hit
    the grid.

    diameter and width can be scalars or arrays.
    """

    diameter = misc.validate_diameter(diameter)
    width = misc.validate_width(gap_width)

    clauses = [
        "d >= D", "1",
        "1 - ((D - d) ** 2) / (D ** 2)"
    ]

    return ne.evaluate(
        'where(%s, %s, %s)' % tuple(clauses),
        local_dict={
            'd': diameter,
            'D': width
        }
    )
