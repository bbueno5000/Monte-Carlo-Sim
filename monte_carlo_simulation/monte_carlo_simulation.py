"""
DOCSTRING
"""
import csv
import random
from matplotlib import pyplot

BUST_FLOOR = 31.235
INITIAL_BANKROLL = 10000
PROFIT_CEILING = 63.208
SAMPLE_SIZE = 100

class MonteCarloSimulation:
    """
    DOCSTRING
    """
    def __init__(self, initial_bankroll, initial_wager, wager_count):
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
        self.wager_count = wager_count
        self.wagers = []

    def alembert_bettor(self):
        """
        DOCSTRING
        """
        for _ in range(self.wager_count):
            if self.previous_wager_won:
                if self.current_wager == self.initial_wager:
                    pass
                else:
                    self.current_wager -= self.initial_wager
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

    def coin_toss(self):
        """
        DOCSTRING
        """
        return bool(random.randint(1, 100) <= 50)

    def graph_data(self):
        """
        DOCTRING
        """
        with open('monte_carlo.csv', 'r') as file:
            data = csv.reader(file, delimiter=',')
            for line in data:
                percent_roi = float(line[0])
                wager_size_percent = float(line[1])
                wager_count = float(line[2])
                plot_color = line[3]
                pyplot.scatter(wager_size_percent, wager_count, color=plot_color)
            pyplot.show()

    def martingale_bettor(self, color):
        """
        DOCSTRING
        """
        for count in range(self.wager_count):
            if self.previous_wager_won:
                if self.roll_dice():
                    self.current_bankroll += self.current_wager
                else:
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    self.previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            else:
                if self.roll_dice():
                    self.current_wager = self.previous_wager*2
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll += self.current_wager
                    self.current_wager = self.initial_wager
                    self.previous_wager_won = True
                else:
                    self.current_wager = self.previous_wager*2
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    self.previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            self.wagers.append(count)
            self.bankrolls.append(self.current_bankroll)
        pyplot.plot(self.wagers, self.bankrolls, color)
        if self.current_bankroll > self.initial_bankroll:
            self.profits += 1
        return self.busts, self.profits

    def multiple_bettor(self, random_multiple):
        """
        DOCSTRING
        """
        for count in range(self.wager_count):
            if self.previous_wager_won:
                if self.roll_dice():
                    self.current_bankroll += self.current_wager
                else:
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    self.previous_wager = self.current_wager
                    if self.current_bankroll <= 0:
                        self.busts += 1
                        break
            else:
                if self.roll_dice():
                    self.current_wager = self.previous_wager*random_multiple
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll += self.current_wager
                    self.current_wager = self.initial_wager
                    self.previous_wager_won = True
                else:
                    self.current_wager = self.previous_wager*random_multiple
                    if (self.current_bankroll-self.current_wager) < 0:
                        self.current_wager = self.current_bankroll
                    self.current_bankroll -= self.current_wager
                    self.previous_wager_won = False
                    self.previous_wager = self.current_wager
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

    def simple_bettor(self, color):
        """
        DOCSTRING
        """
        for count in range(self.wager_count):
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
    BUSTS = []
    MODEL_NAMES = ['simple', 'martingale', 'multiple', 'alembert']
    NUM_WAGERS = int(random.uniform(10, 10000))
    PROFITS = []
    TOTAL_BUSTS = 0
    TOTAL_PROFITS = 0
    WAGER_SIZE = int(random.uniform(1, 1000))
    # simple bettor
    for _ in range(SAMPLE_SIZE):
        busts, profits = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE, NUM_WAGERS).simple_bettor('k')
        TOTAL_BUSTS += busts
        TOTAL_PROFITS += profits
    BUSTS.append(TOTAL_BUSTS)
    PROFITS.append(TOTAL_PROFITS)
    # martingale bettor
    for _ in range(SAMPLE_SIZE):
        busts, profits = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE, NUM_WAGERS).martingale_bettor('c')
        TOTAL_BUSTS += busts
        TOTAL_PROFITS += profits
    BUSTS.append(TOTAL_BUSTS)
    PROFITS.append(TOTAL_PROFITS)
    # multiple bettor
    for _ in range(SAMPLE_SIZE):
        RANDOM_MULTIPLE = random.uniform(0.1, 10.0)
        busts, profits = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE, NUM_WAGERS).multiple_bettor(RANDOM_MULTIPLE)
        BUST_RATE = (busts/SAMPLE_SIZE)*100.00
        PROFIT_RATE = (profits/SAMPLE_SIZE)*100.00
        if BUST_RATE < BUST_FLOOR:
            if PROFIT_RATE > PROFIT_CEILING:
                print('#############################')
                print('Found Winner:' + str(RANDOM_MULTIPLE))
                print('Lower Bust:' + str(BUST_FLOOR))
                print('Higher Profit:' + str(PROFIT_CEILING))
                print('Bust Rate:' + str(BUST_RATE))
                print('Profit Rate:' + str(PROFIT_RATE))
                print('#############################')
        TOTAL_BUSTS += busts
        TOTAL_PROFITS += profits
    BUSTS.append(TOTAL_BUSTS)
    PROFITS.append(TOTAL_PROFITS)
    # alembert bettor
    for _ in range(SAMPLE_SIZE):
        busts, profits = MonteCarloSimulation(
            INITIAL_BANKROLL, WAGER_SIZE, NUM_WAGERS).alembert_bettor()
        TOTAL_BUSTS += busts
        TOTAL_PROFITS += profits
    BUSTS.append(TOTAL_BUSTS)
    PROFITS.append(TOTAL_PROFITS)
    # statistics
    for count_outer, element in enumerate(MODEL_NAMES):
        DEATH_RATE = (BUSTS[count_outer]/float(SAMPLE_SIZE))*100
        SURVIVAL_RATE = 100-DEATH_RATE
        PROFIT_CHANCE = (PROFITS[count_outer]/float(SAMPLE_SIZE))*100
        print('#############################')
        print('Death Rate:' + MODEL_NAMES[count_outer] + ':' + str(DEATH_RATE))
        print('Survival Rate:' + MODEL_NAMES[count_outer] + ':' + str(SURVIVAL_RATE))
        print('Profit Chance:' + MODEL_NAMES[count_outer] + ':' + str(PROFIT_CHANCE))
    # graph
    pyplot.ylabel('Account Value')
    pyplot.xlabel('Wager Count')
    pyplot.axhline(0, color='r')
    pyplot.show()
