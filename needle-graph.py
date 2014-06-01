#!/usr/bin/env python
# coding=utf-8

import argparse, math

import matplotlib.pyplot as plt

from utils import sims, stepvals

# 2D scatter plot - increasing length
def increasing_length(args):
	lengths = stepvals.get_range(args.length, args.step)
	
	## uncomment when NeedleSim.predict_prob() is implemented
	#plt.plot(
	#	lengths, 
	#	[sims.NeedleSim(length, args.gap).predict_prob() for length in lengths], 
	#	color='red', 
	#	linewidth=2.0
	#)

	for length in lengths:
		sim = sims.NeedleSim(length, args.gap)
		expprob = float(sim.run_trials(args.trials))/args.trials

		if args.verbose:
			print("length = %f, gap = %f: %f" % (length, args.gap, expprob))
		plt.scatter(length, expprob)

	plt.xlabel("Length of needle")
	plt.ylabel("P(E)")
	plt.title("Buffon's Needle Experiment - Length of needle against P(E)")
	plt.grid(True)

	if args.output:
		plt.savefig(args.output)
	else:
		plt.show()

# 2D scatter plot - increasing gap
def increasing_gap(args):
	gaps = stepvals.get_range(args.gap, args.step)
	
	## uncomment when NeedleSim.predict_prob() is implemented
	#plt.plot(
	#	lengths, 
	#	[sims.NeedleSim(length, args.gap).predict_prob() for length in lengths], 
	#	color='red', 
	#	linewidth=2.0
	#)

	for gap in gaps:
		sim = sims.NeedleSim(args.length, gap)
		expprob = float(sim.run_trials(args.trials))/args.trials

		if args.verbose:
			print("length = %f, gap = %f: %f" % (args.length, gap, expprob))
		plt.scatter(gap, expprob)

	plt.xlabel("Gap length")
	plt.ylabel("P(E)")
	plt.title("Buffon's Needle Experiment - Gap width against P(E)")
	plt.grid(True)

	if args.output:
		plt.savefig(args.output)
	else:
		plt.show()

modes = {
	0: increasing_length,
	1: increasing_gap
}

modestxt = [
	'mode 0: 2D scatter plot, length of needle against P(E)',
	'mode 1: 2D scatter plot, gap width against P(E)'
]

parser = argparse.ArgumentParser(
	description="Buffon's Needle Experiment - Needle Graph",
	epilog='\n'.join(modestxt))
parser.add_argument('-l', '--length', type=float, required=True, help='length of needle')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
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
