#!/usr/bin/env python
# coding=utf-8

import argparse, math

import matplotlib.pyplot as plt

from utils import sims, stepvals

# 2D scatter plot - increasing angle
def increasing_angle(args):
	angles = stepvals.get_range(math.pi, args.step)[:-1] # we don't want math.pi
	plt.plot(
		angles, 
		[sims.NeedleAngleSim(args.length, args.gap, angle).predict_prob() for angle in angles], 
		color='red', 
		linewidth=2.0
	)

	for angle in angles:
		sim = sims.NeedleAngleSim(args.length, args.gap, angle)
		expprob = float(sim.run_trials(args.trials))/args.trials

		if args.verbose:
			print("length = %f, gap = %f, angle=%f: %f" % (args.length, args.gap, angle, expprob))
		plt.scatter(angle, expprob)

	plt.xlabel("Angle of needle (radians)")
	plt.ylabel("P(E)")
	plt.title("Buffon's Needle Experiment - Angle of needle (radians) against P(E)")

	if args.output:
		plt.savefig(args.output)
	else:
		plt.show()

parser = argparse.ArgumentParser(description="Buffon's Needle Experiment - Needle Angle Graph")
parser.add_argument('-l', '--length', type=float, required=True, help='length of needle')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=1000, help='number of trials to run')
parser.add_argument('-s', '--step', type=float, required=True, help='step to take when increasing radius/gap')
parser.add_argument('-o', '--output', help='filename to output graph to')
parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')

args = parser.parse_args()
increasing_angle(args)
