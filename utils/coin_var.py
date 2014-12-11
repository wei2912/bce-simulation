"""
Simulation of a variation of Buffon's Coin Experiment.

The program checks if the coin will balance in addition
to touching one of the lines of the grid.
"""

import random
import math

from scipy.spatial import ConvexHull 

DEFAULT_TRIALS = 100000

def __transform_center(gap_width, x, y):
    """
    Depending on the region which the coin lands,
    this function transforms the coin onto a
    Cartesian plane where the axes are the closest
    corner and returns the coordinates of the
    center of the circle.
    """

    split = gap_width/2

    if x > split:
        x = gap_width - x
    if y > split:
        y = gap_width - y

    return (x, y)

def __get_pivots(diameter, x, y):
    """
    Get the x-intercepts and y-intercepts of
    the circle and return a list of pivots which
    the coin lies on.
    """

    pivots = []
    radius = diameter / 2

    sqval = radius**2 - y**2
    if sqval > 0: # no imaginary numbers!
        sqrt = sqval**(0.5)
        pivots.append([x + sqrt, 0])
        pivots.append([x - sqrt, 0])
    elif sqval == 0: # tangent
        pivots.append([x, 0])

    sqval = radius**2 - x**2
    if sqval > 0:
        sqrt = sqval**(0.5)
        pivots.append([0, y + sqrt])
        pivots.append([0, y - sqrt])
    elif sqval == 0:
        pivots.append([0, y])

    return pivots

def run_trials(diameter=1.0, gap_width=1.0, trials=DEFAULT_TRIALS):
    """
    Run the simulation a specified number of times.
    """
    hits = 0
    for _ in xrange(trials):
        x = random.uniform(0.0, gap_width)
        y = random.uniform(0.0, gap_width)

        x, y = __transform_center(gap_width, x, y)

        # if the center of gravity actually lies on the edge
        # the coin will balance
        if x == 0 or y == 0:
            hits += 1
            continue

        pivots = __get_pivots(diameter, x, y)

        # if it isn't touching the axes at at least 3 points
        # it will definitely not balance
        # other than in the case above where it lies on the edge
        if not len(pivots) > 2:
            continue

        # convex hull of pivots and center
        # check if the center of gravity is a point in the shape
        # if it is, the coin does not balance.
        # otherwise, the coin does.
        pivots.append([x, y])
        hull = ConvexHull(pivots)

        # if center is in the convex hull
        # whee we have a hit
        center_index = len(pivots) - 1
        if not center_index in hull.vertices:
            hits += 1

    return hits

def predict_prob(diameter=1.0, gap_width=1.0):
    """
    For the variables passed into the simulation,
    predict the probability that the needle will hit
    at least one of the two parallel lines.

    diameter and gap_width can be scalars or arrays.
    """
    d = diameter
    D = gap_width

    if D >= d:
        return (
            math.pi *
            (d / (2 * D)) ** 2
        )
    elif D > (d / 2) * math.sqrt(2):
        return (
            math.sqrt(
                4 *
                (d / (2 * D)) ** 2
                - 1
            ) +
            (d / (2 * D)) ** 2 *
            (math.pi - 4 * math.acos(D / d))
        )
