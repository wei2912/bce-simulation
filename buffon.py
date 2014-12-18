#!/usr/bin/env python
# coding=utf-8

"""
This script runs a simulation of the experiments.
"""

from argh import arg, wrap_errors, dispatch_commands
import pylab

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

STEPSIZE = 1000
OFFSET = 0.01

COLORS = {
    'coin': 'purple',
    'coin_var': 'red',
    'needle': 'blue',
    'needle_var': 'green'
}

LABELS = {
    'coin': u"Buffon's Coin Problem",
    'coin_var': u"Variation of Buffon's Coin Problem",
    'needle': u"Buffon's Needle Problem",
    'needle_var': u"Variation of Buffon's Needle Problem"
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
@arg('xmin', type=float, default=0.0, help='minimum x value')
@arg('xmax', type=float, help='maximum x value')
@arg('output', type=str, help='filename to output graph to')
@wrap_errors([ValueError])
def plot(gtype, xmin, xmax, output):
    """
    Argument handler for the `plot` subcommand.
    """

    pylab.plot(
        [1, 1],
        [0, 1],
        color='black',
        linestyle='dashed',
        linewidth=1
    )

    def get_range(min_val, max_val):
        """
        This function will return a range of values
        given the size of the range.
        """
        i = 1
        while i < STEPSIZE + 1:
            yield i * (max_val - min_val) / STEPSIZE + min_val
            i += 1

    xs = list(get_range(xmin, xmax))
    for problem, sim in sorted(SIMULATIONS.items()):
        ys = []
        for x in xs:
            data = {}
            if gtype == 'length':
                if problem.startswith("coin"):
                    data['diameter'] = x
                elif problem.startswith("needle"):
                    data['length'] = x
            elif gtype == 'gap_width':
                data['gap_width'] = x

            ys.append(sim.predict_prob(**data))

        pylab.plot(
            xs,
            ys,
            color=COLORS[problem],
            label=LABELS[problem],
            linewidth=2.0
        )

    pylab.legend(loc='best')

    offset = (xmax - xmin) * OFFSET
    pylab.xlim(xmin - offset, xmax + offset)
    offset = OFFSET
    pylab.ylim(-offset, 1 + offset)

    pylab.xlabel(GRAPHS[gtype]['xlabel'])
    pylab.ylabel(GRAPHS[gtype]['ylabel'])
    pylab.title(GRAPHS[gtype]['title'])
    pylab.grid(True)

    if output:
        pylab.savefig(output)
    else:
        pylab.show()

dispatch_commands([run, plot])
