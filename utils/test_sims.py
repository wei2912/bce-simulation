import unittest

import random
import math
from sims import InvalidInput, CoinSim, NeedleSim, NeedleAngleSim, CoinPhysicsSim

TRIALS = 10000 # number of trials to run per test case
NUM_TESTS = 10 # number of tests to run per test case
MAX_STAT = 3.841 # p < 0.05 for a df of 1

sqrt_2 = 2**0.5

def _non_zero_rand():
    """
    Returns a random float x where
    0.0 < x <= 1.0
    """
    return 1.0 - random.random()

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

        self.assertRaises(InvalidInput, CoinSim, 0, 1)
        self.assertRaises(InvalidInput, CoinSim, 1, 0)

        self.assertRaises(InvalidInput, CoinSim, -1, 1)
        self.assertRaises(InvalidInput, CoinSim, 1, -1)

        sim = CoinSim(1, 1)
        self.assertRaises(InvalidInput, sim.run_trials, 0)
        self.assertRaises(InvalidInput, sim.run_trials, -1)

    def test_always_hit(self):
        """
        test_always_hit
        ===
        If the diameter of the coin >= gap,
        the coin should always hit the grid.
        """

        for _ in range(NUM_TESTS):
            radius = 1.0 - _non_zero_rand()
            diameter = radius*2
            less_gap = diameter - _non_zero_rand()*diameter

            sim = CoinSim(radius, less_gap)
            hits = sim.run_trials(TRIALS)
            self.assertEquals(
            	hits,
            	TRIALS,
            	"coin does not always hit (radius=%f, gap=%f)"
            		% (radius, less_gap)
            )
            self.assertEquals(
            	sim.predict_prob(),
            	1.0,
            	"predicted probability != 1.0 (radius=%f, gap=%f)"
            		% (radius, less_gap)
            )

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap = _non_zero_rand()
            radius = _non_zero_rand()/2

            sim = CoinSim(radius, gap)

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
                "chi-square = %f >= %f (radius=%f, gap=%f)"
                	% (chi2, MAX_STAT, radius, gap)
            )

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

        self.assertRaises(InvalidInput, NeedleSim, 0, 1)
        self.assertRaises(InvalidInput, NeedleSim, 1, 0)

        self.assertRaises(InvalidInput, NeedleSim, -1, 1)
        self.assertRaises(InvalidInput, NeedleSim, 1, -1)

        sim = NeedleSim(1, 1)
        self.assertRaises(InvalidInput, sim.run_trials, 0)
        self.assertRaises(InvalidInput, sim.run_trials, -1)

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap = _non_zero_rand()
            length = _non_zero_rand()

            sim = NeedleSim(length, gap)

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
                "chi-square = %f >= %f (length=%f, gap=%f)"
                    % (chi2, MAX_STAT, length, gap)
            )

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

        self.assertRaises(InvalidInput, NeedleAngleSim, 0, 1, 0.1)
        self.assertRaises(InvalidInput, NeedleAngleSim, 1, 0, 0.1)

        self.assertRaises(InvalidInput, NeedleAngleSim, -1, 1, 0.1)
        self.assertRaises(InvalidInput, NeedleAngleSim, 1, -1, 0.1)

        self.assertRaises(InvalidInput, NeedleAngleSim, 1, 1, math.pi)
        self.assertRaises(InvalidInput, NeedleAngleSim, 1, 1, 3.15)
        self.assertRaises(InvalidInput, NeedleAngleSim, 1, 1, -0.1)

        sim = NeedleAngleSim(1, 1, 0.1)
        self.assertRaises(InvalidInput, sim.run_trials, 0)
        self.assertRaises(InvalidInput, sim.run_trials, -1)

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

            sim = NeedleAngleSim(length, less_gap, angle)
            hits = sim.run_trials(TRIALS)
            self.assertEquals(
                hits,
                TRIALS,
                "needle does not always hit (length=%f, gap=%f, angle=%f)"
                    % (length, less_gap, angle)
            )
            self.assertEquals(
                sim.predict_prob(),
                1.0,
                "predicted probability != 1.0 (length=%f, gap=%f, angle=%f)"
                    % (length, less_gap, angle)
            )

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

            sim = NeedleAngleSim(length, gap, angle)

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
                "chi-square = %f >= %f (length=%f, gap=%f, angle=%f)"
                    % (chi2, MAX_STAT, length, gap, angle)
            )

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

        self.assertRaises(InvalidInput, CoinPhysicsSim, 0, 1)
        self.assertRaises(InvalidInput, CoinPhysicsSim, 1, 0)

        self.assertRaises(InvalidInput, CoinPhysicsSim, -1, 1)
        self.assertRaises(InvalidInput, CoinPhysicsSim, 1, -1)

        sim = CoinPhysicsSim(1, 1)
        self.assertRaises(InvalidInput, sim.run_trials, 0)
        self.assertRaises(InvalidInput, sim.run_trials, -1)

    def test_always_hit(self):
        """
        test_always_hit
        ===

        If the gap < r*(2**0.5),
        the coin should always balance
        on the grid.
        """

        for _ in range(NUM_TESTS):
            radius = _non_zero_rand()/2
            less_gap = _non_zero_rand() * (radius*sqrt_2)

            sim = CoinPhysicsSim(radius, less_gap)
            hits = sim.run_trials(TRIALS)
            self.assertEquals(
                hits,
                TRIALS,
                "coin does not always balance (radius=%f, gap=%f)"
                    % (radius, less_gap)
            )
            self.assertEquals(
                sim.predict_prob(),
                1.0,
                "predicted probability != 1.0 (radius=%f, gap=%f)"
                    % (radius, less_gap)
            )

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        for _ in range(NUM_TESTS):
            gap = _non_zero_rand()
            radius = _non_zero_rand()/2

            sim = CoinPhysicsSim(radius, gap)

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
                "chi-square = %f >= %f (radius=%f, gap=%f)"
                    % (chi2, MAX_STAT, radius, gap)
            )

if __name__ == '__main__':
    unittest.main()
