import unittest
import math
import random

from scipy.stats.mstats import chisquare

import sims

TRIALS = 10000 # number of trials to run per test case
MAX_STAT = 3.841

# random function without zero
def non_zero_rand():
	return 1.0 - random.random()

class TestCoinSim(unittest.TestCase):
	# if there's bad input, it should raise an exception
	def bad_input_test(self):
		### note ###
		# for programmer, if something goes wrong here
		# add "print(i)" to see which variable it is
		############

		for i in range(3):
			vals = [1, 1, 1]

			vals[i] = 0
			self.assertRaises(sims.InvalidInput, sims.CoinSim, vals[0], vals[1], vals[2])

			vals[i] = -1
			self.assertRaises(sims.InvalidInput, sims.CoinSim, vals[0], vals[1], vals[2])

		good_sim = sims.CoinSim(1, 1, 1)
		self.assertRaises(sims.InvalidInput, good_sim.run_trials, 0)
		self.assertRaises(sims.InvalidInput, good_sim.run_trials, -1)

	# if diameter >= gap_x or diameter >= gap_y, it should always hit
	def always_hit(self):
		for i in range(10):
			radius = 1.0 - non_zero_rand()
			diameter = radius*2
			more_gap = diameter + non_zero_rand()
			less_gap = diameter - non_zero_rand()*diameter

			pairs = [
				(diameter, more_gap),
				(more_gap, diameter),
				(diameter, less_gap),
				(less_gap, diameter),
				(less_gap, more_gap),
				(more_gap, less_gap),
				(less_gap, less_gap)
			]

			for pair in pairs:
				hits = sims.CoinSim(radius, pair[0], pair[1]).run_trials(TRIALS)
				self.assertEquals(hits, TRIALS, "coin does not always hit")

	# if diameter < gap_x and diameter < gap_y
	# chi^2 statistic should be < MAX_DEGREE
	def is_match_theoretical(self):
		for i in range(10):
			gap_x = non_zero_rand()
			gap_y = non_zero_rand()
			diameter = non_zero_rand() * min(gap_x, gap_y)
			radius = diameter/2

			sim = sims.CoinSim(radius, gap_x, gap_y)

			hits = sim.run_trials(TRIALS)
			pred_hits = sim.predict_hits(TRIALS)

			stats = [
				(hits-pred_hits)**2/pred_hits,
				(pred_hits-hits)**2/(TRIALS-pred_hits)
			]
			chi2 = sum(stats)/len(stats)

			print("")
			print("hits:       %d ~ %f: %f" % (hits, pred_hits, stats[0]))
			print("non-hits:   %d ~ %f: %f" % (TRIALS-hits, TRIALS-pred_hits, stats[1]))
			print("sum:        %f" % sum(stats))
			print("chi-square: %f" % chi2)
			
			self.assertTrue(chi2 < MAX_STAT, "chi-square = %f >= %f" % (chi2, MAX_STAT))

	def runTest(self):
		self.bad_input_test()
		self.always_hit()
		self.is_match_theoretical()

class TestNeedleSim(unittest.TestCase):
	# if there's bad input, it should raise an exception
	def bad_input_test(self):
		### note ###
		# for programmer, if something goes wrong here
		# add "print(i)" to see which variable it is
		############

		for i in range(2):
			vals = [1, 1]

			vals[i] = 0
			self.assertRaises(sims.InvalidInput, sims.NeedleSim, vals[0], vals[1])

			vals[i] = -1
			self.assertRaises(sims.InvalidInput, sims.NeedleSim, vals[0], vals[1])

		good_sim = sims.NeedleSim(1, 1)
		self.assertRaises(sims.InvalidInput, good_sim.run_trials, 0)
		self.assertRaises(sims.InvalidInput, good_sim.run_trials, -1)

	def runTest(self):
		self.bad_input_test()

class TestNeedleAngleSim(unittest.TestCase):
	# if there's bad input, it should raise an exception
	def bad_input_test(self):
		### note ###
		# for programmer, if something goes wrong here
		# add "print(i)" to see which variable it is
		############

		for i in range(3):
			vals = [1, 1, 0.1]

			vals[i] = 0
			self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, vals[0], vals[1], vals[2])

			vals[i] = -1
			self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, vals[0], vals[1], vals[2])

			if i == 2: # is angle
				vals[i] = math.pi
				self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, vals[0], vals[1], vals[2])

				vals[i] = math.pi+non_zero_rand()
				self.assertRaises(sims.InvalidInput, sims.NeedleAngleSim, vals[0], vals[1], vals[2])

		good_sim = sims.NeedleAngleSim(1, 1, 0.1)
		self.assertRaises(sims.InvalidInput, good_sim.run_trials, 0)
		self.assertRaises(sims.InvalidInput, good_sim.run_trials, -1)

	# if opposite >= gap, it should always hit
	def always_hit(self):
		for i in range(10):
			# normally in the case of angles we would consider 0 radians
			# however in this case 0 radians would mean it is impossible
			# for the needle to have a non-zero opposite
			angle = non_zero_rand()*math.pi

			opp = non_zero_rand()
			length = opp/math.sin(angle)

			less_gap = opp - non_zero_rand()*opp

			hits = sims.NeedleAngleSim(length, less_gap, angle).run_trials(TRIALS)
			self.assertEquals(hits, TRIALS, "needle does not always hit")

	# if opposite < gap
	# chi^2 statistic should be < MAX_DEGREE
	def is_match_theoretical(self):
		for i in range(10):
			angle = random.uniform(0.0, math.pi)
			length = non_zero_rand()
			opp = length * math.sin(angle)
			gap = opp + non_zero_rand()

			sim = sims.NeedleAngleSim(length, gap, angle)

			hits = sim.run_trials(TRIALS)
			pred_hits = sim.predict_hits(TRIALS)

			stats = [
				(hits-pred_hits)**2/pred_hits,
				(pred_hits-hits)**2/(TRIALS-pred_hits)
			]
			chi2 = sum(stats)/len(stats)

			print("")
			print("hits:       %d ~ %f: %f" % (hits, pred_hits, stats[0]))
			print("non-hits:   %d ~ %f: %f" % (TRIALS-hits, TRIALS-pred_hits, stats[1]))
			print("sum:        %f" % sum(stats))
			print("chi-square: %f" % chi2)
			
			self.assertTrue(chi2 < MAX_STAT, "chi-square = %f >= %f" % (chi2, MAX_STAT))

	def runTest(self):
		self.bad_input_test()
		self.always_hit()
		self.is_match_theoretical()

if __name__ == '__main__':
	unittest.main()
