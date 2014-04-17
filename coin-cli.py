from collections import namedtuple
import argparse

from utils import coin

parser = argparse.ArgumentParser(description="Buffon's Coin Simulation")
parser.add_argument('-r', '--radius', type=float, required=True, help='radius of coin')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=10000000, help='number of trials to run')

args = parser.parse_args()
coinsim = coin.CoinSim(args.radius, args.gap, args.trials)

print(coinsim.run_trials())
