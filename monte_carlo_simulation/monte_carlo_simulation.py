"""
DOCSTRING
"""
import random
from matplotlib import pyplot

def roll_dice():
    """
    DOCSTRING
    """
    return bool(100 > random.randint(1, 100) > 50)

def simple_bettor(bankroll, initial_wager, wager_count):
    """
    DOCSTRING
    """
    value, values, wagers = bankroll, [], []
    for count in range(1, wager_count):
        if roll_dice():
            value += initial_wager
        else:
            value -= initial_wager
        wagers.append(count)
        values.append(value)
    pyplot.plot(wagers, values)

if __name__ == '__main__':
    for _ in range(100):
        simple_bettor(10000, 100, 100)
    pyplot.ylabel('Account Value')
    pyplot.xlabel('Wager Count')
    pyplot.show()
