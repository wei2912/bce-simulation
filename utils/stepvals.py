"""
This module is used to generate step values.

Refer to function `get_range` for more details.
"""

import math
import unittest

def get_range(val, step):
    """
    This function will return a range of values.

    For a value of 100.0 with a step value of 10.0,
    the following range is generated:

    [10.0, 20.0, 30.0, ..., 100.0]

    In the scenario where the last number of the range is
    not the actual value itself, the function will
    append the value onto the range.
    """

    if step >= val:
        raise Exception("Step value is too large! Must be smaller than value.")

    stepvals = [i*step for i in xrange(int(math.ceil(val/step)))][1:]
    if not stepvals[-1] == val: # if last element isn't the actual value
        stepvals += [val] # add it in
    return stepvals

if __name__ == '__main__':
    unittest.main()
    import doctest
    doctest.testmod()
