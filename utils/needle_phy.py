"""
Simulation of Buffon's Needle Experiment.
"""

import math

import numpy as np
import numexpr as ne

from utils import misc

def run_trials(length, gap_width, trials):
    """
    Runs the simulation a specified number of times.
    """

    length = misc.validate_length(length)
    gap_width = misc.validate_width(gap_width)
    trials = misc.validate_trials(trials)

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

def predict_prob(length, gap_width):
    """
    Predicts the probability that the needle will hit
    one of the two parallel lines.

    length and gap_width can be scalars or arrays.
    """

    length = misc.validate_length(length)
    gap_width = misc.validate_width(gap_width)

    # TODO: Add in probability calculation.
    # placeholder to ensure that a full array of zeroes
    # is returned
    return ne.evaluate(
        'l * D * 0',
        local_dict={
            'l': length,
            'D': gap_width
        }
    )
