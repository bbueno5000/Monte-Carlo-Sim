import random

def roll_dice():
    return random.randint(1, 100)

for count in range(100):
    print(roll_dice())
