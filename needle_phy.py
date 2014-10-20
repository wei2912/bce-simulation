#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Needle
Experiment.
"""

from utils import arghandle, graph, misc
from utils import needle_phy

def plot_gap(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of the gap
    between the two parallel lines
    and the probability which the needle hits
    at least one of the lines.
    """

    vals = []
    expected = []
    for gap in graph.get_range(args.gap):
        vals.append(gap)
        expected.append(needle_phy.predict_prob(args.length, gap))

        trials = needle_phy.run_trials(args.length, gap, args.trials)
        prob = misc.get_prob(trials, args.trials)

        graph.scatter_plot(gap, prob)

    graph.line_plot(vals, expected)

    graph.scale_x_plot(args.gap)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
        u"Gap width",
        u"Probability of needle touching a line",
        u"Buffon’s Needle Experiment (a variation)" +
            u"\nlength = %.5g" % args.length
    )

def plot_length(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the length of the
    needle and the probability which the needle
    hits at least one of the two parallel lines.
    """

    vals = []
    expected = []
    for length in graph.get_range(args.length):
        vals.append(length)
        expected.append(needle_phy.predict_prob(length, args.gap))

        trials = needle_phy.run_trials(length, args.gap, args.trials)
        prob = misc.get_prob(trials, args.trials)

        graph.scatter_plot(length, prob)

    graph.line_plot(vals, expected)

    graph.scale_x_plot(args.length)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
        u"Length of needle",
        u"Probability of needle touching a line",
        u"Buffon’s Needle Experiment (a variation)" +
            u"\ngap width = %.5g" % args.gap
    )

MODES = {
    'l': plot_length,
    'w': plot_gap
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode l: 2D scatter plot, length of needle against probability of needle touching a line',
    'mode w: 2D scatter plot, gap width against probability of needle touching a line'
]

def _run_handler(args):
    hits = needle_phy.run_trials(args.length, args.gap, args.trials)

    print("%d/%d" % (hits, args.trials))
    prob = misc.get_prob(hits, args.trials)
    print("observed prob: %f" % prob)
    print("expected prob: %f" % needle_phy.predict_prob(args.length, args.gap))

def _plot_handler(args):
    output = args.output
    graph.init(output)
    MODES[args.mode](args)
    graph.display_plot(output)

def main():
    args = arghandle.get_args('needle_phy', MODES, MODES_TXT)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args)

if __name__ == '__main__':
    main()
