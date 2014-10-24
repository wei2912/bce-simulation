#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of Buffon's Coin
Experiment.
"""

import sys

from utils import arghandle, graph, misc, SIMULATIONS

GRAPH_CAPTIONS = {
    'coin': {
        'l': [
            u"Diameter",
            u"Probability of coin touching the grid",
            u"Buffon’s Coin Experiment\nwidth of square gap = %.5g"
        ],
        'w': [
            u"Width of square gap",
            u"Probability of coin touching the grid",
            u"Buffon’s Coin Experiment\ndiameter = %.5g"
        ]
    },
    'coin_phy': {
        'l': [
            u"Diameter",
            u"Probability of coin balancing on the grid",
            u"Buffon’s Coin Experiment (a variation)\nwidth of square gap = %.5g"
        ],
        'w': [
            u"Width of square gap",
            u"Probability of coin balancing on the grid",
            u"Buffon’s Coin Experiment (a variation)\ndiameter = %.5g"
        ]
    }
}

def plot_length(l, w, trials, simulation):
    xs = list(graph.get_range(l))

    ys = simulation.predict_prob(xs, w)
    graph.line_plot(xs, ys)

    for x in xs:
        y = float(simulation.run_trials(x, w, trials))/trials
        graph.scatter_plot(x, y)

    graph.scale_x_plot(l)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
        caption[0],
        caption[1],
        caption[2] % w
    )

def plot_width(l, w, trials, simulation):
    xs = list(graph.get_range(w))

    ys = simulation.predict_prob(l, xs)
    graph.line_plot(xs, ys)

    for x in xs:
        y = float(simulation.run_trials(l, x, trials))/trials
        graph.scatter_plot(x, y)

    graph.scale_x_plot(w)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
        caption[0],
        caption[1],
        caption[2] % l
    )

MODES = {
    'l': plot_length,
    'w': plot_width
}

def _run_handler(args, experiment):
    simulation = SIMULATIONS[experiment]
    argument = args.diameter if 'diameter' in args else args.length

    hits = simulation.run_trials(argument, args.gap, args.trials)

    print("%d/%d" % (hits, args.trials))
    prob = misc.get_prob(hits, args.trials)
    print("observed prob: %f" % prob)
    print("expected prob: %f" % simulation.predict_prob(argument, args.gap))

def _plot_handler(args, experiment):
    simulation = SIMULATIONS[experiment]
    argument = args.diameter if 'diameter' in args else args.length

    graph.init(args.output)

    d = misc.validate_diameter(argument)
    w = misc.validate_width(args.gap)
    trials = misc.validate_trials(args.trials)

    MODES[args.mode](d, w, trials, simulation)

    graph.display_plot(args.output)

def main():
    args = arghandle.get_args(MODES)
    experiment = args.experiment
    print(args)

    handlers = {
        'run': _run_handler,
        'plot': _plot_handler
    }

    handlers[args.command](args, experiment)

if __name__ == '__main__':
    main()
