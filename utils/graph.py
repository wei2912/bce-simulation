"""
This module serves as an interface to
matplotlib.
"""

import matplotlib
import matplotlib.pyplot as plt
from utils import config

OFFSET = 2 # offset = max_x/stepsize * OFFSET

def line_plot(xs, ys):
	plt.plot(
        xs,
        ys,
        color='red',
        linewidth=2.0
    )

def scatter_plot(x, y):
	plt.scatter(x, y)

def scale_plot(max_x, stepsize):
    offset = max_x/stepsize * OFFSET
    plt.axis(xmin=-offset, xmax=max_x+offset, ymin=0)

def prepare_plot(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

def display_plot(output):
    config.mpl(matplotlib, bool(output))

    if output:
        if output == 'stdout':
            plt.savefig(sys.stdout, format='png')
        else:
            plt.savefig(output)
    else:
        plt.show()
