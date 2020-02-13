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
        broke_count, value, current_wager = 0, bankroll, initial_wager
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
        return broke_count

    def roll_dice(self):
        """
        DOCSTRING
        """
        return bool(100 > random.randint(1, 100) > 50)

    def simple_bettor(self, bankroll, initial_wager, wager_count, color):
        """
        DOCSTRING
        """
        broke_count, value, values, wagers = 0, bankroll, [], []
        for count in range(1, wager_count):
            if self.roll_dice():
                value += initial_wager
            else:
                value -= initial_wager
                if value < 0:
                    broke_count += 1
                    break
            wagers.append(count)
            values.append(value)
        pyplot.plot(wagers, values, color)
        return broke_count

if __name__ == '__main__':
    for _ in range(SAMPLE_SIZE):
        broke_count_a = MonteCarloSimulation().simple_bettor(BANKROLL, WAGER_SIZE, NUM_WAGERS, 'k')
        broke_count_b = MonteCarloSimulation().martingale_bettor(BANKROLL, WAGER_SIZE, NUM_WAGERS, 'c')
    DEATH_RATE = (broke_count_a/float(SAMPLE_SIZE))*100
    SURVIVAL_RATE = 100-DEATH_RATE
    print('Death Rate:Simple:' + str(DEATH_RATE))
    print('Survival Rate:Simple:' + str(SURVIVAL_RATE))
    DEATH_RATE = (broke_count_b/float(SAMPLE_SIZE))*100
    SURVIVAL_RATE = 100-DEATH_RATE
    print('Death Rate:Martingale:' + str(DEATH_RATE))
    print('Survival Rate:Martingale:' + str(SURVIVAL_RATE))
    pyplot.ylabel('Account Value')
    pyplot.xlabel('Wager Count')
    pyplot.axhline(0, color='r')
    pyplot.show()
