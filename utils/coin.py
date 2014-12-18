"""
Simulation of Buffon's Coin Problem.
"""

def predict_prob(diameter=1.0, gap_width=1.0):
    """
    Predicts the probability that the coin will hit
    the grid.
    """
    d = diameter
    D = gap_width

    if d >= D:
        return 1.0
    else:
        return (
            1.0 -
            (D - d) ** 2 /
            D ** 2
        )
