#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of a variant of Buffon's
Coin Experiment which takes into account whether the coin
would balance on the grid and prints out the number of hits.
"""

import argparse

from utils.sims import CoinPhysicsSim

def get_args():
    parser = argparse.ArgumentParser(
        description="Simulation of Buffon's Coin Experiment (physics variant)"
    )

    parser.add_argument(
        '-r',
        '--radius',
        type=float,
        required=True,
        help='radius of coin'
    )

    parser.add_argument(
        '-gx',
        '--gap_x',
        type=float,
        required=True,
        help='width of rectangular gap'
    )

    parser.add_argument(
        '-gy',
        '--gap_y',
        type=float,
        required=True,
        help='length of rectangular gap'
    )

    parser.add_argument(
        '-t',
        '--trials',
        type=int,
        default=100000,
        help='number of trials to run'
    )

    return parser.parse_args()

def main():
    args = get_args()
    sim = CoinPhysicsSim(args.radius, args.gap_x, args.gap_y)
    print "%d/%d" % (sim.run_trials(args.trials), args.trials)

main()