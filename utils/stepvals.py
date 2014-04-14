import math

def get_range(val, step):
	stepvals = [i*step for i in xrange(int(math.ceil(val/step)))][1:]
	if not stepvals[-1] == val: # if last element isn't the actual value
		stepvals += [val] # add it in
	return stepvals
