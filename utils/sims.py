"""
This module contains all simulations used in `bce-simulation`
as well as test suites that can be runned when the module
is runned from the command line.
"""

import random
import math

import numpy as np
import numexpr as ne

from utils import chull

SQRT_2 = 2**0.5

class InvalidInput(Exception):
    """
    Exception for invalid input passed to the below classes.
    """
    pass

class CoinSim(object):
    """
    Simulation of Buffon's Coin Experiment.
    """
    def __init__(self, diameter, gap):
        if diameter <= 0:
            raise InvalidInput("diameter must not be <= 0")
        if gap <= 0:
            raise InvalidInput("gap must not be <= 0")

        self.diameter = float(diameter)
        self.radius = self.diameter/2
        self.gap = float(gap)

    def run_trials(self, trials):
        """
        Run the simulation a specified number of times.
        """

        if trials <= 0:
            raise InvalidInput("trials must not be<= 0")

        ratio = self.radius/self.gap

        x_pos = np.random.random(size=trials)
        y_pos = np.random.random(size=trials)

        clauses = [
            '1.0 - x_pos < ratio',
            'x_pos < ratio',
            '1.0 - y_pos < ratio',
            'y_pos < ratio'
        ]

        return ne.evaluate(
            'sum(where (%s, 1, 0))' %
                ' | '.join(['(%s)' % i for i in clauses])
        )

    def predict_prob(self):
        """
        For the variables passed into the simulation,
        predict the probability that the coin will hit
        the grid.
        """

        if self.diameter >= self.gap:
            return 1.0

        return (self.gap**2 - (self.gap-self.diameter)**2) / self.gap**2

    def predict_hits(self, trials):
        """
        For the variables passed into the simulation,
        predict the number of times the coin will hit
        the grid.

        Note that this function will return a float
        and not an integer.
        """
        return self.predict_prob()*trials

class NeedleSim(object):
    """
    Simulation of Buffon's Needle Experiment.
    """
    def __init__(self, length, gap):
        if length <= 0:
            raise InvalidInput("length must not be <= 0")
        if gap <= 0:
            raise InvalidInput("gap must not be <= 0")

        self.length = float(length)
        self.gap = float(gap)

    def run_trials(self, trials):
        """
        Run the simulation a specified number of times.
        """
        if trials <= 0:
            raise InvalidInput("trials must not be <= 0")

        # redefining vars in the local scope
        length = self.length
        gap = self.gap
        pi = math.pi

        angles = np.random.random(size=trials)
        y_pos = np.random.random(size=trials)

        clauses = [
            'gap - y_pos*gap < length/2 * sin(angles*pi)',
            'y_pos*gap < length/2 * sin(angles*pi)'
        ]

        return ne.evaluate(
            'sum(where (%s, 1, 0))' %
                ' | '.join(['(%s)' % i for i in clauses])
        )

    def predict_prob(self):
        """
        For the variables passed into the simulation,
        predict the probability that the needle will hit
        one of the two parallel lines.
        """

        if self.length <= self.gap:
            return (2*self.length) / (self.gap*math.pi)
        else:
            needle_ratio = self.length/self.gap
            return (
                (2/math.pi) * 
                (
                    self.length/self.gap
                    - (needle_ratio**2 - 1)**0.5
                    + math.acos(self.gap/self.length)
                )
            )

    def predict_hits(self, trials):
        """
        For the variables passed into the simulation,
        predict the number of times the needle will hit
        one of the two parallel lines.

        Note that this function will return a float
        and not an integer.
        """
        return self.predict_prob()*trials

class CoinPhysicsSim(object):
    """
    Simulation of a modified Buffon's Coin Experiment.

    The program checks if the coin will balance in addition
    to touching one of the lines of the grid.
    """
    def __init__(self, diameter, gap):
        if diameter <= 0:
            raise InvalidInput("diameter must not be <= 0")
        if gap <= 0:
            raise InvalidInput("gap must not be <= 0")

        self.diameter = float(diameter)
        self.radius = self.diameter/2
        self.gap = float(gap)

    def __transform_center(self, x_pos, y_pos):
        """
        Depending on the region which the coin lands,
        this function transforms the coin onto a
        Cartesian plane where the axes are the closest
        corner and returns the coordinates of the
        center of the circle.
        """

        split = self.gap/2

        center_x = x_pos
        if x_pos > split:
            center_x = self.gap - x_pos

        center_y = y_pos
        if y_pos > split:
            center_y = self.gap - y_pos

        return (center_x, center_y)

    def __get_pivots(self, center_x, center_y):
        """
        Get the x-intercepts and y-intercepts of
        the circle and return a list of pivots which
        the coin lies on.
        """

        pivots = []

        sqval = self.radius**2 - center_y**2
        if sqval > 0: # no imaginary numbers!
            sqrt = sqval**(0.5)
            pivots.append((center_x + sqrt, 0))
            pivots.append((center_x - sqrt, 0))
        if sqval == 0: # tangent
            pivots.append((center_x, 0))

        sqval = self.radius**2 - center_x**2
        if sqval > 0:
            sqrt = sqval**(0.5)
            pivots.append((0, center_y + sqrt))
            pivots.append((0, center_y - sqrt))
        if sqval == 0:
            pivots.append((0, center_y))

        return pivots

    def run_trials(self, trials):
        """
        Run the simulation a specified number of times.
        """
        if trials <= 0:
            raise InvalidInput("trials must not be<= 0")

        hits = 0

        for _ in xrange(trials):
            x_pos = random.uniform(0.0, self.gap)
            y_pos = random.uniform(0.0, self.gap)

            center = self.__transform_center(x_pos, y_pos)
            center_x = center[0]
            center_y = center[1]

            # if the center of gravity actually lies on the edge
            # the coin will balance
            if center_x == 0 or center_y == 0:
                hits += 1
                continue

            pivots = self.__get_pivots(center_x, center_y)

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

    def predict_prob(self):
        """
        For the variables passed into the simulation,
        predict the probability that the needle will hit
        at least one of the two parallel lines.
        """

        if self.gap >= self.diameter:
            return math.pi * (self.radius/self.gap)**2
        elif self.gap > self.radius*SQRT_2:
            return (
                (4 * (self.radius/self.gap)**2 - 1)**0.5 + (
                    (self.radius/self.gap)**2 * (
                        math.pi - 4*math.acos(
                            self.gap / self.diameter
                        )
                    )
                )
            )
        else:
            return 1.0

    def predict_hits(self, trials):
        """
        For the variables passed into the simulation,
        predict the number of times the needle will hit
        at least one of the two parallel lines.

        Note that this function will return a float
        and not an integer.
        """
        return self.predict_prob()*trials
