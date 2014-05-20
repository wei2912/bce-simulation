#!/usr/bin/env python
# coding=utf-8

import argparse

from utils import sims

parser = argparse.ArgumentParser(description="Buffon's Coin Simulation")
parser.add_argument('-r', '--radius', type=float, required=True, help='radius of coin')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=10000000, help='number of trials to run')

args = parser.parse_args()
sim = sims.CoinSim(args.radius, args.gap, args.trials)

print(sim.run_trials())
