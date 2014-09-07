"""
Simulation of Buffon's Needle Experiment.
"""

import random
import math

import numpy as np
import numexpr as ne

from utils import misc

def run_trials(l, w, trials):
    """
    Runs the simulation a specified number of times.

    l = length of needle
    w = width of gap
    """

    l = misc.validate_length(l)
    w = misc.validate_width(w)
    trials = misc.validate_trials(trials)

    pi = math.pi
    angles = np.random.random(size=trials)
    y_pos = np.random.random(size=trials)

    clauses = [
        'w - y_pos*w < l/2 * sin(angles*pi)',
        'y_pos*w < l/2 * sin(angles*pi)'
    ]

    return ne.evaluate(
        'sum(where (%s, 1, 0))' %
            ' | '.join(['(%s)' % i for i in clauses])
    )

def predict_prob(l, w):
    """
    Predicts the probability that the needle will hit
    one of the two parallel lines.

    l = length of needle
    w = width of gap

    l and w can be scalars or arrays.
    """

    l = misc.validate_length(l)
    w = misc.validate_width(w)

    pi = math.pi
    clauses = [
        "l <= w", "(2*l)/(pi*w)",
        "(2/pi)*(-sqrt((l/w)**2-1)+l/w+arccos(w/l))",
    ]

    return ne.evaluate(
        'where(%s, %s, %s)' % tuple(clauses)
    )
