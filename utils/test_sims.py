import unittest
import random
import math

import sims

TRIALS = 1000 # number of trials to run per test case
MAX_DEGREE = 1.5 # max degree of freedom; refer to https://en.wikipedia.org/wiki/Pearson's_chi-squared_test

class TestCoinSim(unittest.TestCase):
	def runTest(self):
		# bad input
		self.assertRaises(Exception, sims.CoinSim, 0, 1, 1) # bad radius
		self.assertRaises(Exception, sims.CoinSim, -1, 1, 1) # bad radius
		self.assertRaises(Exception, sims.CoinSim, 1, 0, 1) # bad gap
		self.assertRaises(Exception, sims.CoinSim, 1, -1, 1) # bad gap
		self.assertRaises(Exception, sims.CoinSim, 1, 1, 0) # bad length
		self.assertRaises(Exception, sims.CoinSim, 1, 1, -1) # bad length

		# if radius*2 >= gap length, it should always hit
		hits = sims.CoinSim(1, 2, TRIALS).run_trials()
		self.assertEquals(hits, TRIALS, "while radius*2 == gap, coin does not always hit")

		hits = sims.CoinSim(1, 1.5, TRIALS).run_trials()
		self.assertEquals(hits, TRIALS, "while radius*2 > gap, coin does not always hit")

		degrees = []
		for i in range(1000):
			radius = random.random()
			gap = random.random()

			while radius*2 >= gap:
				radius = random.random()
				gap = random.random()

			# if radius*2 < gap length
			# average degree of freedom should be < MAX_DEGREE
			else:
				hits = sims.CoinSim(radius, gap, TRIALS).run_trials()
				pred_hits = self._predict_hits(radius, gap, TRIALS)

				# refer to https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
				# below equation was simplified after substituting original
				chi_squared = 2*((hits - pred_hits)**2)/pred_hits
				degrees.append(chi_squared)

		avg_degree = sum(degrees)/len(degrees)
		self.assertTrue(avg_degree < MAX_DEGREE, "while diameter < gap, average degree of freedom is %f > %f" % (avg_degree, MAX_DEGREE))

	def _predict_hits(self, radius, gap, trials):
		pred_hits = self._predict_prob(radius, gap)*trials
		return pred_hits

	def _predict_prob(self, radius, gap):
		pred_prob = float(radius*2)/gap
		if pred_prob > 1.0:
			return 1.0
		return pred_prob
		
if __name__ == '__main__':
	unittest.main()