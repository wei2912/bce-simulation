#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Needle
Experiment.
"""

import sys

import matplotlib.pyplot as plt

from utils import arghandle, stepvals
from utils.sims import NeedleSim

def plot_length(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the length of the
    needle and the probability which the needle
    hits at least one of the two parallel lines.
    """

    vals = stepvals.get_range(args.length, 1000)
    probs = []
    for length in vals:
        sim = NeedleSim(length, args.gap)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(args.length, args.stepsize)
    for length in vals:
        sim = NeedleSim(length, args.gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "length = %.5g, gap = %.5g: %.5g" % (length, args.gap, expprob)
        plt.scatter(length, expprob)

    plt.axis(xmin=-1, xmax=args.length+1, ymin=0)
    plt.xlabel("Length of needle")
    plt.ylabel("P(E)")
    plt.title("Buffon's Needle Experiment - Length of needle against P(E)" +
        "\ngap = %.5g" % args.gap)
    plt.grid(True)

def plot_gap(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of the gap
    between the two parallel lines
    and the probability which the needle hits
    at least one of the lines.
    """

    vals = stepvals.get_range(args.gap, 1000)
    probs = []
    for gap in vals:
        sim = NeedleSim(args.length, gap)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(args.gap, args.stepsize)
    for gap in vals:
        sim = NeedleSim(args.length, gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "length = %.5g, gap = %.5g: %.5g" % (args.length, gap, expprob)
        plt.scatter(gap, expprob)

    plt.axis(xmin=-1, xmax=args.gap+1, ymin=0)
    plt.xlabel("Gap length")
    plt.ylabel("P(E)")
    plt.title("Buffon's Needle Experiment - Gap width against P(E)" +
        "\nlength = %.5g" % args.length)
    plt.grid(True)

MODES = {
    0: plot_length,
    1: plot_gap
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode 0: 2D scatter plot, length of needle against P(E)',
    'mode 1: 2D scatter plot, gap width against P(E)'
]

def _run_handler(args):
    sim = NeedleSim(args.length, args.gap)
    hits = sim.run_trials(args.trials)

    print("%d/%d" % (hits, args.trials))
    prob = float(hits)/args.trials
    print("observed prob: %f" % prob)
    print("expected prob: %f" % sim.predict_prob())

def _plot_handler(args):
    MODES[args.mode](args)

    if args.output:
        if args.output == 'stdout':
            plt.savefig(sys.stdout)
        else:
            plt.savefig(args.output)
    else:
        plt.show()

def main():
    args = arghandle.get_args('needle', MODES, MODES_TXT)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args)

main()
