"""
Simulation of Buffon's Coin Experiment.
"""

import numexpr as ne

def predict_prob(diameter, width):
    """
    Predicts the probability that the coin will hit
    the grid.

    diameter and width can be scalars or arrays.
    """
    clauses = [
        "d >= D", "1",
        "1 - ((D - d) ** 2) / (D ** 2)"
    ]

    return ne.evaluate(
        'where(%s, %s, %s)' % tuple(clauses),
        local_dict={
            'd': diameter,
            'D': width
        }
    )
