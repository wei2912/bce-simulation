"""
This module serves as an interface to
argparse.
"""

import argparse, sys

MODES_TXT = {
    'coin': [
        'mode determines what type of graph to plot.',
        'mode l: varying diameter of coin',
        'mode w: varying width of gap',
    ],
    'needle': [
        'mode determines what type of graph to plot.',
        'mode l: 2D scatter plot, length of needle against probability of needle touching a line',
        'mode w: 2D scatter plot, gap width against probability of needle touching a line'
    ]
}

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
        choices=[i for i in modes],
        required=True,
        help="\n".join(modes_txt)
    )

def _coin_diameter(parser):
    parser.add_argument(
        '-d',
        '--diameter',
        type=float,
        required=True,
        help='diameter of coin'
    )

def _needle_length(parser):
    parser.add_argument(
        '-l',
        '--length',
        type=float,
        required=True,
        help='length of needle'
    )

def _all_length(parser):
    parser.add_argument(
        '-l',
        '--length',
        type=float,
        required=True,
        help='length/diameter of needle/coin'
    )

def _setup_run(subparsers, experiment):
    parser_run = subparsers.add_parser('run')

    experiments = {
        'coin': _coin_diameter,
        'coin_phy': _coin_diameter,
        'needle': _needle_length,
        'needle_phy': _needle_length,
        'all': lambda x: x
    }

    experiments[experiment](parser_run)

    _gap(parser_run)
    if experiment == 'coin' or experiment == 'needle' or experiment == 'needle_phy':
        _trials(parser_run, 1000000)
    elif experiment == 'coin_phy': # more resource intensive
        _trials(parser_run, 100000)

def _setup_plot(subparsers, experiment, plot_modes, plot_modes_txt):
    parser_plot = subparsers.add_parser('plot')

    experiments = {
        'coin': _coin_diameter,
        'coin_phy': _coin_diameter,
        'needle': _needle_length,
        'needle_phy': _needle_length,
        'all': _all_length
    }

    experiments[experiment](parser_plot)

    _gap(parser_plot)
    if not experiment == 'all':
        _trials(parser_plot, 1000)
    _output(parser_plot)
    _modes(parser_plot, plot_modes, plot_modes_txt)

def _error(parser):
    parser.add_argument(
        'command',
        type=str,
        choices=['run', 'plot'],
        help='command to run'
    )
    parser.parse_args()

def get_args(plot_modes):
    descriptions = {
        'coin': "Buffon's Coin Experiment",
        'coin_phy': "Buffon's Coin Experiment (a variation)",
        'needle': "Buffon's Needle Experiment",
        'needle_phy': "Buffon's Needle Experiment (a variation)",
        'all': "Comparison of the 3 experiments"
    }

    parser = argparse.ArgumentParser(
        description="Simulations of Buffon's Experiments"
    )

    parser.add_argument(
        'experiment',
        type=str,
        choices=list(descriptions.iterkeys()),
        help='experiment to run'
    )

    experiment = None

    # Error if invalid or no command is given
    length = len(sys.argv)
    if length > 1:
        experiment = sys.argv[1]
        if experiment not in descriptions:
            _error(parser)
    elif length == 1:
        _error(parser)

    subparsers = parser.add_subparsers(
        dest='command'
    )

    plot_modes_txt = MODES_TXT[experiment.replace('_phy', '')]

    if not experiment == "all":
        _setup_run(subparsers, experiment)
    _setup_plot(subparsers, experiment, plot_modes, plot_modes_txt)

    return parser.parse_args()
