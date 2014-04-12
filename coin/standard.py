import random

def run_trials(args):
	hits = 0
	for _ in xrange(args.trials):
		x = random.uniform(0.0, args.gap)
		hits += int(args.gap - x < args.radius or x < args.radius)
	return hits