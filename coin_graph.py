#!/usr/bin/env python
# coding=utf-8

"""
This script plots different types of graphs
for Buffon's Coin Experiment.
"""

import argparse

import matplotlib.pyplot as plt

from utils import stepvals
from utils.sims import CoinSim

def plot_width(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of a square gap
    and the probability which the coin hits the grid.
    """

    vals = stepvals.get_range(args.gap, 0.001)
    probs = []
    for gap in vals:
        sim = CoinSim(args.radius, gap, gap)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(args.gap, args.step)
    for gap in vals:
        sim = CoinSim(args.radius, gap, gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "radius = %f, gap = %f: %f" % (args.radius, gap, expprob)
        plt.scatter(gap, expprob)

    plt.xlabel("Width of square gap")
    plt.ylabel("P(E)")
    plt.title("Buffon's Coin Experiment - Width of square gap against P(E)" +
    	"\nradius = %f" % args.radius)
    plt.grid(True)

def plot_radius(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the radius of the coin
    and the probability which the coin hits the grid.
    """

    vals = stepvals.get_range(args.radius, 0.001)
    probs = []
    for radius in vals:
        sim = CoinSim(radius, args.gap, args.gap)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(args.radius, args.step)
    for radius in vals:
        sim = CoinSim(radius, args.gap, args.gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "radius = %f, gap = %f: %f" % (radius, args.gap, expprob)
        plt.scatter(radius, expprob)

    plt.xlabel("Radius")
    plt.ylabel("P(E)")
    plt.title("Buffon's Coin Experiment - Radius against P(E)" +
    	"\nwidth of square gap = %f" % args.gap)
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

def get_args():
    parser = argparse.ArgumentParser(
        description="Graph plotter for Buffon's Coin Experiment"
    )

    parser.add_argument(
        '-r',
        '--radius',
        type=float,
        required=True,
        help='max radius of coin'
    )

    parser.add_argument(
        '-g',
        '--gap',
        type=float,
        required=True,
        help='max width of square gap'
    )

    parser.add_argument(
        '-t',
        '--trials',
        type=int,
        default=1000,
        help='number of trials to run'
    )

    parser.add_argument(
        '-s',
        '--step',
        type=float,
        required=True,
        help='step to take when increasing radius/gap'
    )

    parser.add_argument(
        '-o',
        '--output',
        help='filename to output graph to'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='enable verbose output'
    )

    parser.add_argument(
        '-m',
        '--mode',
        type=int,
        choices=[i for i in MODES],
        required=True,
        help="\n".join(MODES_TXT)
    )

    return parser.parse_args()

def main():
    args = get_args()
    MODES[args.mode](args)

    if args.output:
        plt.savefig(args.output)
    else:
        plt.show()

main()
