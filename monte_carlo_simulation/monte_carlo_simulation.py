"""
DOCSTRING
"""
import random
from matplotlib import pyplot

BANKROLL = 1000
NUM_WAGERS = 1000
WAGER_SIZE = 100
SAMPLE_SIZE = 100

class MonteCarloSimulation:
    """
    DOCSTRING
    """
    def martingale_bettor(self, bankroll, initial_wager, wager_count, color):
        """
        DOCSTRING
        """
        current_wager, value = initial_wager, bankroll
        broke_count, profits = 0, 0
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
                    if value <= 0:
                        broke_count += 1
                        break
            else:
                if self.roll_dice():
                    current_wager = previous_wager*2
                    if (value-current_wager) < 0:
                        current_wager = value
                    value += current_wager
                    current_wager = initial_wager
                    previous_wager_won = True
                else:
                    current_wager = previous_wager*2
                    if (value-current_wager) < 0:
                        current_wager = value
                    value -= current_wager
                    previous_wager_won = False
                    previous_wager = current_wager
                    if value <= 0:
                        broke_count += 1
                        break
            wagers.append(count)
            values.append(value)
        pyplot.plot(wagers, values, color)
        if value > bankroll:
            profits += 1
        return broke_count, profits

    def roll_dice(self):
        """
        DOCSTRING
        """
        return bool(100 > random.randint(1, 100) > 50)

    def simple_bettor(self, bankroll, initial_wager, wager_count, color):
        """
        DOCSTRING
        """
        current_wager, value = initial_wager, bankroll
        broke_count, profits = 0, 0
        values, wagers = [], []
        for count in range(1, wager_count):
            if self.roll_dice():
                value += current_wager
            else:
                value -= current_wager
                if value <= 0:
                    broke_count += 1
                    break
            wagers.append(count)
            values.append(value)
        pyplot.plot(wagers, values, color)
        if value > bankroll:
            value = 0
            profits += 1
        return broke_count, profits

if __name__ == '__main__':
    # simple bettor
    for _ in range(SAMPLE_SIZE):
        broke_count_a, profits_a = MonteCarloSimulation().simple_bettor(
            BANKROLL, WAGER_SIZE, NUM_WAGERS, 'k')
    DEATH_RATE = (broke_count_a/float(SAMPLE_SIZE))*100
    print('Death Rate:Simple:' + str(DEATH_RATE))
    SURVIVAL_RATE = 100-DEATH_RATE
    print('Survival Rate:Simple:' + str(SURVIVAL_RATE))
    PROFIT_CHANCE = (profits_a/float(SAMPLE_SIZE))*100
    print('Profit Chance:Simple:' + str(PROFIT_CHANCE))
    # martingale bettor
    for _ in range(SAMPLE_SIZE):
        broke_count_b, profits_b = MonteCarloSimulation().martingale_bettor(
            BANKROLL, WAGER_SIZE, NUM_WAGERS, 'c')
    DEATH_RATE = (broke_count_b/float(SAMPLE_SIZE))*100
    print('Death Rate:Martingale:' + str(DEATH_RATE))
    SURVIVAL_RATE = 100-DEATH_RATE
    print('Survival Rate:Martingale:' + str(SURVIVAL_RATE))
    PROFIT_CHANCE = (profits_b/float(SAMPLE_SIZE))*100
    print('Profit Chance:Simple:' + str(PROFIT_CHANCE))
    # graph
    pyplot.ylabel('Account Value')
    pyplot.xlabel('Wager Count')
    pyplot.axhline(0, color='r')
    pyplot.show()
