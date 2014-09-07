"""
This module serves as an interface to
matplotlib.
"""

import math

import numpy as np

from utils import misc

STEPSIZE = 100
OFFSET = 2 # offset = max_x/stepsize * OFFSET

def init(output):
    import matplotlib

    if bool(output):
	matplotlib.use('Agg')
    matplotlib.rc('savefig', dpi=150)

    from matplotlib import pyplot
    globals()['plt'] = pyplot

def line_plot(xs, ys, color='red'):
	plt.plot(
        xs,
        ys,
        color=color,
        linewidth=2.0
    )

def legend(*args):
    plt.legend(args, loc='best')

def scatter_plot(x, y, color='blue'):
	plt.scatter(x, y, color=color)

def scale_x_plot(max_x):
    offset = max_x/STEPSIZE * OFFSET
    plt.axis(xmin=-offset, xmax=max_x+offset)

def scale_y_plot(max_y):
    offset = max_y/STEPSIZE * OFFSET
    plt.axis(ymin=-offset, ymax=max_y+offset)

def prepare_plot(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

def display_plot(output):
    if output:
        plt.savefig(output)
    else:
        plt.show()

def get_range(val):
    """
    This function will return a range of values
    given the size of the range.

    For a value of 100.0 with a size of 10,
    the following range is yielded:

    [10.0, 20.0, 30.0, ..., 100.0]
    """
    i = 1
    while i < STEPSIZE+1:
	yield i*(val/STEPSIZE)
	i += 1
