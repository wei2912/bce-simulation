import unittest
import random
import math

import sims

TRIALS = 10000 # number of trials to run per test case
MAX_STAT = 3.841 # 0.05 level of significance, 1 degree of freedom

class TestCoinSim(unittest.TestCase):
	def _predict_prob(self, radius, gap_x, gap_y):
		diameter = radius*2
		if diameter > gap_x or diameter > gap_y:
			return 1.0 # will always touch

		region = gap_x*gap_y - (gap_x-diameter)*(gap_y-diameter) # area of region which coin would hit
		pred_prob = region/(gap_x * gap_y)
		return pred_prob

	# if there's bad input, it should raise an exception
	def bad_input_test(self):
		self.assertRaises(Exception, sims.CoinSim, 1, 1, 1, "while radius == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, 0, 1, "while gap_x == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, 1, 0, "while gap_y == 0, no exception was raised")

		self.assertRaises(Exception, sims.CoinSim, -1, 1, 1, "while radius < 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, -1, 1, "while gap_x < 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, 1, -1, "while gap_y < 0, no exception was raised")
		
		good_sim = sims.CoinSim(1, 1, 1)
		self.assertRaises(Exception, good_sim.run_trials, 0, "while trials == 0, no exception was raised")
		self.assertRaises(Exception, good_sim.run_trials, -1, "while trials < 0, no exception was raised")

	# if diameter >= gap_x or diameter >= gap_y, it should always hit
	def always_hit(self):
		for i in range(10):
			radius = 0
			while radius == 0:
				radius += random.random()
			diameter = radius*2

			more_gap = diameter
			while more_gap == diameter:
				more_gap += random.random()

			hits = sims.CoinSim(radius, diameter, more_gap).run_trials(TRIALS)
			self.assertEquals(hits, TRIALS, "while diameter == gap_x, coin does not always hit")

			hits = sims.CoinSim(radius, more_gap, diameter).run_trials(TRIALS)
			self.assertEquals(hits, TRIALS, "while diameter == gap_y, coin does not always hit")

		for i in range(10):
			radius = 0
			while radius == 0:
				radius = random.random()
			diameter = radius*2

			less_gap = diameter
			while less_gap == diameter:
				less_gap -= random.uniform(0.0, diameter)
			more_gap = diameter
			while more_gap == diameter:
				more_gap = diameter + random.random()

			hits = sims.CoinSim(radius, less_gap, more_gap).run_trials(TRIALS)
			self.assertEquals(hits, TRIALS, "while diameter > gap_x, coin does not always hit")

			hits = sims.CoinSim(radius, more_gap, less_gap).run_trials(TRIALS)
			self.assertEquals(hits, TRIALS, "while diameter > gap_y, coin does not always hit")

	# if diameter < gap_x and diameter < gap_y
	# average degree of freedom should be < MAX_DEGREE
	def is_match_theoretical(self):
		for i in range(10):
			gap_x = random.random()
			gap_y = random.random()
			diameter = random.uniform(0.0, min(gap_x, gap_y))
			radius = diameter/2

			hits = sims.CoinSim(radius, gap_x, gap_y).run_trials(TRIALS)
			pred_hits = self._predict_prob(radius, gap_x, gap_y)*TRIALS

			chi_squared = ((hits - pred_hits)**2)/pred_hits
			print("(%f, %f, %f) %d ~ %f, %f" % (radius, gap_x, gap_y, hits, pred_hits, chi_squared))
			assert(chi_squared >= 0)

			self.assertTrue(chi_squared < MAX_STAT, "while diameter < gap_x and diameter < gap_y, average chi^2 stat is %f >= %f" % (chi_squared, MAX_STAT))

	def runTest(self):
		self.bad_input_test()
		self.always_hit()
		self.is_match_theoretical()

if __name__ == '__main__':
	unittest.main()
