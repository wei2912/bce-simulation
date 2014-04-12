from multiprocessing import Pool
import random

def run_trials(args, process, max_trials):
	p = Pool(processes=process)
	
	def trial(trials):
		hits = 0
		for _ in xrange(trials):
			x = random.uniform(0.0, args.gap)
			hits += int(args.gap - x < args.radius or x < args.radius)
		return hits

	remainder = args.trials % max_trials
	chunks = int((args.trials - remainder)/max_trials)
	trials = [max_trials for _ in xrange(chunks)]
	if remainder > 0:
		trials += [remainder]

	return sum(p.map(trial, trials))