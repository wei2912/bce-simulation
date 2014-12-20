"""
Simulation of a variation of Buffon's Coin Experiment.

The program checks if the coin will balance in addition
to touching one of the lines of the grid.
"""

import random
import math

DEFAULT_TRIALS = 100000

def __convex__hull(points):
    """Computes the convex hull of a set of 2D points.
 
    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.

    Taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain
    """
 
    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))
 
    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points
 
    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
 
    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
 
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
 
    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]

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
        pivots.append((x + sqrt, 0))
        pivots.append((x - sqrt, 0))
    elif sqval == 0: # tangent
        pivots.append((x, 0))

    sqval = radius**2 - x**2
    if sqval > 0:
        sqrt = sqval**(0.5)
        pivots.append((0, y + sqrt))
        pivots.append((0, y - sqrt))
    elif sqval == 0:
        pivots.append((0, y))

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

        # if it is a tangent to either of the axes
        # it won't balance
        if len(pivots) < 4:
            continue

        # convex hull of pivots and center
        # check if the center of gravity is a point in the shape
        # if it is, the coin does not balance.
        # otherwise, the coin does.
        pivots.append((x, y))
        hull = __convex__hull(pivots)

        # if center is in the convex hull
        # whee we have a hit
        if not (x, y) in hull:
            hits += 1

    return hits

def predict_prob(diameter=1.0, gap_width=1.0):
    """
    For the variables passed into the simulation,
    predict the probability that the needle will hit
    at least one of the two parallel lines.

    diameter and gap_width can be scalars or arrays.
    """
    R = diameter / 2
    D = gap_width

    if D >= 2 * R:
        return (
            math.pi *
            (R / D) ** 2
        )
    elif D > R * math.sqrt(2):
        return (
            math.sqrt(
                4 *
                (R / D) ** 2
                - 1
            ) +
            (R / D) ** 2 *
            (math.pi - 4 * math.acos(D / (2*R)))
        )
    else:
        return 1
