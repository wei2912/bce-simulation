"""
Simulation of a variation of Buffon's Coin Experiment.

The program checks if the coin will balance in addition
to touching one of the lines of the grid.
"""

import random
import math

import numexpr as ne

from utils import chull, misc

def __transform_center(gap_width, x, y):
    """
    Depending on the region which the coin lands,
    this function transforms the coin onto a
    Cartesian plane where the axes are the closest
    corner and returns the coordinates of the
    center of the circle.
    """

    split = gap_width/2

    center_x = x
    if x > split:
        center_x = gap_width - x

    center_y = y
    if y > split:
        center_y = gap_width - y

    return (center_x, center_y)

def __get_pivots(diameter, center_x, center_y):
    """
    Get the x-intercepts and y-intercepts of
    the circle and return a list of pivots which
    the coin lies on.
    """

    pivots = []
    radius = diameter / 2

    sqval = radius**2 - center_y**2
    if sqval > 0: # no imaginary numbers!
        sqrt = sqval**(0.5)
        pivots.append((center_x + sqrt, 0))
        pivots.append((center_x - sqrt, 0))
    elif sqval == 0: # tangent
        pivots.append((center_x, 0))

    sqval = radius**2 - center_x**2
    if sqval > 0:
        sqrt = sqval**(0.5)
        pivots.append((0, center_y + sqrt))
        pivots.append((0, center_y - sqrt))
    elif sqval == 0:
        pivots.append((0, center_y))

    return pivots

def run_trials(diameter, gap_width, trials):
    """
    Run the simulation a specified number of times.
    """

    diameter = misc.validate_diameter(diameter)
    gap_width = misc.validate_width(gap_width)
    trials = misc.validate_trials(trials)

    hits = 0
    for _ in xrange(trials):
        x = random.uniform(0.0, gap_width)
        y = random.uniform(0.0, gap_width)

        center_x, center_y = __transform_center(gap_width, x, y)

        # if the center of gravity actually lies on the edge
        # the coin will balance
        if center_x == 0 or center_y == 0:
            hits += 1
            continue

        pivots = __get_pivots(diameter, center_x, center_y)

        # if it isn't touching the axes at at least 3 points
        # it will definitely not balance
        # other than in the case above where it lies on the edge
        if not len(pivots) > 2:
            continue

        # convex hull of pivots and center
        # check if the center of gravity is a point in the shape
        # if it is, the coin does not balance.
        # otherwise, the coin does.
        points = pivots + [(center_x, center_y)]
        hull_points = chull.convex_hull(points)

        # if center is in the convex hull
        # whee we have a hit
        if not (center_x, center_y) in hull_points:
            hits += 1

    return hits

def predict_prob(diameter, gap_width):
    """
    For the variables passed into the simulation,
    predict the probability that the needle will hit
    at least one of the two parallel lines.

    diameter and gap_width can be scalars or arrays.
    """

    diameter = misc.validate_diameter(diameter)
    gap_width = misc.validate_width(gap_width)

    clauses = [
        "D >= d", "pi * (d / (2 * D))**2",
        "D > (d/2) * sqrt(2)", "sqrt(4 * (d / (2 * D))**2 - 1) + (d / (2 * D))**2 * (pi - 4*arccos(D / d))",
        "1"
    ]

    return ne.evaluate(
        'where(%s, %s, where(%s, %s, %s))' % tuple(clauses),
        local_dict={
            'd': diameter,
            'D': gap_width
        },
        global_dict={
            'pi': math.pi
        }
    )
