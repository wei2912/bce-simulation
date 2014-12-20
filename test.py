#!/usr/bin/env python
# coding=utf-8

"""
This script tests the simulations of the experiments.
"""

import math

from utils import coin_var, needle_var

def main():
    needle_var_vals = [
        (1.1, 1.0),
        (1.4, 1.0),
        (2.0, 1.0),

        (2.9, 1.0),
        (3.3, 1.0),
        (5.0, 1.0)
    ]

    print("needle_var:")
    for L, D in needle_var_vals:
        trials = 1000000
        pred_prob = needle_var.predict_prob(length=L, gap_width=D)
        pred_hits = pred_prob * trials
        hits = needle_var.run_trials(length=L, gap_width=D, trials=trials)

        if pred_hits == 0 or pred_hits == trials:
            stat = float('nan')
        else:
            stat = sum([
                (hits - pred_hits) ** 2 / pred_hits,
                ((trials - hits) - (trials - pred_hits)) ** 2 / (trials-pred_hits)
            ])

        print("L = {}, D = {}, expected = {}, observed = {}, stat = {}".format(L, D, pred_hits, hits, stat))

    print("coin_var:")
    coin_var_vals = [
        (1.0, 1.0),
        (1.0, 1.2),
        (1.0, math.sqrt(2)),

        (1.0, 1.5),
        (1.0, 1.8),
        (1.0, 1.9),

        (1.0, 2.0),
        (1.0, 3.0),
        (1.0, 5.0)
    ]

    for R, D in coin_var_vals:
        trials = 100000
        pred_prob = coin_var.predict_prob(diameter=2*R, gap_width=D)
        pred_hits = pred_prob * trials
        hits = coin_var.run_trials(diameter=2*R, gap_width=D, trials=trials)

        if pred_hits == 0 or pred_hits == trials:
            stat = float('nan')
        else:
            stat = sum([
                (hits - pred_hits) ** 2 / pred_hits,
                ((trials - hits) - (trials - pred_hits)) ** 2 / (trials-pred_hits)
            ])

        print("R = {}, D = {}, expected = {}, observed = {}, stat = {}".format(R, D, pred_hits, hits, stat))
main()
