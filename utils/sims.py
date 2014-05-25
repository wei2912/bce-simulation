import random
import math

class InvalidInput(Exception):
	def __init__(self, input_var):
		self.input_var = input_var
	def __str__(self):
		return "%s must not be <= 0." % self.input_var

class CoinSim:
	def __init__(self, radius, gap, trials):
		if radius <= 0:
			raise InvalidInput("radius")
		if gap <= 0:
			raise InvalidInput("gap")
		if trials <= 0:
			raise InvalidInput("trials")

		self.radius = radius  # Radius of the coin
		self.gap = gap        # Gap between the two lines that the coin might fall on
		self.trials = trials  # Number of times to test the coin drop

	def run_trials(self):
		hits = 0

		for _ in xrange(self.trials):
			x = random.uniform(0.0, self.gap) # location of coin after drop

			if self.gap - x < self.radius or x < self.radius:
				hits += 1

		return hits

class CoinGridSim:
	def __init__(self, radius, gap_x, gap_y, trials):
		if radius <= 0:
			raise InvalidInput("radius")
		if gap_x <= 0:
			raise InvalidInput("gap_x")
		if gap_y <= 0:
			raise InvalidInput("gap_y")
		if trials <= 0:
			raise InvalidInput("trials")

		self.radius = radius  # Radius of the coin
		self.gap_x = gap_x    # Horizontal gap between the two lines that the coin might fall on
		self.gap_y = gap_y    # Vertical gap between the two lines that the coin might fall on
		self.trials = trials  # Number of times to test the coin drop

	def run_trials(self):
		hits = 0

		for _ in xrange(self.trials):
			x = random.uniform(0.0, self.gap_x) # location of coin along x-axis after drop
			y = random.uniform(0.0, self.gap_y) # location of coin along y-axis after drop

			if (self.gap_x - x < self.radius or x < self.radius) or (self.gap_y - y < self.radius or y < self.radius):
				hits += 1

		return hits

class NeedleSim:
	def __init__(self, length, gap, trials):
		if length <= 0:
			raise InvalidInput("length")
		if gap <= 0:
			raise InvalidInput("gap")
		if trials <= 0:
			raise InvalidInput("trials")

		self.length = length  # Length of the needle
		self.gap = gap        # Gap between the two lines where the needle falls
		self.trials = trials  # Number of times to test the needle drop

	def run_trials(self):
		hits = 0

		for _ in xrange(self.trials):
			x = random.uniform(0.0, self.gap) # location of needle after drop

			angle = random.uniform(0.0, math.pi) # angle of needle in radians
			opp = self.length/2 * math.sin(angle)

			if self.gap - x < opp or x < opp:
				hits += 1

		return hits

class NeedleAngleSim:
	def __init__(self, length, gap, angle, trials):
		if length <= 0:
			raise InvalidInput("length")
		if gap <= 0:
			raise InvalidInput("gap")
		if angle <= 0:
			raise InvalidInput("angle")
		if trials <= 0:
			raise InvalidInput("trials")

		self.length = length  # Length of the needle
		self.gap = gap        # Gap between the two lines where the needle falls
		self.angle = angle    # Angle of needle
		self.trials = trials  # Number of times to test the needle drop

	def run_trials(self):
		# since the angle is specified, precompute the opposite
		opp = self.length/2 * math.sin(self.angle)

		hits = 0

		for _ in xrange(self.trials):
			x = random.uniform(0.0, self.gap) # location of needle after drop

			if self.gap - x < opp or x < opp:
				hits += 1

		return hits
