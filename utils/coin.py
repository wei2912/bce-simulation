import random

class Simulation:
	def __init__(self, radius, gap, trials):
		# Store the `radius`, `gap` and `trials` properties on `self` for future reference
		self.radius = radius  # Radius of the coin
		self.gap = gap        # Gap between the two lines that the coin might fall on
		self.trials = trials  # Number of times to test the coin drop

	def run_trials(self):
		# Number of times the coin touches one of the lines
		hits = 0

		# Run this loop `trials` number of times
		for _ in xrange(self.trials):
			# Generate a random decimal number between 0 and the `gap`,
			# used to indicate location of the coin after coin drop
			x = random.uniform(0.0, self.gap)

			# Boolean value indicating whether the coin touched the line
			hit = self.gap - x < self.radius or x < self.radius

			# Convert `hit` to either `0` or `1`, and increment the number of hits
			hits += int(hit)

		# Return the number of hits
		return hits
