"""
This module serves as an interface to
matplotlib.
"""

from utils import config

OFFSET = 2 # offset = max_x/stepsize * OFFSET

def init(output):
    import matplotlib
    config.mpl(matplotlib, bool(output))
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

def scale_x_plot(max_x, stepsize):
    offset = max_x/stepsize * OFFSET
    plt.axis(xmin=-offset, xmax=max_x+offset)

def scale_y_plot(max_y, stepsize):
    offset = max_y/stepsize * OFFSET
    plt.axis(ymin=-offset, ymax=max_y+offset)

def prepare_plot(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

def display_plot(output):
    if output:
        if output == 'stdout':
            plt.savefig(sys.stdout, format='png')
        else:
            plt.savefig(output)
    else:
        plt.show()
