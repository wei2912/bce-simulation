"""
This module contains test suites for simulations
in `sims.py` that can be runned when the module
is runned from the command line.
"""

import pytest

import random
import math
from utils.sims import InvalidInput, CoinSim, NeedleSim, NeedleAngleSim, CoinPhysicsSim
from utils import stepvals

TRIALS = 10000 # number of trials to run per test case
NUM_TESTS = 5 # number of tests to run per test case
MAX_STAT = 3.841 # p < 0.05 for a df of 1

SQRT_2 = 2**0.5

def _non_zero_rand():
    """
    Returns a random float x where
    0.0 < x <= 1.0
    """
    return 1.0 - random.random()

class TestCoinSim:
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

        with pytest.raises(InvalidInput):
            CoinSim(0, 1)
        with pytest.raises(InvalidInput):
            CoinSim(1, 0)

        with pytest.raises(InvalidInput):
            CoinSim(-1, 1)
        with pytest.raises(InvalidInput):
            CoinSim(1, -1)

        sim = CoinSim(1, 1)
        with pytest.raises(InvalidInput):
            sim.run_trials(0)
        with pytest.raises(InvalidInput):
            sim.run_trials(-1)

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
            assert hits == TRIALS
            assert sim.predict_prob() == 1.0

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        pairs = []
        for radius in stepvals.get_range(0.5, TRIALS):
            pairs += [(radius, 1.0)]
        for gap in stepvals.get_range(1.0, TRIALS):
            pairs += [(0.05, gap)]

        for pair in pairs:
            sim = CoinSim(pair[0], pair[1])

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
            assert chi2 < MAX_STAT

class TestNeedleSim:
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

        with pytest.raises(InvalidInput):
            NeedleSim(0, 1)
        with pytest.raises(InvalidInput):
            NeedleSim(1, 0)

        with pytest.raises(InvalidInput):
            NeedleSim(-1, 1)
        with pytest.raises(InvalidInput):
            NeedleSim(1, -1)

        sim = NeedleSim(1, 1)
        with pytest.raises(InvalidInput):
            sim.run_trials(0)
        with pytest.raises(InvalidInput):
            sim.run_trials(-1)

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        pairs = []
        for length in stepvals.get_range(1.0, TRIALS):
            pairs += [(length, 0.5)]
        for gap in stepvals.get_range(1.0, TRIALS):
            pairs += [(0.5, gap)]

        for pair in pairs:
            sim = NeedleSim(pair[0], pair[1])

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
            assert chi2 < MAX_STAT

class TestNeedleAngleSim:
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

        with pytest.raises(InvalidInput):
            NeedleAngleSim(0, 1, 0.1)
        with pytest.raises(InvalidInput):
            NeedleAngleSim(1, 0, 0.1)

        with pytest.raises(InvalidInput):
            NeedleAngleSim(-1, 1, 0.1)
        with pytest.raises(InvalidInput):
            NeedleAngleSim(1, -1, 0.1)

        with pytest.raises(InvalidInput):
            NeedleAngleSim(1, 1, math.pi)
        with pytest.raises(InvalidInput):
            NeedleAngleSim(1, 1, 3.15)
        with pytest.raises(InvalidInput):
            NeedleAngleSim(1, 1, -0.1)

        sim = NeedleAngleSim(1, 1, 0.1)
        with pytest.raises(InvalidInput):
            sim.run_trials(0)
        with pytest.raises(InvalidInput):
            sim.run_trials(-1)

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
            assert hits == TRIALS
            assert sim.predict_prob() == 1.0

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        angle = random.uniform(0.0, math.pi)

        pairs = []
        for length in stepvals.get_range(1.0, TRIALS):
            pairs += [(length, 0.5)]
        for gap in stepvals.get_range(1.0, TRIALS):
            pairs += [(0.5, gap)]

        for pair in pairs:
            sim = NeedleAngleSim(pair[0], pair[1], angle)

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
            assert chi2 < MAX_STAT

class TestCoinPhysicsSim:
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

        with pytest.raises(InvalidInput):
            CoinPhysicsSim(0, 1)
        with pytest.raises(InvalidInput):
            CoinPhysicsSim(1, 0)

        with pytest.raises(InvalidInput):
            CoinPhysicsSim(-1, 1)
        with pytest.raises(InvalidInput):
            CoinPhysicsSim(1, -1)

        sim = CoinPhysicsSim(1, 1)
        with pytest.raises(InvalidInput):
            sim.run_trials(0)
        with pytest.raises(InvalidInput):
            sim.run_trials(-1)

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
            less_gap = _non_zero_rand() * (radius*SQRT_2)

            sim = CoinPhysicsSim(radius, less_gap)
            hits = sim.run_trials(TRIALS)
            assert hits == TRIALS
            assert sim.predict_prob() == 1.0

    def test_match_theoretical(self):
        """
        test_match_theoretical
        ===
        When the chi-square statistic is calculated,
        the p-value should be < 0.05.
        """

        pairs = []
        for radius in stepvals.get_range(0.5, TRIALS):
            pairs += [(radius, 1.0)]
        for gap in stepvals.get_range(1.0, TRIALS):
            pairs += [(0.05, gap)]

        for pair in pairs:
            sim = CoinPhysicsSim(pair[0], pair[1])

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
            assert chi2 < MAX_STAT
