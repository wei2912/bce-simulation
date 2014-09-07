"""
Test suite for simulation of Buffon's Coin Experiment.
"""

import pytest
from pytest import mark

from utils import misc, coin

TRIALS = 10000 # number of trials to run per test
NUM_TESTS = 20 # number of tests to run per test case
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
	d = misc.non_zero_rand()
	less_w = d - misc.non_zero_rand()*d

	# diameter > gap
	hits = coin.run_trials(d, less_w, TRIALS)
	assert hits == TRIALS
	assert coin.predict_prob(d, less_w) == 1.0

	# diameter = gap
	hits = coin.run_trials(d, d, TRIALS)
	assert hits == TRIALS
	assert coin.predict_prob(d, d) == 1.0

def test_match_theoretical():
    """
    When the chi-square statistic is calculated,
    the p-value should be < 0.05.
    """

    results = []
    for _ in range(NUM_TESTS):
	d = misc.non_zero_rand()
	w = misc.non_zero_rand()

	hits = coin.run_trials(d, w, TRIALS)
	pred_hits = coin.predict_prob(d, w) * TRIALS

	results.append((hits, pred_hits))

    assert misc.is_pass_chi2(
	results,
	TRIALS
    )

@mark.bench('coin.run_trials')
def test_general():
    """
    Benchmark the general performance
    of CoinSim.
    """

    d = misc.non_zero_rand()
    w = misc.non_zero_rand()

    coin.run_trials(d, w, BENCH_TRIALS)
