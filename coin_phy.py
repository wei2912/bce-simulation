#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Coin
Experiment.
"""

import sys

from utils import arghandle, coin_phy, graph, misc

def plot_diameter(d, w, trials):
    """
    Plots a 2D scatter plot which shows the
    relationship between the diameter of the coin
    and the probability which the coin hits the grid.

    d = diameter of coin
    w = width of gap
    """

    xs = list(graph.get_range(d))

    ys = coin_phy.predict_prob(xs, w)
    graph.line_plot(xs, ys)

    for x in xs:
        y = float(coin_phy.run_trials(x, w, trials))/trials
        graph.scatter_plot(x, y)

    graph.scale_x_plot(d)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
    	"Diameter",
    	"Probability of coin touching the grid",
    	u"Buffon’s Coin Experiment" +
    	    u"\nwidth of square gap = %.5g" % w
    )

def plot_width(d, w, trials):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of a square gap
    and the probability which the coin hits the grid.

    d = diameter of coin
    w = width of gap
    """

    xs = list(graph.get_range(w))

    ys = coin_phy.predict_prob(d, xs)
    graph.line_plot(xs, ys)

    for x in xs:
	y = float(coin_phy.run_trials(d, x, trials))/trials
	graph.scatter_plot(x, y)

    graph.scale_x_plot(w)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
    	"Width of square gap",
    	"Probability of coin touching the grid",
    	u"Buffon’s Coin Experiment" +
    		u"\ndiameter = %.5g" % d
    )

MODES = {
    'l': plot_diameter,
    'w': plot_width
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode l: varying diameter of coin',
    'mode w: varying width of gap',
]

def _run_handler(args):
    hits = coin_phy.run_trials(args.diameter, args.gap, args.trials)

    print("%d/%d" % (hits, args.trials))
    prob = misc.get_prob(hits, args.trials)
    print("observed prob: %f" % prob)
    print("expected prob: %f" % coin_phy.predict_prob(args.diameter, args.gap))

def _plot_handler(args):
    graph.init(args.output)

    d = misc.validate_diameter(args.diameter)
    w = misc.validate_width(args.gap)
    trials = misc.validate_trials(args.trials)

    MODES[args.mode](d, w, trials)

    graph.display_plot(args.output)

def main():
    args = arghandle.get_args('coin', MODES, MODES_TXT)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args)

if __name__ == '__main__':
    main()
