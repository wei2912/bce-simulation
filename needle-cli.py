from collections import namedtuple
import argparse

from utils import needle

parser = argparse.ArgumentParser(description="Buffon's Needle Simulation")
parser.add_argument('-l', '--length', type=float, required=True, help='length of needle')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-a', '--angle', type=float, help='angle of needle. if not specified, program generates a random number as the angle.')
parser.add_argument('-t', '--trials', type=int, default=10000000, help='number of trials to run')

args = parser.parse_args()
needlesim = needle.NeedleSim(args.length, args.gap, args.angle, args.trials)

print(needlesim.run_trials())
