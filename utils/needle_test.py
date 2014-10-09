"""
Test suite for simulation of Buffon's Needle Experiment.
"""

import pytest
from pytest import mark

from utils import misc, needle

TRIALS = 10000 # number of trials to run per test
NUM_TESTS = 20 # number of tests to run per test case
BENCH_TRIALS = 1000000 # number of trials to run for benchmarking

def test_bad_input():
    """
    If bad input is passed to the simulation,
    the simulation should raise an exception.
    """

    with pytest.raises(ValueError):
	needle.run_trials(0, 1, 1)
    with pytest.raises(ValueError):
	needle.run_trials(-1, 1, 1)

    with pytest.raises(ValueError):
	needle.run_trials(1, 0, 1)
    with pytest.raises(ValueError):
	needle.run_trials(1, -1, 1)

    with pytest.raises(TypeError):
	needle.run_trials(1, 1, 1.1)
    with pytest.raises(ValueError):
	needle.run_trials(1, 1, 0)
    with pytest.raises(ValueError):
	needle.run_trials(1, 1, -1)

    with pytest.raises(ValueError):
	needle.predict_prob(0, 1)
    with pytest.raises(ValueError):
	needle.predict_prob(-1, 1)

    with pytest.raises(ValueError):
	needle.predict_prob(1, 0)
    with pytest.raises(ValueError):
	needle.predict_prob(1, -1)

def test_match_theoretical():
    """
    When the chi-square statistic is calculated,
    the p-value should be < 0.05.
    """

    results = []
    for _ in range(NUM_TESTS):
	l = misc.non_zero_rand()
	w = misc.non_zero_rand()

	hits = needle.run_trials(l, w, TRIALS)
	pred_hits = needle.predict_prob(l, w) * TRIALS

	results.append((hits, pred_hits))

    assert misc.is_pass_chi2(
	results,
	TRIALS
    )

@mark.bench('needle.run_trials')
def test_general():
    """
    Benchmark the general performance
    of NeedleSim.
    """

    l = misc.non_zero_rand()
    w = misc.non_zero_rand()

    sim = needle.run_trials(l, w, BENCH_TRIALS)
