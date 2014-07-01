#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Coin
Experiment (physics variant).
"""

import sys

from utils import arghandle, config, stepvals
from utils.sims import CoinPhysicsSim

OFFSET = 2 # offset = x/stepsize * OFFSET

def plot_width(plt, args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of a square gap
    and the probability which the coin hits and
    balances on the grid.
    """

    vals = stepvals.get_range(args.gap, 1000)
    probs = []
    for gap in vals:
        sim = CoinPhysicsSim(args.radius, gap)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(args.gap, args.stepsize)
    for gap in vals:
        sim = CoinPhysicsSim(args.radius, gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "radius = %.5g, gap = %.5g: %.5g" % (args.radius, gap, expprob)
        plt.scatter(gap, expprob)

    offset = args.gap/args.stepsize * OFFSET
    plt.axis(xmin=-offset, xmax=args.gap+offset, ymin=0)
    plt.xlabel("Width of square gap")
    plt.ylabel("P(E)")
    plt.title("Buffon's Coin Experiment (physics variant)" +
    	" - Width of square gap against P(E)" +
    	"\nradius = %.5g" % args.radius)
    plt.grid(True)

def plot_radius(plt, args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the radius of the coin
    and the probability which the coin hits and
    balances on the grid.
    """

    vals = stepvals.get_range(args.radius, 1000)
    probs = []
    for radius in vals:
        sim = CoinPhysicsSim(radius, args.gap)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(args.radius, args.stepsize)
    for radius in vals:
        sim = CoinPhysicsSim(radius, args.gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "radius = %.5g, gap = %.5g: %.5g" % (radius, args.gap, expprob)
        plt.scatter(radius, expprob)

    offset = args.radius/args.stepsize * OFFSET
    plt.axis(xmin=-offset, xmax=args.radius+offset, ymin=0)
    plt.xlabel("Radius")
    plt.ylabel("P(E)")
    plt.title("Buffon's Coin Experiment (physics variant)" +
    	" - Radius against P(E)" +
    	"\nwidth of square gap = %.5g" % args.gap)
    plt.grid(True)

MODES = {
    0: plot_width,
    1: plot_radius
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode 0: 2D scatter plot, width of square gap against P(E)',
    'mode 1: 2D scatter plot, radius against P(E)'
]

def _run_handler(args):
    sim = CoinPhysicsSim(args.radius, args.gap)
    hits = sim.run_trials(args.trials)

    print("%d/%d" % (hits, args.trials))
    prob = float(hits)/args.trials
    print("observed prob: %f" % prob)
    print("expected prob: %f" % sim.predict_prob())

def _plot_handler(args):
    output = args.output
    stdout = output == 'stdout'

    import matplotlib
    config.mpl(matplotlib, stdout=stdout)
    import matplotlib.pyplot as plt

    MODES[args.mode](plt, args)

    if output:
        if stdout:
            plt.savefig(sys.stdout, format='png')
        else:
            plt.savefig(output)
    else:
        plt.show()

def main():
    args = arghandle.get_args('coin_phy', MODES, MODES_TXT)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args)

main()
