#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of the experiments.
"""

# Use Agg if running Matplotlib from a server
import os
if os.environ.get('SERVER'):
  import matplotlib
  matplotlib.use('Agg')

from argh import arg, wrap_errors, dispatch_commands
from matplotlib import pyplot as plt

from utils import coin, coin_var, needle, needle_var

SIMULATIONS = {
    'coin': coin,
    'coin_var': coin_var,
    'needle': needle,
    'needle_var': needle_var
}

GRAPHS = {
    'length': {
        'xlabel': u"Diameter/Length",
        'ylabel': u"Probability of coin/needle balancing",
        'title': u"Buffon's Coin Problem and Buffon's Needle Problem"
    },
    'gap_width': {
        'xlabel': u"Width of gap",
        'ylabel': u"Probability of coin/needle balancing",
        'title': u"Buffon's Coin Problem and Buffon's Needle Problem"
    }
}

COLORS = {
    'coin': 'red',
    'coin_var': 'red',
    'coin_var_sim': 'red',
    'needle': 'blue',
    'needle_var': 'blue',
    'needle_var_sim': 'blue'
}

LABELS = {
    'coin': u"Buffon's Coin Problem",
    'coin_var': u"Variation of Buffon's Coin Problem",
    'coin_var_sim': u"Variation of Buffon's Coin Problem (simulated)",
    'needle': u"Buffon's Needle Problem",
    'needle_var': u"Variation of Buffon's Needle Problem",
    'needle_var_sim': u"Variation of Buffon's Needle Problem (simulated)"
}

@arg('problem', choices=list(SIMULATIONS.keys()), help='type of problem')
@arg('length', type=float, help='length of needle or diameter of coin')
@arg('gap', type=float, help='width of gap')
@arg('-t', '--trials', type=int, help='number of trials to run')
@wrap_errors([ValueError])
def run(problem, length, gap, trials=None):
    """
    Argument handler for the `run` subcommand.
    """
    sim = SIMULATIONS[problem]

    data = {}
    if problem.startswith("coin"):
        data['diameter'] = length
    elif problem.startswith("needle"):
        data['length'] = length
    data['gap_width'] = gap

    pred_prob = sim.predict_prob(**data)
    yield "predicted probability: %f" % pred_prob

    if trials:
        pred_hits = pred_prob * trials
        yield "predicted hits: %f" % pred_hits

        if problem.endswith("_var"):
            data['trials'] = trials

            hits = sim.run_trials(**data)
            yield "observed hits: %d" % hits

            stat = sum([
                (hits - pred_hits) ** 2 / pred_hits,
                ((trials - hits) - (trials - pred_hits)) ** 2 / (trials-pred_hits)
            ])
            yield "chi-square stat: %f" % stat

@arg('gtype', choices=list(GRAPHS.keys()), help='type of graph')
@arg('xmin', type=float, help='minimum x value')
@arg('xmax', type=float, help='maximum x value')
@arg('-o', '--output', type=str, help='filename to output graph to')
@wrap_errors([ValueError])
def plot(gtype, xmin, xmax, output=None):
    """
    Argument handler for the `plot` subcommand.
    """

    def get_range(min_val, max_val, stepsize):
        """
        This function will return a range of values
        given the size of the range.
        """
        i = 1
        while i < stepsize + 1:
            yield i * (max_val - min_val) / stepsize + min_val
            i += 1

    def get_data(gtype, problem, x):
        data = {}
        if gtype == 'length':
            if problem.startswith("coin"):
                data['diameter'] = x
            elif problem.startswith("needle"):
                data['length'] = x
        elif gtype == 'gap_width':
            data['gap_width'] = x
        return data

    plt.plot(
        [1, 1],
        [0, 1],
        color='black',
        linestyle='--',
        linewidth=1
    )

    xs = list(get_range(xmin, xmax, 10000))
    trials_xs = list(get_range(xmin, xmax, 200))
    for problem, sim in sorted(SIMULATIONS.items()):
        ys = []
        for x in xs:
            data = get_data(gtype, problem, x)
            ys.append(sim.predict_prob(**data))

        plt.plot(
            xs,
            ys,
            color=COLORS[problem],
            label=LABELS[problem],
            linewidth=2,
            linestyle='-' if problem.endswith("var") else '--'
        )

        if problem.endswith('var'):
            trials_ys = []
            for x in trials_xs:
            	if problem == 'needle_var':
            		length = x if gtype == 'length' else 1
            		gap_width = x if gtype == 'gap_width' else 1
            		if length <= gap_width:
            			trials_ys.append(None)
            			continue
                data = get_data(gtype, problem, x)
                data['trials'] = 1000
                trials_ys.append(sim.run_trials(**data) / 1000.0)

            plt.scatter(
                trials_xs,
                trials_ys,
                color=COLORS[problem + "_sim"],
                label=LABELS[problem + "_sim"]
            )

    plt.legend(loc='best', prop={'size': 10})

    offset = (xmax - xmin) * 0.01
    plt.xlim(xmin - offset, xmax + offset)
    offset = 0.01
    plt.ylim(0, 1 + offset)

    plt.xlabel(GRAPHS[gtype]['xlabel'])
    plt.ylabel(GRAPHS[gtype]['ylabel'])
    plt.title(GRAPHS[gtype]['title'])
    plt.grid(True)

    if output:
        plt.savefig(output)
    else:
        plt.show()

dispatch_commands([run, plot])
