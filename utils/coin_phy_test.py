"""
Test suite for coin_phyulation of our variation
of Buffon's Coin Experiment.
"""

import pytest
from pytest import mark

from utils import misc, coin_phy

TRIALS = 10000 # number of trials to run per test
NUM_TESTS = 20 # number of tests to run per test case
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
    If the w < r*sqrt(2),
    the coin should always balance
    on the grid.
    """

    for _ in range(NUM_TESTS):
	d = misc.non_zero_rand()
	r = d/2
	less_w = misc.non_zero_rand() * (r * 2**0.5)

	hits = coin_phy.run_trials(d, less_w, TRIALS)
	assert hits == TRIALS
	assert coin_phy.predict_prob(d, less_w) == 1.0

def test_match_theoretical():
    """
    test_match_theoretical
    ===
    When the chi-square statistic is calculated,
    the p-value should be < 0.05.
    """

    results = []
    for _ in range(NUM_TESTS):
	d = misc.non_zero_rand()
	w = misc.non_zero_rand()

	hits = coin_phy.run_trials(d, w, TRIALS)
	pred_hits = coin_phy.predict_prob(d, w) * TRIALS

	results.append((hits, pred_hits))

    assert misc.is_pass_chi2(
	results,
	TRIALS
    )

@mark.bench('CoinPhysicscoin_phy.run_trials')
def test_general():
    """
    Benchmark the general performance
    of CoinPhysicscoin_phy.
    """

    d = misc.non_zero_rand()
    w = misc.non_zero_rand()

    coin_phy.run_trials(d, w, BENCH_TRIALS)
