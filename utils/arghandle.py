"""
This module serves as an interface to
argparse.
"""

import argparse

def _trials(parser, trials):
    parser.add_argument(
        '-t',
        '--trials',
        type=int,
        default=trials,
        help='number of trials to run'
    )

def _gap(parser):
    parser.add_argument(
        '-g',
        '--gap',
        type=float,
        required=True,
        help='width of square gap'
    )

def _stepsize(parser, stepsize):
    parser.add_argument(
        '-s',
        '--stepsize',
        type=int,
        default=stepsize,
        help='number of steps to take'
    )

def _verbose(parser):
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='enable verbose output'
    )

def _output(parser):
    parser.add_argument(
        '-o',
        '--output',
        help='filename to output graph to'
    )

def _modes(parser, modes, modes_txt):
    parser.add_argument(
        '-m',
        '--mode',
        type=int,
        choices=[i for i in modes],
        required=True,
        help="\n".join(modes_txt)
    )

def _coin_radius(parser):
    parser.add_argument(
        '-r',
        '--radius',
        type=float,
        required=True,
        help='radius of coin'
    )

def _needle_length(parser):
    parser.add_argument(
        '-l',
        '--length',
        type=float,
        required=True,
        help='length of needle'
    )

def _diameter(parser):
    parser.add_argument(
        '-d',
        '--diameter',
        type=float,
        required=True,
        help='diameter of coin/length of needle'
    )

def _setup_run(subparsers, mode):
    parser_run = subparsers.add_parser('run')

    mode_specific = {
        'coin': _coin_radius,
        'needle': _needle_length,
        'coin_phy': _coin_radius,
        'all': lambda x: x
    }

    mode_specific[mode](parser_run)

    _gap(parser_run)
    if mode == 'coin' or mode == 'needle':
        _trials(parser_run, 1000000)
    elif mode == 'coin_phy': # more resource intensive
        _trials(parser_run, 100000)

def _setup_plot(subparsers, mode, plot_modes, plot_modes_txt):
    parser_plot = subparsers.add_parser('plot')

    mode_specific = {
        'coin': _coin_radius,
        'needle': _needle_length,
        'coin_phy': _coin_radius,
        'all': _diameter
    }

    mode_specific[mode](parser_plot)

    _gap(parser_plot)
    if not mode == 'all':
        _trials(parser_plot, 1000)
        _stepsize(parser_plot, 100)
        _verbose(parser_plot)
    _output(parser_plot)
    _modes(parser_plot, plot_modes, plot_modes_txt)

def get_args(mode, plot_modes, plot_modes_txt):
    descriptions = {
        'coin': "Buffon's Coin Experiment",
        'needle': "Buffon's Needle Experiment",
        'coin_phy': "Buffon's Coin Experiment (a variation)",
        'all': "Comparison of the 3 experiments"
    }

    parser = argparse.ArgumentParser(
        description=descriptions[mode]
    )

    subparsers = parser.add_subparsers(
        dest='command'
    )

    if not mode == "all":
        _setup_run(subparsers, mode)
    _setup_plot(subparsers, mode, plot_modes, plot_modes_txt)

    return parser.parse_args()
