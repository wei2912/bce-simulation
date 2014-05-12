from collections import namedtuple
import argparse, math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import needle, stepvals

parser = argparse.ArgumentParser(description="Buffon's Needle Experiment - Needle Graph")
parser.add_argument('-l', '--length', type=float, required=True, help='length of needle')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=10000, help='number of trials to run')
parser.add_argument('-s', '--step', type=float, default=0.1, help='step to take when increasing radius/gap')
parser.add_argument('-o', '--output', help='filename to output graph to')

args = parser.parse_args()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

## increasing length and gap - 3D scatter plot ##

# truncate 0
xs = stepvals.get_range(args.length, args.step)
ys = stepvals.get_range(args.gap, args.step)

for length in xs:
	for gap in ys:
		sim = needle.Simulation(length, gap, None, args.trials)
		expprob = float(sim.run_trials())/args.trials

		print("length = %f, gap = %f: %f" % (length, gap, expprob))
		ax.scatter(length, gap, expprob)

ax.set_xlabel("Length")
ax.set_ylabel("Gap")
ax.set_zlabel("P(E)")
ax.set_title("Buffon's Needle Experiment - Increasing length & gap")

if args.output:
	plt.savefig(args.output)
else:
	plt.show()
