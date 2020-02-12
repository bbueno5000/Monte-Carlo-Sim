"""
DOCSTRING
"""
import random
from matplotlib import pyplot

NUM_BETTORS = 1000

class MonteCarloSimulation:
    """
    DOCSTRING
    """
    broke_count = 0

    def martingale_bettor(self, bankroll, initial_wager, wager_count):
        """
        DOCSTRING
        """
        value, current_wager = bankroll, initial_wager
        values, wagers = [], []
        previous_wager_won = True
        previous_wager = initial_wager
        for count in range(1, wager_count):
            if previous_wager_won:
                if self.roll_dice():
                    value += current_wager
                else:
                    value -= current_wager
                    previous_wager_won = False
                    previous_wager = current_wager
                    if value < 0:
                        MonteCarloSimulation.broke_count += 1
                        break
            else:
                if self.roll_dice():
                    current_wager = previous_wager*2
                    value += current_wager
                    current_wager = initial_wager
                    previous_wager_won = True
                else:
                    current_wager = previous_wager*2
                    value -= current_wager
                    previous_wager_won = False
                    previous_wager = current_wager
                    if value < 0:
                        MonteCarloSimulation.broke_count += 1
                        break
            wagers.append(count)
            values.append(value)
        pyplot.plot(wagers, values)
    
    def roll_dice(self):
        """
        DOCSTRING
        """
        return bool(100 > random.randint(1, 100) > 50)

    def simple_bettor(self, bankroll, initial_wager, wager_count):
        """
        DOCSTRING
        """
        value, values, wagers = bankroll, [], []
        for count in range(1, wager_count):
            if self.roll_dice():
                value += initial_wager
            else:
                value -= initial_wager
            wagers.append(count)
            values.append(value)
        pyplot.plot(wagers, values)

if __name__ == '__main__':
    for _ in range(NUM_BETTORS):
        MonteCarloSimulation().martingale_bettor(10000, 100, 100)
    DEATH_RATE = (MonteCarloSimulation().broke_count/float(NUM_BETTORS))*100
    SURVIVAL_RATE = 100-DEATH_RATE
    print('Death Rate:' + str(DEATH_RATE))
    print('Survival Rate:' + str(SURVIVAL_RATE))
    pyplot.ylabel('Account Value')
    pyplot.xlabel('Wager Count')
    pyplot.axhline(0, color='r')
    pyplot.show()
