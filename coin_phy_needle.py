#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Coin
Experiment (physics variant).
"""

import sys
import numpy as np

from utils import arghandle, config, graph, stepvals
from utils.sims import CoinSim, CoinPhysicsSim, NeedleSim

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
        sim = NeedleSim(args.diameter, gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected)

    expected = []
    for gap in vals:
        sim = CoinSim(args.diameter/2, gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected, color='green')

    expected = []
    for gap in vals:
        sim = CoinPhysicsSim(args.diameter/2, gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected, color='blue')

    graph.legend("Needle", "Coin", "Coin (Physics)")
    graph.scale_plot(args.gap, args.stepsize)
    graph.prepare_plot(
        "Width of gap",
        "Probability of coin/needle balancing on grid",
        "Comparison of the 3 experiments" +
            "\nlength/diameter = %.5g" % args.diameter
    )

def plot_diameter(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the radius of the coin
    and the probability which the coin hits the grid.
    """

    vals = stepvals.get_range(args.diameter, 1000)
    expected = []
    for diameter in vals:
        sim = NeedleSim(diameter, args.gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected)

    expected = []
    for diameter in vals:
        sim = CoinSim(diameter/2, args.gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected, color='green')

    expected = []
    for diameter in vals:
        sim = CoinPhysicsSim(diameter/2, args.gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected, color='blue')

    graph.legend("Needle", "Coin", "Coin (Physics)")

    graph.scale_plot(args.diameter, args.stepsize)
    graph.prepare_plot(
        "Length/Diameter",
        "Probability of coin/needle balancing on grid",
        "Comparison of the 3 experiments" +
            "\nwidth of square gap = %.5g" % args.gap
    )

MODES = {
    0: plot_width,
    1: plot_diameter
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode 0: 2D scatter plot, width of square gap against Probability',
    'mode 1: 2D scatter plot, radius against Probability'
]

def _plot_handler(args):
    output = args.output
    graph.init(output)
    MODES[args.mode](args)
    graph.display_plot(output)

def main():
    args = arghandle.get_args('coin_phy_needle', MODES, MODES_TXT)
    _plot_handler(args)

if __name__ == '__main__':
    main()
