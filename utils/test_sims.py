"""
This module contains test suites for all simulations
in `sims.py`.
"""

import unittest
import math
import random

from utils import sims

TRIALS = 10000 # number of trials to run per test case
NUM_TESTS = 10 # number of tests to run
MAX_STAT = 3.841 # p < 0.05 for a df of 1

def non_zero_rand():
    """
    Returns a random float x where
    0.0 < x <= 1.0
    """
    return 1.0 - random.random()

class TestCoinSim(unittest.TestCase):
    """
    Test suite for CoinSim.
    """

    def __bad_input_test(self):
        """
        bad_input_test
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

    def __always_hit_test(self):
        """
        always_hit_test
        ===
        If the diameter of the coin >= gap_x or
        the diameter of the coin >= gap_y,
        the coin should always hit the grid.
        """

        for _ in range(NUM_TESTS):
            radius = 1.0 - non_zero_rand()
            diameter = radius*2
            more_gap = diameter + non_zero_rand()
            less_gap = diameter - non_zero_rand()*diameter

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

    def __match_theoretical_test(self):
        """
        match_theoretical_test
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap_x = non_zero_rand()
            gap_y = non_zero_rand()
            radius = non_zero_rand()/2

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

    def test_init(self):
        """
        Runs the following tests for the init function:
        * bad_input_test
        """
        self.__bad_input_test()

    def test_run_trials(self):
        """
        Runs the following tests for function `run_trials`:
        * always_hit_test
        * match_theoretical_test
        """
        self.__always_hit_test()
        self.__match_theoretical_test()

class TestNeedleSim(unittest.TestCase):
    """
    Test suite for NeedleSim.
    """

    def __bad_input_test(self):
        """
        bad_input_test
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

    def test_init(self):
        """
        Runs the following tests for the init function:
        * bad_input_test
        """
        self.__bad_input_test()

class TestNeedleAngleSim(unittest.TestCase):
    """
    Test suite for NeedleAngleSim.
    """

    def __bad_input_test(self):
        """
        bad_input_test
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

    def __always_hit_test(self):
        """
        always_hit_test
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
            angle = non_zero_rand()*math.pi

            opp = non_zero_rand()
            length = opp/math.sin(angle)

            less_gap = opp - non_zero_rand()*opp

            sim = sims.NeedleAngleSim(length, less_gap, angle)
            hits = sim.run_trials(TRIALS)
            self.assertEquals(hits, TRIALS, "needle does not always hit")

    def __match_theoretical_test(self):
        """
        match_theoretical_test
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            angle = random.uniform(0.0, math.pi)
            length = non_zero_rand()
            gap = non_zero_rand()

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

    def test_init(self):
        """
        Runs the following tests for the init function:
        * bad_input_test
        """
        self.__bad_input_test()

    def test_run_trials(self):
        """
        Runs the following tests for function `run_trials`:
        * always_hit_test
        * match_theoretical_test
        """
        self.__always_hit_test()
        self.__match_theoretical_test()

class TestCoinPhysicsSim(unittest.TestCase):
    """
    Test suite for CoinPhysicsSim.
    """

    def __bad_input_test(self):
        """
        bad_input_test
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

    def __match_theoretical_test(self):
        """
        match_theoretical_test
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap_x = non_zero_rand()
            gap_y = non_zero_rand()
            radius = non_zero_rand()/2

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

    def test_init(self):
        """
        Runs the following tests for the init function:
        * bad_input_test
        """
        self.__bad_input_test()

    def test_run_trials(self):
        """
        Runs the following tests for function `run_trials`:
        * match_theoretical_test
        """
        self.__match_theoretical_test()

if __name__ == '__main__':
    unittest.main()
