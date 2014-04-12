import argparse, multiprocessing
from coin import mp, standard

max_trials = 1e6 # max number of trials to run per job

def main(args):
	print("Radius: %f" % args.radius)
	print("Gap length: %f" % args.gap)
	print("")
	print("Running %d trials..." % args.trials)
	print("===")

	if not args.process:
		args.process = multiprocessing.cpu_count()

	if args.process == 1 or args.trials < max_trials*args.process:
		hits = standard.run_trials(args)
	else:
		hits = mp.run_trials(args, args.process, max_trials)
	nonhits = args.trials - hits

	print("Number of hits: %d" % hits)
	print("Number of non-hits: %d" % nonhits)
	print("")

	exp_prob = hits/args.trials
	print("Experimental P(C) = %f" % exp_prob)

parser = argparse.ArgumentParser(description="Buffon's Coin Experiment - Coin Simulation")
parser.add_argument('-r', '--radius', type=float, required=True, help='radius of coin')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-t', '--trials', type=int, default=1e6, help='number of trials to run')
parser.add_argument('-p', '--process', type=int, help='number of processes to run')

args = parser.parse_args()
main(args)