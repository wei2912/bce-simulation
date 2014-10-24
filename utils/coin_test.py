"""
Test suite for simulation of Buffon's Coin Experiment.
"""

import pytest
from pytest import mark

from utils import misc, coin

TRIALS = 10000 # number of trials to run per test
NUM_TESTS = 5 # number of tests to run per test case
BENCH_TRIALS = 1000000 # number of trials to run for benchmarking

def test_bad_input():
    """
    If bad input is passed to the simulation,
    the simulation should raise an exception.
    """

    with pytest.raises(ValueError):
        coin.run_trials(0, 1, 1)
    with pytest.raises(ValueError):
        coin.run_trials(-1, 1, 1)

    with pytest.raises(ValueError):
        coin.run_trials(1, 0, 1)
    with pytest.raises(ValueError):
        coin.run_trials(1, -1, 1)

    with pytest.raises(TypeError):
        coin.run_trials(1, 1, 1.1)
    with pytest.raises(ValueError):
        coin.run_trials(1, 1, 0)
    with pytest.raises(ValueError):
        coin.run_trials(1, 1, -1)

    with pytest.raises(ValueError):
        coin.predict_prob(0, 1)
    with pytest.raises(ValueError):
        coin.predict_prob(-1, 1)

    with pytest.raises(ValueError):
        coin.predict_prob(1, 0)
    with pytest.raises(ValueError):
        coin.predict_prob(1, -1)

def test_always_hit():
    """
    If the diameter of the coin >= gap,
    the coin should always hit the grid.
    """

    for _ in range(NUM_TESTS):
        diameter = misc.non_zero_rand()
        less_gap_width = diameter - misc.non_zero_rand() * diameter

        # diameter > gap width
        hits = coin.run_trials(diameter, less_gap_width, TRIALS)
        assert hits == TRIALS
        assert coin.predict_prob(diameter, less_gap_width) == 1.0

        # diameter = gap width
        hits = coin.run_trials(diameter, diameter, TRIALS)
        assert hits == TRIALS
        assert coin.predict_prob(diameter, diameter) == 1.0

@mark.bench('coin.run_trials')
def test_general():
    """
    Benchmark the general performance
    of CoinSim.
    """

    diameter = misc.non_zero_rand()
    gap_width = misc.non_zero_rand()

    coin.run_trials(diameter, gap_width, BENCH_TRIALS)
