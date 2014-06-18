"""
This module is used to generate step values.

Refer to function `get_range` for more details.
"""

import math

def get_range(val, size):
    """
    This function will return a range of values
    given a step size.

    For a value of 100.0 with a step size of 10,
    the following range is generated:

    [10.0, 20.0, 30.0, ..., 100.0]

    In the scenario where the last number of the range is
    not the actual value itself, the function will
    append the value onto the range.
    """

    stepvals = [i*(val/size) for i in xrange(1, size+1)]
    if not stepvals[-1] == val: # if last element isn't the actual value
        stepvals += [val] # add it in
    return stepvals
