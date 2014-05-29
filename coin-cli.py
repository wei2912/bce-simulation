#!/usr/bin/env python
# coding=utf-8

from collections import namedtuple
import argparse

from utils import sims

parser = argparse.ArgumentParser(description="Buffon's Coin Simulation")
parser.add_argument('-r', '--radius', type=float, required=True, help='radius of coin')
parser.add_argument('-gx', '--gap_x', type=float, required=True, help='length of horizontal gap between two lines')
parser.add_argument('-gy', '--gap_y', type=float, required=True, help='length of vertical gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=1000000, help='number of trials to run')

args = parser.parse_args()
sim = sims.CoinSim(args.radius, args.gap_x, args.gap_y, args.trials)

print(sim.run_trials())
