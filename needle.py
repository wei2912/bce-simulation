import argparse, multiprocessing, math
from needle import mp, standard

max_trials = 1e6 # max trials a job can handle

def main(args):
	print("Length: %f" % args.length)
	print("Gap length: %f" % args.gap)
	if args.angle: print("Angle: %f" % args.angle)
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

	exp_prob = float(hits)/args.trials

	if args.angle:
		print("Experimental P(C) for angle %f = %f" % (args.angle, exp_prob))
	else:
		pred_prob = 2*args.length/args.gap/math.pi
		print("Predicted P(C) = %f" % pred_prob)
		print("Experimental P(C) = %f" % exp_prob)
		error = math.fabs(100-exp_prob/pred_prob*100)
		print("Error = %f" % error)

parser = argparse.ArgumentParser(description="Buffon's Needle Simulation")
parser.add_argument('-l', '--length', type=float, required=True, help='length of needle')
parser.add_argument('-g', '--gap', type=float, required=True, help='length of gap between two lines')
parser.add_argument('-a', '--angle', type=float, help='angle of needle. if not specified, program generates a random number as the angle.')
parser.add_argument('-t', '--trials', type=int, default=1e7, help='number of trials to run')
parser.add_argument('-p', '--process', type=int, help='number of processes to run')

args = parser.parse_args()
main(args)