"""
Test suite for coin_phyulation of our variation
of Buffon's Coin Experiment.
"""

import pytest
from pytest import mark

from utils import misc, coin_phy

TRIALS = 10000 # number of trials to run per test
NUM_TESTS = 5 # number of tests to run per test case
BENCH_TRIALS = 1000 # number of trials to run for benchmarking

def test_bad_input():
    """
    If bad input is passed to the coin_phyulation,
    the coin_phyulation should raise an exception.
    """

    with pytest.raises(ValueError):
        coin_phy.run_trials(0, 1, 1)
    with pytest.raises(ValueError):
        coin_phy.run_trials(-1, 1, 1)

    with pytest.raises(ValueError):
        coin_phy.run_trials(1, 0, 1)
    with pytest.raises(ValueError):
        coin_phy.run_trials(1, -1, 1)

    with pytest.raises(TypeError):
        coin_phy.run_trials(1, 1, 1.1)
    with pytest.raises(ValueError):
        coin_phy.run_trials(1, 1, 0)
    with pytest.raises(ValueError):
        coin_phy.run_trials(1, 1, -1)

    with pytest.raises(ValueError):
        coin_phy.predict_prob(0, 1)
    with pytest.raises(ValueError):
        coin_phy.predict_prob(-1, 1)

    with pytest.raises(ValueError):
        coin_phy.predict_prob(1, 0)
    with pytest.raises(ValueError):
        coin_phy.predict_prob(1, -1)

def test_always_hit():
    """
    If the D < r * sqrt(2),
    the coin should always balance
    on the grid.
    """

    for _ in range(NUM_TESTS):
        diameter = misc.non_zero_rand()
        radius = diameter/2
        less_gap_width = misc.non_zero_rand() * (radius * 2**0.5)

        hits = coin_phy.run_trials(diameter, less_gap_width, TRIALS)
        assert hits == TRIALS
        assert coin_phy.predict_prob(diameter, less_gap_width) == 1.0

@mark.bench('coin_phy.run_trials')
def test_general():
    """
    Benchmark the general performance
    of the simulation.
    """

    diameter = misc.non_zero_rand()
    gap_width = misc.non_zero_rand()

    coin_phy.run_trials(diameter, gap_width, BENCH_TRIALS)
