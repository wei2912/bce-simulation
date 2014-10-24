"""
This module contains utilities for `bce-simulation` which
will be used by the scripts in the root directory.
"""
from . import coin, coin_phy, needle, needle_phy

SIMULATIONS = {
    'coin': coin,
    'coin_phy': coin_phy,
    'needle': needle,
    'needle_phy': needle_phy
}
