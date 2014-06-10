"""
This module contains all simulations used in `bce-simulation`.
"""

import random
import math

class InvalidInput(Exception):
    """
    Exception for invalid input passed to the below classes.
    """
    pass

class CoinSim(object):
    """
    Simulation of Buffon's Coin Experiment.
    """
    def __init__(self, radius, gap_x, gap_y):
        if radius <= 0:
            raise InvalidInput("radius must not be <= 0")
        if gap_x <= 0:
            raise InvalidInput("gap_x must not be <= 0")
        if gap_y <= 0:
            raise InvalidInput("gap_y must not be <= 0")

        self.radius = float(radius)
        self.gap_x = float(gap_x)
        self.gap_y = float(gap_y)

    def run_trials(self, trials):
        """
        Run the simulation a specified number of times.
        """
        if trials <= 0:
            raise InvalidInput("trials must not be<= 0")

        hits = 0

        for _ in xrange(trials):
            x_pos = random.uniform(0.0, self.gap_x)
            y_pos = random.uniform(0.0, self.gap_y)

            if (self.gap_x - x_pos < self.radius or x_pos < self.radius or
                self.gap_y - y_pos < self.radius or y_pos < self.radius):
                hits += 1

        return hits

    def predict_prob(self):
        """
        For the variables passed into the simulation,
        predict the probability that the coin will hit
        the grid.
        """
        diameter = self.radius*2

        # will always touch
        if diameter >= self.gap_x or diameter >= self.gap_y:
            return 1.0

        # area of region which coin would be on if it hit
        region = (self.gap_x * self.gap_y -
            (self.gap_x-diameter) * (self.gap_y-diameter))
        return region/(self.gap_x * self.gap_y)

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

        hits = 0

        for _ in xrange(trials):
            x_pos = random.uniform(0.0, self.gap)

            angle = random.uniform(0.0, math.pi)
            opp = self.length/2 * math.sin(angle)

            if self.gap - x_pos < opp or x_pos < opp:
                hits += 1

        return hits

class NeedleAngleSim(object):
    """
    Simulation of Buffon's Needle Experiment, with a fixed angle.
    """
    def __init__(self, length, gap, angle):
        if length <= 0:
            raise InvalidInput("length must not be <= 0")
        if gap <= 0:
            raise InvalidInput("gap must not be <= 0")
        if angle <= 0 or angle >= math.pi:
            raise InvalidInput("angle must not be <= 0 or >= math.pi")

        self.length = float(length)
        self.gap = float(gap)
        self.angle = float(angle)

    def run_trials(self, trials):
        """
        Run the simulation a specified number of times.
        """
        if trials <= 0:
            raise InvalidInput("trials must not be <= 0")

        # since the angle is specified, precompute the opposite
        opp = self.length/2 * math.sin(self.angle)

        hits = 0

        for _ in xrange(trials):
            x_pos = random.uniform(0.0, self.gap)

            if self.gap - x_pos < opp or x_pos < opp:
                hits += 1

        return hits

    def predict_prob(self):
        """
        For the variables passed into the simulation,
        predict the probability that the needle will hit
        at least one of the two parallel lines.
        """
        opp = self.length/2 * math.sin(self.angle)

        # will always touch
        if opp*2 >= self.gap:
            return 1.0

        # area of region which needle would be on if it hit
        return opp*2/self.gap

    def predict_hits(self, trials):
        """
        For the variables passed into the simulation,
        predict the number of times the needle will hit
        at least one of the two parallel lines.

        Note that this function will return a float
        and not an integer.
        """
        return self.predict_prob()*trials
