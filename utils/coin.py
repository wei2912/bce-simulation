"""
Simulation of Buffon's Coin Experiment.
"""

import random
import math

import numpy as np
import numexpr as ne

from utils import misc

def run_trials(d, w, trials):
    """
    Runs the simulation a specified number of times.

    d = diameter of coin
    w = width of gap
    """

    d = misc.validate_diameter(d)
    w = misc.validate_width(w)
    trials = misc.validate_trials(trials)

    x_pos = np.random.random(size=trials)
    y_pos = np.random.random(size=trials)

    clauses = [
	'1.0 - x_pos < d/(2*w)',
	'x_pos < d/(2*w)',
	'1.0 - y_pos < d/(2*w)',
	'y_pos < d/(2*w)'
    ]

    return ne.evaluate(
	'sum(where (%s, 1, 0))' %
	    ' | '.join(['(%s)' % i for i in clauses])
    )

def predict_prob(d, w):
    """
    Predicts the probability that the coin will hit
    the grid.

    d = diameter of coin
    w = width of gap

    d and w can be scalars or arrays.
    """

    d = misc.validate_diameter(d)
    w = misc.validate_width(w)

    clauses = [
	"d >= w", "1",
	"1-((w-d)**2)/(w**2)"
    ]

    return ne.evaluate(
	'where(%s, %s, %s)' % tuple(clauses)
    )