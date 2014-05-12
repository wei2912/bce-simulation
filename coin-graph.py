#!/usr/bin/env python

from collections import namedtuple
import argparse, math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import coin, stepvals

parser = argparse.ArgumentParser(description="Buffon's Coin Experiment - Coin Graph")
parser.add_argument('-r', '--radius', type=float, required=True, help='max radius of coin')
parser.add_argument('-g', '--gap', type=float, required=True, help='max length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=10000, help='number of trials to run')
parser.add_argument('-s', '--step', type=float, default=0.5, help='step to take when increasing radius/gap')
parser.add_argument('-o', '--output', help='filename to output graph to')
parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')

args = parser.parse_args()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# increasing radius and gap - 3D scatter plot

# truncate 0
xs = stepvals.get_range(args.radius, args.step)
ys = stepvals.get_range(args.gap, args.step)

for radius in xs:
	for gap in ys:
		sim = coin.Simulation(radius, gap, args.trials)
		expprob = float(sim.run_trials())/args.trials

		if args.verbose:
			print("radius = %f, gap = %f: %f" % (radius, gap, expprob))
		ax.scatter(radius, gap, expprob)

ax.set_xlabel("Radius")
ax.set_ylabel("Gap")
ax.set_zlabel("P(E)")
ax.set_title("Buffon's Coin Experiment - Increasing radius & gap")

if args.output:
	plt.savefig(args.output)
else:
	plt.show()
