import random

class CoinSim:
	def __init__(self, radius, gap, trials):
		self.radius = radius
		self.gap = gap
		self.trials = trials

	def run_trials(self):
		hits = 0
		for _ in xrange(self.trials):
			x = random.uniform(0.0, self.gap)
			hits += int(self.gap - x < self.radius or x < self.radius)
		return hits
