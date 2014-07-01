"""
This module contains various configurations for various modules.
"""

def mpl(matplotlib, stdout):
    if stdout:
        matplotlib.use('Agg')
    matplotlib.rc('savefig', dpi=150)
