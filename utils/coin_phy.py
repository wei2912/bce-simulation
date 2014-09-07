"""
Simulation of a variation of Buffon's Coin Experiment.

The program checks if the coin will balance in addition
to touching one of the lines of the grid.
"""

import random
import math

import numpy as np
import numexpr as ne

from utils import chull, misc

def __transform_center(w, x_pos, y_pos):
    """
    Depending on the region which the coin lands,
    this function transforms the coin onto a
    Cartesian plane where the axes are the closest
    corner and returns the coordinates of the
    center of the circle.

    w = width of gap
    """

    split = w/2

    center_x = x_pos
    if x_pos > split:
        center_x = w - x_pos

    center_y = y_pos
    if y_pos > split:
        center_y = w - y_pos

    return (center_x, center_y)

def __get_pivots(r, center_x, center_y):
    """
    Get the x-intercepts and y-intercepts of
    the circle and return a list of pivots which
    the coin lies on.

    r = radius of coin
    """

    pivots = []

    sqval = r**2 - center_y**2
    if sqval > 0: # no imaginary numbers!
        sqrt = sqval**(0.5)
        pivots.append((center_x + sqrt, 0))
        pivots.append((center_x - sqrt, 0))
    elif sqval == 0: # tangent
        pivots.append((center_x, 0))

    sqval = r**2 - center_x**2
    if sqval > 0:
        sqrt = sqval**(0.5)
        pivots.append((0, center_y + sqrt))
        pivots.append((0, center_y - sqrt))
    elif sqval == 0:
        pivots.append((0, center_y))

    return pivots

def run_trials(d, w, trials):
    """
    Run the simulation a specified number of times.

    d = diameter of coin
    w = width of gap
    """

    d = misc.validate_diameter(d)
    w = misc.validate_width(w)
    trials = misc.validate_trials(trials)

    hits = 0
    for _ in xrange(trials):
        x_pos = random.uniform(0.0, w)
        y_pos = random.uniform(0.0, w)

        center = __transform_center(w, x_pos, y_pos)
        center_x = center[0]
        center_y = center[1]

        # if the center of gravity actually lies on the edge
        # the coin will balance
        if center_x == 0 or center_y == 0:
            hits += 1
            continue

        pivots = __get_pivots(d/2, center_x, center_y)

        # if it isn't touching the axes at at least 3 points
        # it will definitely not balance
        # other than in the case above where it lies on the edge
        if not len(pivots) > 2:
            continue

        # convex hull of pivots and center
        # check if the center of gravity is a point in the shape
        # if it is, the coin does not balance.
        # otherwise, the coin does.
        points = pivots + [center]
        hull_points = chull.convex_hull(points)

        # if center is in the convex hull
        # whee we have a hit
        if not center in hull_points:
            hits += 1

    return hits

def predict_prob(d, w):
    """
    For the variables passed into the simulation,
    predict the probability that the needle will hit
    at least one of the two parallel lines.

    d = diameter of coin
    w = width of gap

    d and w can be scalars or arrays.
    """

    d = misc.validate_diameter(d)
    w = misc.validate_width(w)

    pi = math.pi
    clauses = [
        "w >= d", "pi*(d/(2*w))**2",
        "w > (d/2)*sqrt(2)", "sqrt(4*(d/(2*w))**2-1)+(d/(2*w))**2*(pi-4*arccos(w/d))",
        "1"
    ]

    return ne.evaluate(
        'where(%s, %s, where(%s, %s, %s))' % tuple(clauses)
    )
