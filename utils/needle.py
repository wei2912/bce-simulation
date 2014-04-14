import random, math

class NeedleSim:
	def __init__(self, length, gap, angle, trials):
		self.length = length
		self.gap = gap
		self.angle = angle
		self.trials = trials

	def run_trials(self):
		# if the angle is specified, precompute it
		if self.angle:
			oppval = self.length/2 * math.sin(self.angle)

		hits = 0
		for _ in xrange(self.trials):
			x = random.uniform(0.0, self.gap)

			if self.angle:
				opposite = oppval
			else:
				angle = random.uniform(0.0, math.pi) # in radians
				opposite = self.length/2 * math.sin(angle)

			hits += int(self.gap - x < opposite or x < opposite)
		return hits
