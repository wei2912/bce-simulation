#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Needle
Experiment and prints out the number of hits.
"""

import argparse

from utils import sims

def get_args():
    parser = argparse.ArgumentParser(
        description="Simulation of Buffon's Needle Experiment"
    )

    parser.add_argument(
        '-l',
        '--length',
        type=float,
        required=True,
        help='length of needle'
    )

    parser.add_argument(
        '-g',
        '--gap',
        type=float,
        required=True,
        help='length of gap between two lines'
    )

    parser.add_argument(
        '-a',
        '--angle',
        type=float,
        help=('angle of needle (if provided, angle will be fixed)')
    )

    parser.add_argument(
        '-t',
        '--trials',
        type=int,
        default=1000000,
        help='number of trials to run'
    )

    return parser.parse_args()

def main():
    args = get_args()
    if args.angle:
        sim = sims.NeedleAngleSim(args.length, args.gap, args.angle)
    else:
        sim = sims.NeedleSim(args.length, args.gap)
    print "%d/%d" % (sim.run_trials(args.trials), args.trials)

main()
