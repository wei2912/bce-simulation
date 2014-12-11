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
    clauses = [
        "l > 2*D", "(D*(pi + 2*arcsin(D/l) - 4*arcsin(2*D/l)) + 2*(sqrt(l*l - D*D) - sqrt(l*l - 4*D*D))) / (pi * D)",
        "l > D", "(2*sqrt(l*l - D*D) + D*(2*arcsin(D/l) - pi)) / (pi * D)",
        "0"
    ]

    return ne.evaluate(
        'where(%s, %s, where(%s, %s, %s))' % tuple(clauses),
        local_dict={
            'l': length,
            'D': gap_width
        },
        global_dict={
            'pi': math.pi
        }
    )
