"""
DOCSTRING
"""
import random
from matplotlib import pyplot

INITIAL_BANKROLL = 1000
HIGHER_PROFIT = 63.208
LOWER_BUST = 31.235
NUM_WAGERS = 1000
WAGER_SIZE = 100
SAMPLE_SIZE = 100

class MonteCarloSimulation:
    """
    DOCSTRING
    """
    def __init__(self, initial_bankroll, initial_wager):
        """
        DOCSTRING
        """
        self.bankrolls = []
        self.busts = 0
        self.current_bankroll = initial_bankroll
        self.current_wager = initial_wager
        self.initial_bankroll = initial_bankroll
        self.initial_wager = initial_wager
        self.previous_wager = initial_wager
        self.previous_wager_won = True
        self.profits = 0
        self.wagers = []

    def alembert_bettor(self, wager_count):
        """
        DOCSTRING
        """
        for _ in range(1, wager_count):
            if self.previous_wager_won:
                if self.current_wager == self.initial_wager:
                    pass
                else:
                    self.current_wager -=  self.initial_wager
                if self.roll_dice():
                    self.current_bankroll += self.current_wager
                    self.previous_wager = self.current_wager
                else:
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    self.previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            else:
                self.current_wager = self.previous_wager + self.initial_wager
                if self.current_bankroll - self.current_wager <= 0:
                    self.current_wager = self.current_bankroll
                if self.roll_dice():
                    self.current_bankroll += self.current_wager
                    self.previous_wager = self.current_wager
                    self.previous_wager_won = True
                else:
                    self.current_bankroll -= self.current_wager
                    self.previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
        if self.current_bankroll > self.initial_bankroll:
            self.profits += 1
        return self.busts, self.profits

    def martingale_bettor(self, wager_count, color):
        """
        DOCSTRING
        """
        for count in range(1, wager_count):
            if self.previous_wager_won:
                if self.roll_dice():
                    self.current_bankroll += self.current_wager
                else:
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            else:
                if self.roll_dice():
                    self.current_wager = previous_wager*2
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll += self.current_wager
                    self.current_wager = self.initial_wager
                    self.previous_wager_won = True
                else:
                    self.current_wager = previous_wager*2
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            self.wagers.append(count)
            self.bankrolls.append(self.current_bankroll)
        pyplot.plot(self.wagers, self.bankrolls, color)
        if self.current_bankroll > self.initial_bankroll:
            self.profits += 1
        return self.busts, self.profits

    def multiple_bettor(self, wager_count, random_multiple):
        """
        DOCSTRING
        """
        for count in range(1, wager_count):
            if self.previous_wager_won:
                if self.roll_dice():
                    self.current_bankroll += self.current_wager
                else:
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            else:
                if self.roll_dice():
                    self.current_wager = previous_wager*random_multiple
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll += self.current_wager
                    self.current_wager = self.initial_wager
                    self.previous_wager_won = True
                else:
                    self.current_wager = previous_wager*random_multiple
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            self.wagers.append(count)
            self.bankrolls.append(self.current_bankroll)
        pyplot.plot(self.wagers, self.bankrolls)
        if self.current_bankroll > self.initial_bankroll:
            self.profits += 1
        return self.busts, self.profits

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
                self.current_bankroll += self.current_wager
            else:
                self.current_bankroll -= self.current_wager
                if self.current_bankroll <= 0:
                    self.busts += 1
                    break
            self.wagers.append(count)
            self.bankrolls.append(self.current_bankroll)
        pyplot.plot(self.wagers, self.bankrolls, color)
        if self.current_bankroll > self.initial_bankroll:
            self.current_bankroll = 0
            self.profits += 1
        return self.busts, self.profits

if __name__ == '__main__':
    MODEL_NAMES = ['simple', 'martingale', 'multiple', 'alembert']
    BROKE_COUNTS = []
    PROFITS = []
    # simple bettor
    for _ in range(SAMPLE_SIZE):
        busts, profit = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE).simple_bettor(NUM_WAGERS, 'k')
        BROKE_COUNTS.append(busts)
        PROFITS.append(profit)
    # martingale bettor
    for _ in range(SAMPLE_SIZE):
        busts, profit = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE).martingale_bettor(NUM_WAGERS, 'c')
        BROKE_COUNTS.append(busts)
        PROFITS.append(profit)
    # multiple bettor
    for _ in range(SAMPLE_SIZE):
        RANDOM_MULTIPLE = random.uniform(0.1, 10.0)
        busts, profit = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE).multiple_bettor(NUM_WAGERS, RANDOM_MULTIPLE)
        BUST_RATE = (busts/SAMPLE_SIZE)*100.00
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
        BROKE_COUNTS.append(busts)
        PROFITS.append(profit)
    # alembert bettor
    for _ in range(SAMPLE_SIZE):
        busts, profit = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE).alembert_bettor(NUM_WAGERS)
        BROKE_COUNTS.append(busts)
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
