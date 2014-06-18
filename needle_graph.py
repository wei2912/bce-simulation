#!/usr/bin/env python
# coding=utf-8

"""
This script plots different types of graphs
for Buffon's Needle Experiment.
"""

import argparse, math

import matplotlib.pyplot as plt

from utils import stepvals
from utils.sims import NeedleSim, NeedleAngleSim

def plot_length(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the length of the
    needle and the probability which the needle
    hits at least one of the two parallel lines.
    """

    vals = stepvals.get_range(args.length, args.stepsize)
    for length in vals:
        sim = NeedleSim(length, args.gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "length = %f, gap = %f: %f" % (length, args.gap, expprob)
        plt.scatter(length, expprob)

    plt.xlabel("Length of needle")
    plt.ylabel("P(E)")
    plt.title("Buffon's Needle Experiment - Length of needle against P(E)" +
        "\ngap = %f" % args.gap)
    plt.grid(True)

def plot_gap(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of the gap
    between the two parallel lines
    and the probability which the needle hits
    at least one of the lines.
    """

    vals = stepvals.get_range(args.gap, args.stepsize)
    for gap in vals:
        sim = NeedleSim(args.length, gap)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "length = %f, gap = %f: %f" % (args.length, gap, expprob)
        plt.scatter(gap, expprob)

    plt.xlabel("Gap length")
    plt.ylabel("P(E)")
    plt.title("Buffon's Needle Experiment - Gap width against P(E)" +
        "\nradius = %f" % args.radius)
    plt.grid(True)

def plot_angle(args):
    """
    Plots a 2D scatter plot which shows the
    relationship between the angle of a needle
    and the probability which the needle hits
    at least one of the two parallel lines.
    """

    vals = stepvals.get_range(math.pi, 1000)[:-1] # we don't want math.pi
    probs = []
    for angle in vals:
        sim = NeedleAngleSim(args.length, args.gap, angle)
        probs.append(sim.predict_prob())

    plt.plot(
        vals,
        probs,
        color='red',
        linewidth=2.0
    )

    vals = stepvals.get_range(math.pi, args.stepsize)[:-1]
    for angle in vals:
        sim = NeedleAngleSim(args.length, args.gap, angle)
        expprob = float(sim.run_trials(args.trials))/args.trials

        if args.verbose:
            print "length = %f, gap = %f, angle=%f: %f" % (args.length,
                args.gap, angle, expprob)
        plt.scatter(angle, expprob)

    plt.xlabel("Angle of needle (radians)")
    plt.ylabel("P(E)")
    plt.title("Buffon's Needle Experiment - Angle of needle against P(E)")
    plt.grid(True)

MODES = {
    0: plot_length,
    1: plot_gap,
    2: plot_angle
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode 0: 2D scatter plot, length of needle against P(E)',
    'mode 1: 2D scatter plot, gap width against P(E)'
    'mode 2: 2D scatter plot, angle of needle against P(E)'
]

def get_args():
    parser = argparse.ArgumentParser(
        description="Graph plotter for Buffon's Needle Experiment"
    )

    parser.add_argument(
        '-l',
        '--length',
        type=float,
        required=True,
        help='length of needle'
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
        '--stepsize',
        type=float,
        required=True,
        help='number of steps to take when increasing radius/gap'
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
