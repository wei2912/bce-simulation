"""
This module contains all simulations used in `bce-simulation`
as well as test suites that can be runned when the module
is runned from the command line.
"""

import random
import math
import unittest
from pyhull import convex_hull

TRIALS = 10000 # number of trials to run per test case
NUM_TESTS = 10 # number of tests to run per test case
MAX_STAT = 3.841 # p < 0.05 for a df of 1

def _non_zero_rand():
    """
    Returns a random float x where
    0.0 < x <= 1.0
    """
    return 1.0 - random.random()

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

        # if it always touches
        # cap the probability at 1.0
        if diameter >= self.gap_x or diameter >= self.gap_y:
            return 1.0

        area = self.gap_x * self.gap_y
        return ((area - (self.gap_x-diameter) * (self.gap_y-diameter)) /
            area)

    def predict_hits(self, trials):
        """
        For the variables passed into the simulation,
        predict the number of times the coin will hit
        the grid.

        Note that this function will return a float
        and not an integer.
        """
        return self.predict_prob()*trials

class TestCoinSim(unittest.TestCase):
    """
    Test suite for CoinSim.
    """

    def test_bad_input(self):
        """
        test_bad_input
        ===

        If bad input is passed to the simulation,
        the simulation should raise an exception.
        """

        self.assertRaises(sims.InvalidInput, sims.CoinSim, 0, 1, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinSim, 1, 0, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinSim, 1, 1, 0)

        self.assertRaises(sims.InvalidInput, sims.CoinSim, -1, 1, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinSim, 1, -1, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinSim, 1, 1, -1)

        sim = sims.CoinSim(1, 1, 1)
        self.assertRaises(sims.InvalidInput, sim.run_trials, 0)
        self.assertRaises(sims.InvalidInput, sim.run_trials, -1)

    def test_always_hit(self):
        """
        test_always_hit
        ===
        If the diameter of the coin >= gap_x or
        the diameter of the coin >= gap_y,
        the coin should always hit the grid.
        """

        for _ in range(NUM_TESTS):
            radius = 1.0 - _non_zero_rand()
            diameter = radius*2
            more_gap = diameter + _non_zero_rand()
            less_gap = diameter - _non_zero_rand()*diameter

            pairs = [
                (diameter, more_gap),
                (more_gap, diameter),
                (diameter, less_gap),
                (less_gap, diameter),
                (less_gap, more_gap),
                (more_gap, less_gap),
                (less_gap, less_gap)
            ]

            for pair in pairs:
                sim = sims.CoinSim(radius, pair[0], pair[1])
                hits = sim.run_trials(TRIALS)
                self.assertEquals(hits, TRIALS, "coin does not always hit")
                self.assertEquals(sim.predict_prob(), 1.0, "predicted probability != 1.0")

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap_x = _non_zero_rand()
            gap_y = _non_zero_rand()
            radius = _non_zero_rand()/2

            sim = sims.CoinSim(radius, gap_x, gap_y)

            hits = sim.run_trials(TRIALS)
            pred_hits = sim.predict_hits(TRIALS)

            # if they're equal
            # skip the calculation
            if hits == pred_hits:
                continue

            stats = [
                (hits-pred_hits)**2/pred_hits,
                (pred_hits-hits)**2/(TRIALS-pred_hits)
            ]
            chi2 = sum(stats)
            self.assertTrue(
                chi2 < MAX_STAT,
                "chi-square = %f >= %f" % (chi2, MAX_STAT)
            )


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

class TestNeedleSim(unittest.TestCase):
    """
    Test suite for NeedleSim.
    """

    def test_bad_input(self):
        """
        test_bad_input
        ===

        If bad input is passed to the simulation,
        the simulation should raise an exception.
        """

        self.assertRaises(sims.InvalidInput, sims.NeedleSim, 0, 1)
        self.assertRaises(sims.InvalidInput, sims.NeedleSim, 1, 0)

        self.assertRaises(sims.InvalidInput, sims.NeedleSim, -1, 1)
        self.assertRaises(sims.InvalidInput, sims.NeedleSim, 1, -1)

        sim = sims.NeedleSim(1, 1)
        self.assertRaises(sims.InvalidInput, sim.run_trials, 0)
        self.assertRaises(sims.InvalidInput, sim.run_trials, -1)


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

        # if it always touches
        # cap the probability at 1.0
        if opp*2 >= self.gap:
            return 1.0

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

class TestNeedleAngleSim(unittest.TestCase):
    """
    Test suite for NeedleAngleSim.
    """

    def test_bad_input(self):
        """
        test_bad_input
        ===

        If bad input is passed to the simulation,
        the simulation should raise an exception.
        """

        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, 0, 1, 0.1)
        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, 1, 0, 0.1)

        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, -1, 1, 0.1)
        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, 1, -1, 0.1)

        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, 1, 1, math.pi)
        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, 1, 1, 3.15)
        self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, 1, 1, -0.1)

        sim = sims.NeedleAngleSim(1, 1, 0.1)
        self.assertRaises(sims.InvalidInput, sim.run_trials, 0)
        self.assertRaises(sims.InvalidInput, sim.run_trials, -1)

    def test_always_hit(self):
        """
        test_always_hit
        ===

        If the opposite of the needle >= gap,
        the needle should always hit at least
        one of the two parallel lines.
        """

        for _ in range(NUM_TESTS):
            # normally we would consider 0 radians
            # however in this case 0 radians would mean it
            # is impossible for the needle to have a non-zero opposite
            # and hence will not always hit.
            angle = _non_zero_rand()*math.pi

            opp = _non_zero_rand()
            length = opp/math.sin(angle)

            less_gap = opp - _non_zero_rand()*opp

            sim = sims.NeedleAngleSim(length, less_gap, angle)
            hits = sim.run_trials(TRIALS)
            self.assertEquals(hits, TRIALS, "needle does not always hit")
            self.assertEquals(sim.predict_prob(), 1.0, "predicted probability != 1.0")

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            angle = random.uniform(0.0, math.pi)
            length = _non_zero_rand()
            gap = _non_zero_rand()

            sim = sims.NeedleAngleSim(length, gap, angle)

            hits = sim.run_trials(TRIALS)
            pred_hits = sim.predict_hits(TRIALS)

            # if they're equal
            # skip the calculation
            if hits == pred_hits:
                continue

            stats = [
                (hits-pred_hits)**2/pred_hits,
                (pred_hits-hits)**2/(TRIALS-pred_hits)
            ]
            chi2 = sum(stats)
            self.assertTrue(
                chi2 < MAX_STAT,
                "chi-square = %f >= %f" % (chi2, MAX_STAT)
            )


class CoinPhysicsSim(object):
    """
    Simulation of a modified Buffon's Coin Experiment.

    The program checks if the coin will balance in addition
    to touching one of the lines of the grid.
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

    def __transform_center(self, x_pos, y_pos):
        """
        Depending on the region which the coin lands,
        this function transforms the coin onto a
        Cartesian plane where the axes are the closest
        corner and returns the coordinates of the
        center of the circle.
        """

        x_split = self.gap_x/2
        y_split = self.gap_y/2

        center_x = x_pos
        if x_pos > x_split:
            center_x = self.gap_x-x_pos

        center_y = y_pos
        if y_pos > y_split:
            center_y = self.gap_y-y_pos

        return (center_x, center_y)

    def __get_pivots(self, center_x, center_y):
        """
        Get the x-intercepts and y-intercepts of
        the circle and return a list of pivots which
        the coin lies on.
        """

        pivots = []

        if self.radius**2 - center_y**2 > 0: # no imaginary numbers!
            sqrt = (self.radius**2 - center_y**2)**(0.5)
            pivots.append((center_x + sqrt, 0))
            pivots.append((center_x - sqrt, 0))

        if self.radius**2 - center_x**2 > 0:
            sqrt = (self.radius**2 - center_x**2)**(0.5)
            pivots.append((0, center_y + sqrt))
            pivots.append((0, center_y - sqrt))

        return pivots

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
            hull = convex_hull.ConvexHull(points)
            found = True
            for line in hull.vertices:
                # the center is always the last point
                # if the last point is found in the vertice
                # it's not a hit.
                if len(points)-1 in line:
                    found = False
                    break

            # if the center isn't part of the vertices
            # it's a hit
            if found:
                hits += 1

        return hits

    def predict_prob(self):
        """
        For the variables passed into the simulation,
        predict the probability that the needle will hit
        at least one of the two parallel lines.
        """

        # area of coin / area of rectangle
        area_coin = math.pi * self.radius**2
        area = self.gap_x * self.gap_y
        if area_coin > area:
            return 1.0
        return area_coin / area

    def predict_hits(self, trials):
        """
        For the variables passed into the simulation,
        predict the number of times the needle will hit
        at least one of the two parallel lines.

        Note that this function will return a float
        and not an integer.
        """
        return self.predict_prob()*trials

class TestCoinPhysicsSim(unittest.TestCase):
    """
    Test suite for CoinPhysicsSim.
    """

    def test_bad_input(self):
        """
        test_bad_input
        ===

        If bad input is passed to the simulation,
        the simulation should raise an exception.
        """

        self.assertRaises(sims.InvalidInput, sims.CoinPhysicsSim, 0, 1, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinPhysicsSim, 1, 0, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinPhysicsSim, 1, 1, 0)

        self.assertRaises(sims.InvalidInput, sims.CoinPhysicsSim, -1, 1, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinPhysicsSim, 1, -1, 1)
        self.assertRaises(sims.InvalidInput, sims.CoinPhysicsSim, 1, 1, -1)

        sim = sims.CoinPhysicsSim(1, 1, 1)
        self.assertRaises(sims.InvalidInput, sim.run_trials, 0)
        self.assertRaises(sims.InvalidInput, sim.run_trials, -1)

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap_x = _non_zero_rand()
            gap_y = _non_zero_rand()
            radius = _non_zero_rand()/2

            sim = sims.CoinPhysicsSim(radius, gap_x, gap_y)

            hits = sim.run_trials(TRIALS)
            pred_hits = sim.predict_hits(TRIALS)

            # if they're equal
            # skip the calculation
            if pred_hits:
                continue

            stats = [
                (hits-pred_hits)**2/pred_hits,
                (pred_hits-hits)**2/(TRIALS-pred_hits)
            ]
            chi2 = sum(stats)
            self.assertTrue(
                chi2 < MAX_STAT,
                "chi-square = %f >= %f" % (chi2, MAX_STAT)
            )

if __name__ == '__main__':
    unittest.main()
    import doctest
    doctest.testmod()
