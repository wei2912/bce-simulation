import random
import math

class InvalidInput(Exception):
	def __init__(self, input_var, condition):
		self.input_var = input_var
		self.condition = condition
	def __str__(self):
		return "%s must not be %s." % (self.input_var, self.condition)

class CoinSim:
	def __init__(self, radius, gap_x, gap_y):
		if radius <= 0:
			raise InvalidInput("radius", "<= 0")
		if gap_x <= 0:
			raise InvalidInput("gap_x", "<= 0")
		if gap_y <= 0:
			raise InvalidInput("gap_y", "<= 0")

		self.radius = float(radius)  # Radius of the coin
		self.gap_x = float(gap_x)    # Horizontal gap between the two lines that the coin might fall on
		self.gap_y = float(gap_y)    # Vertical gap between the two lines that the coin might fall on

	def run_trials(self, trials):
		if trials <= 0:
			raise InvalidInput("trials", "<= 0")

		hits = 0

		for _ in xrange(trials):
			x = random.uniform(0.0, self.gap_x) # location of coin along x-axis after drop
			y = random.uniform(0.0, self.gap_y) # location of coin along y-axis after drop

			if (self.gap_x - x < self.radius or x < self.radius) or (self.gap_y - y < self.radius or y < self.radius):
				hits += 1

		return hits

	def predict_prob(self):
		diameter = self.radius*2
		if diameter >= self.gap_x or diameter >= self.gap_y:
			return 1.0 # will always touch

		# area of region which coin would be on if it hit
		region = self.gap_x*self.gap_y - (self.gap_x-diameter)*(self.gap_y-diameter)
		return region/(self.gap_x * self.gap_y)

	def predict_hits(self, trials):
		return self.predict_prob()*trials

class NeedleSim:
	def __init__(self, length, gap):
		if length <= 0:
			raise InvalidInput("length", "<= 0")
		if gap <= 0:
			raise InvalidInput("gap", "<= 0")

		self.length = float(length)  # Length of the needle
		self.gap = float(gap)        # Gap between the two lines where the needle falls

	def run_trials(self, trials):
		if trials <= 0:
			raise InvalidInput("trials", "<= 0")

		hits = 0

		for _ in xrange(trials):
			x = random.uniform(0.0, self.gap) # location of needle after drop

			angle = random.uniform(0.0, math.pi) # angle of needle in radians
			opp = self.length/2 * math.sin(angle)

			if self.gap - x < opp or x < opp:
				hits += 1

		return hits

class NeedleAngleSim:
	def __init__(self, length, gap, angle):
		if length <= 0:
			raise InvalidInput("length", "<= 0")
		if gap <= 0:
			raise InvalidInput("gap", "<= 0")
		if angle <= 0 or angle >= math.pi:
			raise InvalidInput("angle", "<= 0 or >= math.pi")

		self.length = float(length)  # Length of the needle
		self.gap = float(gap)        # Gap between the two lines where the needle falls
		self.angle = float(angle)    # Angle of needle

	def run_trials(self, trials):
		if trials <= 0:
			raise InvalidInput("trials", "<= 0")

		# since the angle is specified, precompute the opposite
		opp = self.length/2 * math.sin(self.angle)

		hits = 0

		for _ in xrange(trials):
			x = random.uniform(0.0, self.gap) # location of needle after drop

			if self.gap - x < opp or x < opp:
				hits += 1

		return hits

	def predict_prob(self):
		opp = self.length/2 * math.sin(self.angle)
		if opp*2 >= self.gap:
			return 1.0 # will always touch

		# area of region which needle would be on if it hit
		return opp*2/self.gap

	def predict_hits(self, trials):
		return self.predict_prob()*trials
