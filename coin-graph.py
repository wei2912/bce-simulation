#!/usr/bin/env python
# coding=utf-8

import argparse, math

import matplotlib.pyplot as plt

from utils import sims, stepvals

# 2D scatter plot - increasing width of square gap
def increasing_width(args):
	gaps = stepvals.get_range(args.gap, args.step)
	plt.plot(
		gaps, 
		[sims.CoinSim(args.radius, gap, gap).predict_prob() for gap in gaps], 
		color='red', 
		linewidth=2.0
	)
	
	for gap in gaps:
		sim = sims.CoinSim(args.radius, gap, gap)
		expprob = float(sim.run_trials(args.trials))/args.trials

		if args.verbose:
			print("radius = %f, gap = %f: %f" % (args.radius, gap, expprob))
		plt.scatter(gap, expprob)

	plt.xlabel("Width of square gap")
	plt.ylabel("P(E)")
	plt.title("Buffon's Coin Experiment - Width of square gap against P(E)")
	plt.grid(True)

	if args.output:
		plt.savefig(args.output)
	else:
		plt.show()

# 2D scatter plot - increasing radius
def increasing_radius(args):
	radii = stepvals.get_range(args.radius, args.step)
	plt.plot(
		radii, 
		[sims.CoinSim(radius, args.gap, args.gap).predict_prob() for radius in radii], 
		color='red', 
		linewidth=2.0
	)
	
	for radius in radii:
		sim = sims.CoinSim(radius, args.gap, args.gap)
		expprob = float(sim.run_trials(args.trials))/args.trials

		if args.verbose:
			print("radius = %f, gap = %f: %f" % (radius, args.gap, expprob))
		plt.scatter(radius, expprob)

	plt.xlabel("Radius")
	plt.ylabel("P(E)")
	plt.title("Buffon's Coin Experiment - Radius against P(E)")
	plt.grid(True)

	if args.output:
		plt.savefig(args.output)
	else:
		plt.show()

modes = {
	0: increasing_width,
	1: increasing_radius
}

modestxt = [
	'mode 0: 2D scatter plot, width of square gap against P(E)',
	'mode 1: 2D scatter plot, radius against P(E)'
]

parser = argparse.ArgumentParser(
	description="Buffon's Coin Experiment - Coin Graph",
	epilog="\n".join(modestxt))
parser.add_argument('-r', '--radius', type=float, required=True, help='max radius of coin')
parser.add_argument('-g', '--gap', type=float, required=True, help='max width of square gap')
parser.add_argument('-t', '--trials', type=int, default=1000, help='number of trials to run')
parser.add_argument('-s', '--step', type=float, required=True, help='step to take when increasing radius/gap')
parser.add_argument('-o', '--output', help='filename to output graph to')
parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
parser.add_argument('-m', '--mode', type=int, required=True, help='mode decides which type of graph to generate. refer to below for more details.')

args = parser.parse_args()

if args.mode in modes:
	modes[args.mode](args)
else:
	print("Mode number is invalid. Please type 'python coin-graph.py -h' for more details.")
