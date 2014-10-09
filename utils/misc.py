"""
This module contains miscellaneous stuff.
"""

import random

MAX_STAT = 3.841 # p < 0.05 for a df of 1
MAX_FAILS = 0.1 # percentage of Chi-Square tests that can fail
		# before the test is reported to have failed

def __is_sequence(arg):
    return (not hasattr(arg, "strip") and
	    hasattr(arg, "__getitem__") or
	    hasattr(arg, "__iter__"))

def __validate_pos(l, msg):
    if __is_sequence(l):
	for i in xrange(len(l)):
	    if l[i] <= 0:
		raise ValueError(msg)
	    l[i] = float(l[i])
	return l
    if l <= 0:
	raise ValueError(msg)
    return float(l)

def validate_length(l):
    return __validate_pos(l, "length of needle is not positive")

def validate_diameter(d):
    return __validate_pos(d, "diameter of coin is not positive")

def validate_width(w):
    return __validate_pos(w, "width of gap is not positive")

def validate_trials(trials):
    if not int(trials) == trials:
	raise TypeError("Number of trials is not an integer")
    if trials <= 0:
	raise ValueError("number of trials is not positive")
    return int(trials)

def non_zero_rand():
    """
    Returns a random float x where
    0.0 < x <= 1.0
    """
    return 1.0 - random.random()

def is_pass_chi2(results, trials):
    """
    Calculates a chi-square statistic and
    return a boolean value indicating if
    the test is passed.
    """

    fails = 0
    for result in results:
	hits, pred_hits = result

	if pred_hits == hits:
	    continue
	elif pred_hits == 0 or pred_hits == trials:
	    # if the predicted number of hits reaches an extreme value
	    # it should fail automatically if pred_hits != hits.
	    fails += 1
	    continue

	stats = [
	    (hits - pred_hits)**2 / pred_hits,
	    ((trials - hits) - (trials - pred_hits))**2 / (trials-pred_hits)
	]

	if sum(stats) > MAX_STAT:
	    fails += 1

	if fails >= MAX_FAILS*len(results):
	    return False
    return True

def get_prob(hits, trials):
    return float(hits)/trials
