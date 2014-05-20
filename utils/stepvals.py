import math

def get_range(val, step):
	if step >= val:
		raise Exception("Step value is too large! Must be smaller than value.")

	stepvals = [i*step for i in xrange(int(math.ceil(val/step)))][1:]
	if not stepvals[-1] == val: # if last element isn't the actual value
		stepvals += [val] # add it in
	return stepvals
