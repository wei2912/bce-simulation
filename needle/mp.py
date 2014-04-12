from multiprocessing import Pool
import random, math

def run_trials(args, num_process, max_trials):
	# if the angle is specified, precompute it
	if args.angle:
		oppval = args.length/2 * math.sin(args.angle)

	p = Pool(processes=num_process)

	def trial(trials):
		hits = 0
		for _ in xrange(trials):
			x = random.uniform(0.0, args.gap)

			if args.angle:
				opposite = oppval
			else:
				angle = random.uniform(0.0, math.pi) # in radians
				opposite = args.length/2 * math.sin(angle)
			hits += int(args.gap - x < opposite or x < opposite)
		return hits

	remainder = args.trials % max_trials
	chunks = int((args.trials - remainder)/max_trials)
	trials = [max_trials for _ in xrange(chunks)]
	if remainder > 0:
		trials += [remainder]

	return sum(p.map(trial, trials))