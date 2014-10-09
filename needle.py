#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Needle
Experiment.
"""

import sys

from utils import arghandle, config, graph, stepvals
from utils.sims import NeedleSim

def _get_prob(hits, trials):
    return float(hits)/trials

def plot_gap(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of the gap
    between the two parallel lines
    and the probability which the needle hits
    at least one of the lines.
    """

    vals = stepvals.get_range(args.gap, 1000)
    expected = []
    for gap in vals:
        sim = NeedleSim(args.length, gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected)

    vals = stepvals.get_range(args.gap, args.stepsize)
    for gap in vals:
        sim = NeedleSim(args.length, gap)
        prob = _get_prob(sim.run_trials(args.trials), args.trials)

        if args.verbose:
            print "length = %.5g, gap width = %.5g: %.5g" % (args.length, gap, prob)
        graph.scatter_plot(gap, prob)

    graph.scale_x_plot(args.gap, args.stepsize)
    graph.scale_y_plot(1.0, args.stepsize)
    graph.prepare_plot(
        "Gap width",
        "Probability of needle touching a line",
        u"Buffon’s Needle Experiment" +
            u"\nlength = %.5g" % args.length
    )

def plot_length(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the length of the
    needle and the probability which the needle
    hits at least one of the two parallel lines.
    """

    vals = stepvals.get_range(args.length, 1000)
    expected = []
    for length in vals:
        sim = NeedleSim(length, args.gap)
        expected.append(sim.predict_prob())

    graph.line_plot(vals, expected)

    vals = stepvals.get_range(args.length, args.stepsize)
    for length in vals:
        sim = NeedleSim(length, args.gap)
        prob = _get_prob(sim.run_trials(args.trials), args.trials)

        if args.verbose:
            print "length = %.5g, gap width = %.5g: %.5g" % (length, args.gap, prob)
        graph.scatter_plot(length, prob)

    graph.scale_x_plot(args.length, args.stepsize)
    graph.scale_y_plot(1.0, args.stepsize)
    graph.prepare_plot(
        "Length of needle",
        "Probability of needle touching a line",
        u"Buffon’s Needle Experiment" +
            u"\ngap width = %.5g" % args.gap
    )

MODES = {
    0: plot_gap,
    1: plot_length
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode 0: 2D scatter plot, gap width against probability of needle touching a line',
    'mode 1: 2D scatter plot, length of needle against probability of needle touching a line'
]

def _run_handler(args):
    sim = NeedleSim(args.length, args.gap)
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
    args = arghandle.get_args('needle', MODES, MODES_TXT)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args)

if __name__ == '__main__':
    main()
