"""
DOCSTRING
"""
import random
from matplotlib import pyplot

BANKROLL = 1000
HIGHER_PROFIT = 63.208
LOWER_BUST = 31.235
NUM_WAGERS = 1000
WAGER_SIZE = 100
SAMPLE_SIZE = 100

class MonteCarloSimulation:
    """
    DOCSTRING
    """
    def __init__(self, bankroll, initial_wager):
        """
        DOCSTRING
        """
        self.bankroll = bankroll
        self.broke_count = 0
        self.current_wager = 1
        self.initial_wager = initial_wager
        self.previous_wager = initial_wager
        self.previous_wager_won = True
        self.profits = 0
        self.value = bankroll
        self.values = []
        self.wagers = []

    def martingale_bettor(self, wager_count, color):
        """
        DOCSTRING
        """
        for count in range(1, wager_count):
            if self.previous_wager_won:
                if self.roll_dice():
                    self.value += self.current_wager
                else:
                    self.value -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.value <= 0:
                        self.broke_count += 1
                        break
            else:
                if self.roll_dice():
                    self.current_wager = previous_wager*2
                    if (self.value-self.current_wager) < 0:
                        self.current_wager = self.value
                    self.value += self.current_wager
                    self.current_wager = self.initial_wager
                    self.previous_wager_won = True
                else:
                    self.current_wager = previous_wager*2
                    if (self.value-self.current_wager) < 0:
                        self.current_wager = self.value
                    self.value -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.value <= 0:
                        self.broke_count += 1
                        break
            self.wagers.append(count)
            self.values.append(self.value)
        pyplot.plot(self.wagers, self.values, color)
        if self.value > self.bankroll:
            self.profits += 1
        return self.broke_count, self.profits

    def multiple_bettor(self, wager_count, random_multiple):
        """
        DOCSTRING
        """
        for count in range(1, wager_count):
            if self.previous_wager_won:
                if self.roll_dice():
                    self.value += self.current_wager
                else:
                    self.value -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.value <= 0:
                        self.broke_count += 1
                        break
            else:
                if self.roll_dice():
                    self.current_wager = previous_wager*random_multiple
                    if (self.value-self.current_wager) < 0:
                        self.current_wager = self.value
                    self.value += self.current_wager
                    self.current_wager = self.initial_wager
                    self.previous_wager_won = True
                else:
                    self.current_wager = previous_wager*random_multiple
                    if (self.value-self.current_wager) < 0:
                        self.current_wager = self.value
                    self.value -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.value <= 0:
                        self.broke_count += 1
                        break
            self.wagers.append(count)
            self.values.append(self.value)
        #pyplot.plot(self.wagers, self.values)
        if self.value > self.bankroll:
            self.profits += 1
        return self.broke_count, self.profits

    def roll_dice(self):
        """
        DOCSTRING
        """
        return bool(100 > random.randint(1, 100) > 50)

    def simple_bettor(self, wager_count, color):
        """
        DOCSTRING
        """
        for count in range(1, wager_count):
            if self.roll_dice():
                self.value += self.current_wager
            else:
                self.value -= self.current_wager
                if self.value <= 0:
                    self.broke_count += 1
                    break
            self.wagers.append(count)
            self.values.append(self.value)
        pyplot.plot(self.wagers, self.values, color)
        if self.value > self.bankroll:
            self.value = 0
            self.profits += 1
        return self.broke_count, self.profits

if __name__ == '__main__':
    MODEL_NAMES = ['simple', 'martingale', 'multiple']
    BROKE_COUNTS = []
    PROFITS = []
    # simple bettor
    for _ in range(SAMPLE_SIZE):
        broke_count, profit = MonteCarloSimulation(
            BANKROLL, WAGER_SIZE).simple_bettor(NUM_WAGERS, 'k')
        BROKE_COUNTS.append(broke_count)
        PROFITS.append(profit)
    # martingale bettor
    for _ in range(SAMPLE_SIZE):
        broke_count, profit = MonteCarloSimulation(
            BANKROLL, WAGER_SIZE).martingale_bettor(NUM_WAGERS, 'c')
        BROKE_COUNTS.append(broke_count)
        PROFITS.append(profit)
    # multiple bettor
    for _ in range(SAMPLE_SIZE):
        RANDOM_MULTIPLE = random.uniform(0.1, 10.0)
        broke_count, profit = MonteCarloSimulation(
            BANKROLL, WAGER_SIZE).multiple_bettor(NUM_WAGERS, RANDOM_MULTIPLE)
        BUST_RATE = (broke_count/SAMPLE_SIZE)*100.00
        PROFIT_RATE = (profit/SAMPLE_SIZE)*100.00
        if BUST_RATE < LOWER_BUST:
            if PROFIT_RATE > HIGHER_PROFIT:
                print('#############################')
                print('Found Winner:' + str(RANDOM_MULTIPLE))
                print('Lower Bust:' + str(LOWER_BUST))
                print('Higher Profit:' + str(HIGHER_PROFIT))
                print('Bust Rate:' + str(BUST_RATE))
                print('Profit Rate:' + str(PROFIT_RATE))
                print('#############################')
        BROKE_COUNTS.append(broke_count)
        PROFITS.append(profit)
    # statistics
    for count_outer, element in enumerate(MODEL_NAMES):
        DEATH_RATE = (BROKE_COUNTS[count_outer]/float(SAMPLE_SIZE))*100
        SURVIVAL_RATE = 100-DEATH_RATE
        PROFIT_CHANCE = (PROFITS[count_outer]/float(SAMPLE_SIZE))*100
        print('Death Rate:' + MODEL_NAMES[count_outer] + ':' + str(DEATH_RATE))
        print('Survival Rate:' + MODEL_NAMES[count_outer] + ':' + str(SURVIVAL_RATE))
        print('Profit Chance:' + MODEL_NAMES[count_outer] + ':' + str(PROFIT_CHANCE))
    # graph
    pyplot.ylabel('Account Value')
    pyplot.xlabel('Wager Count')
    pyplot.axhline(0, color='r')
    pyplot.show()
