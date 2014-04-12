import random, math

def run_trials(args):
	hits = 0
	for _ in xrange(args.trials):
		x = random.uniform(0.0, args.gap)
		angle = random.uniform(0.0, math.pi) # in radians

		opposite = args.length/2 * math.sin(angle)
		hits += int(args.gap - x < opposite or x < opposite)
	return hits