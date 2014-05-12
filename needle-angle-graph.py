from collections import namedtuple
import argparse, math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import needle, stepvals

parser = argparse.ArgumentParser(description="Buffon's Needle Experiment - Needle Angle Graph")
parser.add_argument('-l', '--length', type=float, required=True, help='length of needle')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=10000, help='number of trials to run')
parser.add_argument('-s', '--step', type=float, default=0.01, help='step to take when increasing radius/gap')
parser.add_argument('-o', '--output', help='filename to output graph to')

args = parser.parse_args()

fig = plt.figure()
ax = fig.add_subplot(111)

## increasing angle - 2D cross plot ##

# truncate 0
xs = stepvals.get_range(math.pi, args.step)

for angle in xs:
	sim = needle.Simulation(args.length, args.gap, angle, args.trials)
	expprob = float(sim.run_trials())/args.trials

	print("length = %f, gap = %f, angle=%f: %f" % (args.length, args.gap, angle, expprob))
	ax.scatter(angle, expprob)

ax.set_xlabel("Angle (radians)")
ax.set_ylabel("P(E)")
ax.set_title("Buffon's Needle Experiment - Increasing angle\nlength = %f, gap = %f" % (args.length, args.gap))

if args.output:
	plt.savefig(args.output)
else:
	plt.show()
