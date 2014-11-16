#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of the experiments.
"""

from argh import arg, wrap_errors, dispatch_commands

from utils import graph, SIMULATIONS

MODES = [
    'length',
    'gap_width'
]

GRAPH_CAPTIONS = {
    'coin': {
        'length': [
            u"Diameter",
            u"Probability of coin touching the grid",
            u"Buffon’s Coin Experiment"
        ],
        'gap_width': [
            u"Width of square gap",
            u"Probability of coin touching the grid",
            u"Buffon’s Coin Experiment"
        ]
    },
    'coin_phy': {
        'length': [
            u"Diameter",
            u"Probability of coin balancing on the grid",
            u"Buffon’s Coin Experiment (a variation)"
        ],
        'gap_width': [
            u"Width of square gap",
            u"Probability of coin balancing on the grid",
            u"Buffon’s Coin Experiment (a variation)"
        ]
    },
    'needle': {
        'length': [
            u"Length",
            u"Probability of needle touching the lines",
            u"Buffon’s Needle Experiment"
        ],
        'gap_width': [
            u"Width of square gap",
            u"Probability of needle touching the lines",
            u"Buffon's Needle Experiment"
        ]
    },
    'needle_phy': {
        'length': [
            u"Length",
            u"Probability of needle balancing on the lines",
            u"Buffon’s Needle Experiment (a variation)"
        ],
        'gap_width': [
            u"Width of square gap",
            u"Probability of needle balancing on the lines",
            u"Buffon's Needle Experiment (a variation)"
        ]
    }
}

@arg('experiment', choices=SIMULATIONS.keys(), help='type of experiment to run')
@arg('-l', '--length', type=float, required=True, help='length of needle or diameter of coin')
@arg('-g', '--gap', type=float, required=True, help='width of gap')
@arg('-t', '--trials', type=int, help='number of trials to run')
@wrap_errors([ValueError])
def run(experiment, length, gap, trials=1000000):
    """
    Argument handler for the `run` subcommand.
    """
    sim = SIMULATIONS[experiment]

    hits = sim.run_trials(length, gap, trials)

    yield "%d/%d" % (hits, trials)
    prob = float(hits) / trials
    yield "observed prob: %f" % prob
    yield "expected prob: %f" % sim.predict_prob(length, gap)

@arg('experiment', choices=SIMULATIONS.keys(), help='type of experiment to run')
@arg('mode', choices=MODES, help='variable to vary (all other variables are set to 1)')
@arg('--xmin', type=float, default=0.0, help='minimum x value')
@arg('--xmax', type=float, required=True, help='maximum x value')
@arg('-t', '--trials', type=int, default=1000, help='number of trials to run')
@arg('-o', '--output', type=str, help='filename to output graph to')
@wrap_errors([ValueError])
def plot(experiment, mode, xmin, xmax, trials, output):
    """
    Argument handler for the `plot` subcommand.
    """
    sim = SIMULATIONS[experiment]

    graph.init(output)

    xs = list(graph.get_range(xmin, xmax))
    if mode == 'length':
        predict_prob = lambda xs: sim.predict_prob(xs, 1.0)
        run_trials = lambda x: sim.run_trials(x, 1.0, trials)
    elif mode == 'gap_width':
        predict_prob = lambda xs: sim.predict_prob(1.0, xs)
        run_trials = lambda x: sim.run_trials(1.0, x, trials)

    graph.line_plot(xs, predict_prob(xs))
    graph.scatter_plot(xs, [float(run_trials(x)) / trials for x in xs])

    graph.scale_x_plot(xs[-1])
    graph.scale_y_plot(1.0)

    graph.prepare_plot(*GRAPH_CAPTIONS[experiment][mode])

    graph.display_plot(output)

dispatch_commands([run, plot])
