import unittest
import random
import math

import sims

TRIALS = 1000 # number of trials to run per test case
MAX_DEGREE = 1.5 # max degree of freedom; refer to https://en.wikipedia.org/wiki/Pearson's_chi-squared_test

class TestCoinSim(unittest.TestCase):
	def _predict_hits(self, radius, gap, trials):
		pred_hits = self._predict_prob(radius, gap)*trials
		return pred_hits

	def _predict_prob(self, radius, gap):
		region = radius*2 # area of region which coin would hit
		pred_prob = region/gap
		if pred_prob > 1.0:
			return 1.0
		return pred_prob	

	# if there's bad input, it should raise an exception
	def bad_input_test(self):
		self.assertRaises(Exception, sims.CoinSim, 0, 1, 1, "while radius == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, 0, 1, "while gap == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, 1, 0, "while length == 0, no exception was raised")

		self.assertRaises(Exception, sims.CoinSim, -1, 1, 1, "while radius > 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, -1, 1, "while gap > 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinSim, 1, 1, -1, "while length > 0, no exception was raised")

	# if diameter >= gap length, it should always hit
	def always_hit(self):
		for i in range(1000):
			radius = 0
			while radius == 0:
				radius = random.random()

			hits = sims.CoinSim(radius, radius*2, TRIALS).run_trials()
			self.assertEquals(hits, TRIALS, "while diameter == gap, coin does not always hit")

		for i in range(1000):
			radius = 0
			while radius == 0:
				radius = random.random()

			gap = radius*2
			while gap >= radius*2 or gap < 0:
				gap = radius*2 - random.random()

			hits = sims.CoinSim(radius, gap, TRIALS).run_trials()
			self.assertEquals(hits, TRIALS, "while diameter > gap, coin does not always hit")

	# if diameter < gap length
	# average degree of freedom should be < MAX_DEGREE
	def is_uniform_random(self):
		degrees = []
		for i in range(1000):
			radius = random.random()
			gap = random.random()

			while radius*2 >= gap:
				radius = random.random()
				gap = random.random()

			hits = sims.CoinSim(radius, gap, TRIALS).run_trials()
			pred_hits = self._predict_hits(radius, gap, TRIALS)

			# refer to https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
			# below equation was simplified after substituting original
			chi_squared = 2*((hits - pred_hits)**2)/pred_hits
			degrees.append(chi_squared)

		avg_degree = sum(degrees)/len(degrees)
		self.assertTrue(avg_degree < MAX_DEGREE, "while diameter < gap, average degree of freedom is %f > %f" % (avg_degree, MAX_DEGREE))

	def runTest(self):
		self.bad_input_test()
		self.always_hit()
		self.is_uniform_random()

class TestCoinGridSim(unittest.TestCase):
	def _predict_hits(self, radius, gap_x, gap_y, trials):
		pred_hits = self._predict_prob(radius, gap_x, gap_y)*trials
		return pred_hits

	def _predict_prob(self, radius, gap_x, gap_y):
		region = gap_x*gap_y - (gap_x-radius*2)*(gap_y-radius*2) # area of region which coin would hit
		pred_prob = region/(gap_x * gap_y)
		if pred_prob > 1.0:
			return 1.0
		return pred_prob	

	# if there's bad input, it should raise an exception
	def bad_input_test(self):
		self.assertRaises(Exception, sims.CoinGridSim, 0, 1, 1, 1, "while radius == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinGridSim, 1, 0, 1, 1, "while gap_x == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinGridSim, 1, 1, 0, 1, "while gap_y == 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinGridSim, 1, 1, 1, 0, "while length == 0, no exception was raised")

		self.assertRaises(Exception, sims.CoinGridSim, -1, 1, 1, 1, "while radius < 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinGridSim, 1, -1, 1, 1, "while gap_x < 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinGridSim, 1, 1, -1, 1, "while gap_y < 0, no exception was raised")
		self.assertRaises(Exception, sims.CoinGridSim, 1, 1, 1, -1, "while length < 0, no exception was raised")

	# if diameter >= gap_x or diameter >= gap_y, it should always hit
	def always_hit(self):
		for i in range(1000):
			radius = 0
			while radius == 0:
				radius = random.random()

			more_gap = radius*2
			while more_gap == radius*2:
				more_gap = radius*2 + random.random()

			hits = sims.CoinGridSim(radius, radius*2, more_gap, TRIALS).run_trials()
			self.assertEquals(hits, TRIALS, "while diameter == gap_x, coin does not always hit")

			hits = sims.CoinGridSim(radius, more_gap, radius*2, TRIALS).run_trials()
			self.assertEquals(hits, TRIALS, "while diameter == gap_y, coin does not always hit")

		for i in range(1000):
			radius = 0
			while radius == 0:
				radius = random.random()

			less_gap = radius*2
			while less_gap >= radius*2 or less_gap < 0:
				less_gap = radius*2 - random.random()
			more_gap = radius*2
			while more_gap == radius*2:
				more_gap = radius*2 + random.random()

			hits = sims.CoinGridSim(radius, less_gap, more_gap, TRIALS).run_trials()
			self.assertEquals(hits, TRIALS, "while diameter> gap_x, coin does not always hit")

			hits = sims.CoinGridSim(radius, more_gap, less_gap, TRIALS).run_trials()
			self.assertEquals(hits, TRIALS, "while diameter > gap_y, coin does not always hit")

	# if diameter < gap_x and diameter < gap_y
	# average degree of freedom should be < MAX_DEGREE
	def is_uniform_random(self):
		degrees = []
		for i in range(1000):
			radius = random.random()
			gap_x = random.random()
			gap_y = random.random()

			while radius*2 >= gap_x or radius*2 >= gap_y:
				radius = random.random()
				gap_x = random.random()
				gap_y = random.random()

			hits = sims.CoinGridSim(radius, gap_x, gap_y, TRIALS).run_trials()
			pred_hits = self._predict_hits(radius, gap_x, gap_y, TRIALS)

			# refer to https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
			# below equation was simplified after substituting original
			chi_squared = 2*((hits - pred_hits)**2)/pred_hits
			degrees.append(chi_squared)

		avg_degree = sum(degrees)/len(degrees)
		self.assertTrue(avg_degree < MAX_DEGREE, "while diameter < gap_x and diameter < gap_y, average degree of freedom is %f > %f" % (avg_degree, MAX_DEGREE))

	def runTest(self):
		self.bad_input_test()
		self.always_hit()
		self.is_uniform_random()

if __name__ == '__main__':
	unittest.main()