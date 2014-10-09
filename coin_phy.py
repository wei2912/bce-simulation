#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Coin
Experiment (physics variant).
"""

import sys

from utils import arghandle, config, graph, stepvals
from utils.sims import CoinPhysicsSim

def _get_prob(hits, trials):
    return float(hits)/trials

def plot_width(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of a square gap
    and the probability which the coin hits the grid.
    """

    vals = stepvals.get_range(args.gap, 1000)
    expected = []
    for gap in vals:
        sim = CoinPhysicsSim(args.diameter, gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected)

    vals = stepvals.get_range(args.gap, args.stepsize)
    for gap in vals:
        sim = CoinPhysicsSim(args.diameter, gap)
        prob = _get_prob(sim.run_trials(args.trials), args.trials)

        if args.verbose:
            print "diameter = %.5g, gap width = %.5g: %.5g" % (args.diameter, gap, prob)
        graph.scatter_plot(gap, prob)

    graph.scale_x_plot(args.gap, args.stepsize)
    graph.scale_y_plot(1.0, args.stepsize)
    graph.prepare_plot(
        "Width of square gap",
        "Probability of coin balancing on grid",
        u"Buffon’s Coin Experiment (a variation)" +
            u"\ndiameter = %.5g" % args.diameter
    )

def plot_diameter(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the diameter of the coin
    and the probability which the coin hits the grid.
    """

    vals = stepvals.get_range(args.diameter, 1000)
    expected = []
    for diameter in vals:
        sim = CoinPhysicsSim(diameter, args.gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected)

    vals = stepvals.get_range(args.diameter, args.stepsize)
    for diameter in vals:
        sim = CoinPhysicsSim(diameter, args.gap)
        prob = _get_prob(sim.run_trials(args.trials), args.trials)

        if args.verbose:
            print "diameter = %.5g, gap width = %.5g: %.5g" % (diameter, args.gap, prob)
        graph.scatter_plot(diameter, prob)

    graph.scale_x_plot(args.diameter, args.stepsize)
    graph.scale_y_plot(1.0, args.stepsize)
    graph.prepare_plot(
        "Diameter",
        "Probability of coin balancing on grid",
        u"Buffon’s Coin Experiment (a variation)" +
            u"\nwidth of square gap = %.5g" % args.gap
    )

MODES = {
    0: plot_width,
    1: plot_diameter
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode 0: 2D scatter plot, width of square gap against probability of coin balancing on grid',
    'mode 1: 2D scatter plot, diameter against probability of coin balancing on grid'
]

def _run_handler(args):
    sim = CoinPhysicsSim(args.diameter, args.gap)
    hits = sim.run_trials(args.trials)

    print("%d/%d" % (hits, args.trials))
    prob = _get_prob(hits, args.trials)
    print("observed prob: %f" % prob)
    print("expected prob: %f" % sim.predict_prob())

def _plot_handler(args):
    output = args.output
    graph.init(output)
    MODES[args.mode](args)
    graph.display_plot(output)

def main():
    args = arghandle.get_args('coin_phy', MODES, MODES_TXT)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args)

if __name__ == '__main__':
    main()
