"""
Test suite for simulation of Buffon's Needle Experiment.
"""

import pytest
from pytest import mark

from utils import misc, needle_phy

TRIALS = 10000 # number of trials to run per test
NUM_TESTS = 5 # number of tests to run per test case
BENCH_TRIALS = 1000000 # number of trials to run for benchmarking

def test_bad_input():
    """
    If bad input is passed to the simulation,
    the simulation should raise an exception.
    """

    with pytest.raises(ValueError):
        needle_phy.run_trials(0, 1, 1)
    with pytest.raises(ValueError):
        needle_phy.run_trials(-1, 1, 1)

    with pytest.raises(ValueError):
        needle_phy.run_trials(1, 0, 1)
    with pytest.raises(ValueError):
        needle_phy.run_trials(1, -1, 1)

    with pytest.raises(TypeError):
        needle_phy.run_trials(1, 1, 1.1)
    with pytest.raises(ValueError):
        needle_phy.run_trials(1, 1, 0)
    with pytest.raises(ValueError):
        needle_phy.run_trials(1, 1, -1)

    with pytest.raises(ValueError):
        needle_phy.predict_prob(0, 1)
    with pytest.raises(ValueError):
        needle_phy.predict_prob(-1, 1)

    with pytest.raises(ValueError):
        needle_phy.predict_prob(1, 0)
    with pytest.raises(ValueError):
        needle_phy.predict_prob(1, -1)

@mark.bench('needle.run_trials')
def test_general():
    """
    Benchmark the general performance
    of NeedleSim.
    """

    length = misc.non_zero_rand()
    gap_width = misc.non_zero_rand()

    needle_phy.run_trials(length, gap_width, BENCH_TRIALS)
