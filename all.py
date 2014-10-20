#!/usr/bin/env python
# coding=utf-8

"""
This script compares all 3 simulations.
"""

from utils import arghandle, graph
from utils import coin, coin_phy, needle

def plot_length(l, w):
    """
    Plots a 2D scatter plot which shows the
    relationship between the diameter/length against
    probability of coin/needle touching/balancing on lines.
    """

    xs = list(graph.get_range(l))

    ys = needle.predict_prob(xs, w)
    graph.line_plot(xs, ys, color='red')

    ys = coin.predict_prob(xs, w)
    graph.line_plot(xs, ys, color='green')

    ys = coin_phy.predict_prob(xs, w)
    graph.line_plot(xs, ys, color='blue')

    graph.legend(
    	u"Buffon’s Needle Experiment",
    	u"Buffon’s Coin Experiment",
    	u"Buffon’s Coin Experiment (A variation)"
    )

    graph.scale_x_plot(l)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
        "Length of needle/Diameter of coin",
        "Probability of needle/coin touching/balancing on lines",
        "Comparison of the 3 experiments" +
            "\nwidth of gap = %.5g" % w
    )

def plot_width(l, w):
    """
    Plots a 2D scatter plot which shows the
    relationship between the width of a square gap
    and the probability which the coin hits the grid.

    l = length of needle/diameter of coin
    w = width of gap
    """

    xs = list(graph.get_range(w))

    ys = needle.predict_prob(l, xs)
    graph.line_plot(xs, ys, color='red')

    ys = coin.predict_prob(l, xs)
    graph.line_plot(xs, ys, color='green')

    ys = coin_phy.predict_prob(l, xs)
    graph.line_plot(xs, ys, color='blue')

    graph.legend(
    	u"Buffon’s Needle Experiment",
    	u"Buffon’s Coin Experiment",
    	u"Buffon’s Coin Experiment (A variation)"
    )
    graph.scale_x_plot(w)
    graph.scale_y_plot(1.0)
    graph.prepare_plot(
        "Width of gap",
        "Probability of needle/coin touching/balancing on lines",
        "Comparison of the 3 experiments" +
            "\nlength/diameter = %.5g" % l
    )

MODES = {
    'l': plot_length,
    'w': plot_width
}

MODES_TXT = [
    'mode determines what type of graph to plot.',
    'mode l: varying diameter of coin/length of needle',
    'mode w: varying width of gap'
]

def _plot_handler(args):
    graph.init(args.output)

    l = float(args.length)
    w = float(args.gap)

    MODES[args.mode](l, w)

    graph.display_plot(args.output)

def main():
    args = arghandle.get_args('all', MODES, MODES_TXT)
    _plot_handler(args)

if __name__ == '__main__':
    main()
